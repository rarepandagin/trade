from dashboard.modules.dapps.dapp_class import *

# ARBI

"""
AAVE pool on testnet
    0x16dA4541aD1807f4443d92D26044C1147406EB80

"""

class Arbi(Dapp):
    def __init__(self):

        super().__init__(network='sepolia')

        self.dapp_name = "arbi"

        tk.logger.info(f"initiating {self.dapp_name} W3 on {self.network}...")

        self.token_addresses = {
            'mainnet': {
                'dai': '0x6B175474E89094C44Da98b954EedeAC495271d0F',
                'weth': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
                'usdc': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
                'wbtc': '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599',
            },

            'sepolia': {
                'dai': '0xFF34B3d4Aee8ddCd6F9AFFFB6Fe49bD371b8a357',
                'weth': '0xC558DBdd856501FCd9aaF1E62eae57A9F0629a3c',
                'usdc': '0x94a9D9AC8a22534E3FaCa9F4e7F2E2cf85d5E4C8',
                'wbtc': '0x29f2D40B0605204364af54EC677bD022dA425d03',
                'link': '0xf8Fb3713D459D7C1018BD0A49D19b4C44290EBE5',
            },
        }

        self.contract_addresses = {
            'mainnet': {
                'flash_loan': '',
            },

            'sepolia': {
                'flash_loan':               '0xe50A99785857340df82A4928932cBA81ef06B0d6',
                'dex':                      '0xb0581C4aB425CDf36fF23593be4C46d08B0F3743',
                'flash_loan_arbitrage_no_logic':     '0x9568dd9333C2423D60F50B47b5c505B70F05421C',
                'flash_loan_arbitrage':     '0x293879b3752f990ebD634e2202B55162Fc0C64f8',
            }
        }



        self.abis_folder = os.path.join(tk.arbi_dapp_folder_path, 'abis')

        self.abis = {}

        with open(os.path.join(self.abis_folder, 'erc20ABI.json')) as f:
            self.abis['erc20'] = json.load(f)

        with open(os.path.join(self.abis_folder, "flash_loan.json")) as f:
            self.abis['flash_loan'] = json.load(f)

        with open(os.path.join(self.abis_folder, 'dex.json')) as f:
            self.abis['dex'] = json.load(f)

        with open(os.path.join(self.abis_folder, 'flash_loan_arbitrage.json')) as f:
            self.abis['flash_loan_arbitrage'] = json.load(f)

        with open(os.path.join(self.abis_folder, 'weth.json')) as f:
            self.abis['weth'] = json.load(f)





        self.max_gas_fee_multiplier = 2.5
        self.gas_limit = 22_0000
        self.gas_custom_token_limit = 600_000


        
        # self.eth = Token(name='eth', network=self.network, address=self.token_addresses[self.network]['eth'], decimals=18, fee_tiers = 500,
        #                   abi=erc20_abi, w3=self.w3)
                
        self.weth = Token(name='weth', network=self.network, address=self.token_addresses[self.network]['weth'], decimals=18, fee_tiers = 500,
                          abi=self.abis['weth'], w3=self.w3)
        
        self.dai = Token(name='dai', network=self.network, address=self.token_addresses[self.network]['dai'], decimals=18, fee_tiers = 500,
                         abi=self.abis['erc20'], w3=self.w3)

        self.usdc = Token(name='usdc', network=self.network, address=self.token_addresses[self.network]['usdc'], decimals=6, fee_tiers = 500,
                          abi=self.abis['erc20'], w3=self.w3)

        # self.wbtc = Token(name='wbtc', network=self.network, address=self.token_addresses[self.network]['wbtc'], decimals=8, fee_tiers = 500,
        #                   abi=wbtc_abi, w3=self.w3)



        # self.flash_loan_contract = self.w3.eth.contract(abi=flash_loan_abi,
        #                                                     address=self.w3.to_checksum_address(
        #                                                         self.contract_addresses[self.network]['flash_loan']))



        # self.flash_loan_arbitrage = self.w3.eth.contract(abi=flash_loan_arbitrage_abi,
        #                                                     address=self.w3.to_checksum_address(
        #                                                         self.contract_addresses[self.network]['flash_loan_arbitrage']))



        # self.dex = self.w3.eth.contract(abi=dex_abi,
        #                                                     address=self.w3.to_checksum_address(
        #                                                         self.contract_addresses[self.network]['dex']))


        self.flash_loan             = Contract(name='flash_loan',           dapp=self)
        self.flash_loan_arbitrage   = Contract(name='flash_loan_arbitrage', dapp=self)
        self.dex                    = Contract(name='dex',                  dapp=self)







    def approve_spenders(self):
        # self.approve(spender=self.contract_addresses[self.network]['flash_loan_arbitrage'], token=self.usdc)
        # self.approve(spender=self.contract_addresses[self.network]['flash_loan_arbitrage'], token=self.dai)

        # self.approve(spender=self.flash_loan.address, token=self.usdc)
        # self.approve(spender=self.contract_addresses[self.network]['dex'], token=self.dai)

        # action = token.contract.functions.approve(self.w3.to_checksum_address(spender), 2**256 - 1)

        # self.build_and_execute_tx(action=action)




        self.build_and_execute_tx(action=self.flash_loan_arbitrage.contract.functions.approveDAI(2**256 - 1))
        self.build_and_execute_tx(action=self.flash_loan_arbitrage.contract.functions.approveUSDC(2**256 - 1))


        return True





    def get_balance(self):


        ret = {}
        for contract in [self.dex, self.flash_loan_arbitrage, self.flash_loan]:
            ret[contract.name] = {}
            for token in [self.dai, self.usdc]:
                ret[contract.name][token.name] = contract.contract.functions.getBalance(
                    self.token_addresses[self.network][token.name]
                ).call() / (10 ** token.decimals)

        tk.logger.info(ret)
        return ret


    def deposit(self):

        self.build_and_execute_tx(action=self.usdc.contract.functions.transfer(
            self.flash_loan_arbitrage.address,
            int(2000 * (10 ** self.usdc.decimals)),
        ))

        self.build_and_execute_tx(action=self.dai.contract.functions.transfer(
            self.flash_loan_arbitrage.address,
            int(2000 * (10 ** self.dai.decimals)),
        ))


        self.build_and_execute_tx(action=self.usdc.contract.functions.transfer(
            self.dex.address,
            int(2000 * (10 ** self.usdc.decimals)),
        ))

        self.build_and_execute_tx(action=self.dai.contract.functions.transfer(
            self.dex.address,
            int(2000 * (10 ** self.dai.decimals)),
        ))


        # self.build_and_execute_tx(action=self.usdc.contract.functions.transfer(
        #     self.flash_loan.address,
        #     int(1000 * (10 ** self.usdc.decimals)),
        # ))

        # self.build_and_execute_tx(action=self.dai.contract.functions.transfer(
        #     self.flash_loan.address,
        #     int(1000 * (10 ** self.dai.decimals)),
        # ))


    def withdraw(self):
        self.build_and_execute_tx(action=self.flash_loan_arbitrage.contract.functions.withdraw(self.dai.address))
        self.build_and_execute_tx(action=self.flash_loan_arbitrage.contract.functions.withdraw(self.usdc.address))
        # self.build_and_execute_tx(action=self.flash_loan.contract.functions.withdraw(self.dai.address))
        # self.build_and_execute_tx(action=self.flash_loan.contract.functions.withdraw(self.usdc.address))


        tk.logger.info('withdraw')


    def get_allowance(self):
        ret = {}
        for token in [self.dai, self.usdc]:
            ret[token.name] = {}
            # for contract in ['dex', 'flash_loan_arbitrage']:
            ret[token.name] = token.contract.functions.allowance(
                self.flash_loan_arbitrage.address,
                self.dex.address
            ).call()

        ret['allowanceUSDC'] = self.flash_loan_arbitrage.contract.functions.allowanceUSDC().call()
        ret['allowanceDAI'] = self.flash_loan_arbitrage.contract.functions.allowanceDAI().call()

        tk.logger.info(ret)

        return ret



    def perform_flash_loan(self, token:Token, amount):
        # interface for contract function requestFlashLoan

        amount_by_token_decimal = int(amount * (10 ** token.decimals))
        

        # bare structure
        # action = self.flash_loan.contract.functions.requestFlashLoan(
        #     token.address,
        #     amount_by_token_decimal,
        # )

        # mock arbitrage
        action = self.flash_loan_arbitrage.contract.functions.requestFlashLoan(
            token.address,
            amount_by_token_decimal,
        )

        tx_return = self.build_and_execute_tx(action=action)
        
        return tx_return



