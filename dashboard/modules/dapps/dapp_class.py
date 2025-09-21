from django.db.models import Empty
from web3 import Web3
import time
import json
import os

from traceback import format_exc

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

class Dapp():
    def __init__(self, network='mainnet'):
        self.network = network


        self.mainnet_infura_url = f"https://{self.network}.infura.io/v3/3f440b85f4ab47{os.getenv('trader_mainnet_infura_url')}" 
        

        
        
        
        self.default_account_address = f"0x0CF89B3E8B6BdF43e{os.getenv('trader_default_account_address')}"
        self.account_private_key = f"c01be2ee6b174632ad3c0e16a10{os.getenv('trader_account_private_key')}"




        self.w3 = Web3(Web3.HTTPProvider(self.mainnet_infura_url))
        self.w3.eth.default_account = self.w3.to_checksum_address(self.default_account_address)


        # below properties are set by the dapp itself at its own init
        self.dapp_name = ""
        self.token_addresses = {}

        self.max_gas_fee_multiplier = 0
        self.gas_limit = 0
        self.gas_custom_token_limit = 0



    def get_token_object(self, token_string) -> Token:
        
        if token_string.lower() in ['eth', 'weth']:
            return self.weth

        elif token_string.lower() == 'usdc':
            return self.usdc

        # elif token_string.lower() == 'dai':
        #     return self.dai
        
        # elif token_string.lower() == 'wbtc':
        #     return self.wbtc

        # elif token_string.lower() == 'wsol':
        #     return self.wsol

        # elif token_string.lower() == 'usdt':
        #     return self.usdt
        
        else:
            raise

    def get_network_gas_price(self):

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





    def build_and_execute_tx(self, action, transaction_object=None, value=0):

        receipt = None

        try:

            tk.logger.info(f'building tx for action: {action.fn_name}')

            gas_info = self.get_network_gas_price()

            assert not gas_info is None

            nonce = self.w3.eth.get_transaction_count(self.w3.eth.default_account) 


            tx_settings = {
                'chainId': 1,

                'from': self.w3.eth.default_account,
                'value': value,

                'gas': self.gas_custom_token_limit,
                'maxFeePerGas': self.w3.to_wei(gas_info['maxFeePerGas_gwei'], 'gwei'),
                'maxPriorityFeePerGas': self.w3.to_wei(gas_info['maxPriorityFeePerGas_gwei'], 'gwei'),
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

            if transaction_object is not None:
                transaction_object.hash = tx_hash
                transaction_object.save()


            tk.logger.info(
                f'waiting for https://{"" if self.network == "mainnet" else self.network + "."}etherscan.io/tx/{self.w3.to_hex(tx_hash)} \n')

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