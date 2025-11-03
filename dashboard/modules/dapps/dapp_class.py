from itertools import chain
from django.db.models import Empty
from web3 import Web3
from datetime import datetime
import json
import os
import human_readable
import time
from traceback import format_exc
from dashboard.models.models_adminsettings import *
from dashboard.views_pages import toolkit as tk
import os



class Token():
    def __init__(self, name, network, address, abi, decimals, fee_tiers, w3):
        self.name = name
        self.network = network
        self.w3 = w3
        self.address = self.w3.to_checksum_address(address)
        self.abi = abi
        self.contract = self.w3.eth.contract(abi=self.abi, address=self.address)
        self.decimals = decimals
        self.fee_tiers = fee_tiers


class Contract():
    def __init__(self, name, dapp, abi=None):
        self.name = name

        self.dapp = dapp

        if abi is None:
            self.abi = self.dapp.abis[self.name]
        else:
            self.abi = self.dapp.abis[abi]

        
        self.address = self.dapp.contract_addresses[self.dapp.network][self.name]

        self.contract = self.dapp.w3.eth.contract(
                abi=self.abi, 
                address=self.dapp.w3.to_checksum_address(self.address)
            )


class Dapp():
    def __init__(self, network):
        self.network = network


        self.mainnet_infura_url = f"https://{self.network}.infura.io/v3/{os.getenv('trader_mainnet_infura_url')}" 
        self.mainnet_alchemy_url = f"https://eth-mainnet.g.alchemy.com/v2/{os.getenv('trader_mainnet_alchemy_key')}"
        
        

        if self.network == 'mainnet':

            admin_settings = tk.get_admin_settings()

            if admin_settings.active_account == account_hedge:
                self.account_public_address = f"0x30127b1414483aE437427d6f107F13fC54a2B62b"

            elif admin_settings.active_account == account_dex:
                self.account_public_address = "0xD9f4A6615eD03883809D4d8434C33023A174c03d"

            elif admin_settings.active_account == account_ajax:
                self.account_public_address = "0xE7cc257fd6e46ca88985d997682F8BD4d1FEB0E0"


            elif admin_settings.active_account == account_eagle:
                self.account_public_address = "0xf62D1c3fF13863307a8f31c222830b36826B8945"


            elif admin_settings.active_account == account_ranger:
                self.account_public_address = "0x9498eeFb63b412B84FAD21cB8D03C9Becd46F188"


            elif admin_settings.active_account == account_lion:
                self.account_public_address = "0xF15ebFce063630b39d9C9D307dFf377aC7082aEE"


            elif admin_settings.active_account == account_tiger:
                self.account_public_address = "0x7be962ca2efD77Aa3Fe259A6Bd5fe4C9CaD9F69b"


            self.account_private_key = os.getenv(f'{admin_settings.active_account}_private_key')



        else:
            self.account_public_address = f"0x51DAc1f4A5a7439444D8c1ac49ba42c21Aee13B2"
            self.account_private_key = f"9108f9ba583eb7d1a8b745a259935a65684e82c8b643cbfd9c866ecfa85a35b6"
        




        self.w3 = Web3(Web3.HTTPProvider(self.mainnet_alchemy_url))
        

        self.account_public_checksum_address = self.w3.to_checksum_address(self.account_public_address)
        self.w3.eth.default_account = self.account_public_checksum_address


        # below properties are set by the dapp itself at its own init
        self.dapp_name = ""
        self.token_addresses = {}

        self.max_gas_fee_multiplier = 0
        self.gas_custom_token_limit = 0



    def get_token_object(self, token_string) -> Token:
        
        if token_string.lower() in ['eth', 'weth']:
            return self.weth

        elif token_string.lower() == 'usdc':
            return self.usdc

        # elif token_string.lower() == 'dai':
        #     return self.dai
        
        elif token_string.lower() == 'wbtc':
            return self.wbtc

        # elif token_string.lower() == 'wsol':
        #     return self.wsol

        # elif token_string.lower() == 'usdt':
        #     return self.usdt
        
        else:
            raise

    def get_network_gas_price(self):

        """
        ensure that maxFeePerGas is set to a value greater than or equal to maxPriorityFeePerGas
        """

        admin_settings = tk.get_admin_settings()

        full_gas_info = admin_settings.gas

        gas_price_gwei = full_gas_info['gas_basic_price'] + full_gas_info[admin_settings.gas_speed]

        return {
            'maxPriorityFeePerGas_gwei': full_gas_info['FastGasPrice'],
            'maxFeePerGas_gwei': self.max_gas_fee_multiplier * gas_price_gwei,
            'tx_fee_eth': gas_price_gwei * self.gas_custom_token_limit / (10 ** 9),
        }




    def approve(self, spender, token):

        action = token.contract.functions.approve(self.w3.to_checksum_address(spender), 2**256 - 1)

        self.build_and_execute_tx(action=action)





    def build_and_execute_tx(self, action, transaction_object=None, value=0, nonce=None):

        receipt = None

        try:

            tk.logger.info(f'building tx for action: {action.fn_name}')
    
            gas_info = self.get_network_gas_price()

            assert not gas_info is None

            if nonce is None:
                nonce = self.w3.eth.get_transaction_count(self.w3.eth.default_account) 

            chainId = 1 if self.network == 'mainnet' else 11155111

            maxFeePerGas = self.w3.to_wei(gas_info['maxFeePerGas_gwei'], 'gwei')
            maxPriorityFeePerGas = self.w3.to_wei(gas_info['maxPriorityFeePerGas_gwei'], 'gwei')
            
            one_gwei = self.w3.to_wei(1, 'gwei')
            maxPriorityFeePerGas = max(maxPriorityFeePerGas, one_gwei)
            maxFeePerGas = max(maxFeePerGas, maxPriorityFeePerGas)
            
            tx_settings = {
                'chainId': chainId,

                'from': self.w3.eth.default_account,
                'value': value,

                'gas': self.gas_custom_token_limit,
                'maxFeePerGas': maxFeePerGas,
                'maxPriorityFeePerGas': maxPriorityFeePerGas,
                'nonce': nonce,
            }

            tx = action.build_transaction(tx_settings)

            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.account_private_key)

            if hasattr(signed_tx, 'rawTransaction'):
                tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            elif hasattr(signed_tx, 'raw_transaction'):
                tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            else:
                tk.logger.info('the signed tx contains neither a rawTransaction nor a raw_transaction')
                raise

            tx_hash = self.w3.to_hex(tx_hash)

            if transaction_object is not None:
                transaction_object.hash = tx_hash
                transaction_object.save()


            tk.logger.info(
                f'waiting for https://{"" if self.network == "mainnet" else self.network + "."}etherscan.io/tx/{tx_hash} \n')

            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            # while True:
            #     try:
            #         receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            #         break
            #     except:
            #         time.sleep(0.3)


        except:
            tk.logger.info(format_exc())

        finally:
            return self.process_receipt(receipt)



    def process_log(self, log):
        log_token = None
        for token in self.token_addresses['mainnet']:
            if self.token_addresses['mainnet'][token].lower() == log.address.lower():
                log_token = token
                break

        if log_token is None:
            return "unknown", 0

        else:
            token = self.get_token_object(log_token)
            amount = self.w3.to_int(log['data']) / (10 ** token.decimals)

            return token.name, amount



    def process_receipt(self, receipt):

        if receipt is None:

            return {
                'successful': False,
                'tx_hash': "",
                'tx_fee_in_eth': 0,
                'logs_results': [],
            }

        else:

            successful = (receipt.status == 1)

            tx_hash = self.w3.to_hex(receipt.transactionHash)

            tk.logger.info('---------------> successful' if successful else '-------------> failed')

            tx_fee_in_eth = receipt.effectiveGasPrice  * receipt.gasUsed / (10 ** 18)

            logs_results = {}

            try:
                for idx, log in enumerate(receipt.logs):
                    token_name, token_amount = self.process_log(log)
                    logs_results[f"{token_name}"] = {"idx": idx, "amount": token_amount}
            except:
                pass

            return {
                'successful': successful,
                'tx_hash': tx_hash,
                'tx_fee_in_eth': tx_fee_in_eth,
                'logs_results': logs_results,
            }

    def process_solidity_log(self, event):
        datetime_obj = datetime.fromtimestamp(event.args.timestamp)
        delta_time = human_readable.date_time(datetime.now() - datetime_obj)
        return {'delta_time': delta_time, 'content': event.args.content}