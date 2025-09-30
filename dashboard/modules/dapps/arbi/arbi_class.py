from dashboard.modules.dapps.dapp_class import *
from threading import Thread
from mysite import settings
# ARBI

"""
AAVE pool on testnet
    0x16dA4541aD1807f4443d92D26044C1147406EB80

"""

class Arbi(Dapp):
    def __init__(self):

        super().__init__(network='mainnet')

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
                'dai':          '0xFF34B3d4Aee8ddCd6F9AFFFB6Fe49bD371b8a357',
                'weth':         '0xC558DBdd856501FCd9aaF1E62eae57A9F0629a3c',
                'weth_uniswap': '0xfff9976782d46cc05630d1f6ebab18b2324d6b14',
                'usdc':         '0x94a9D9AC8a22534E3FaCa9F4e7F2E2cf85d5E4C8',
                'wbtc':         '0x29f2D40B0605204364af54EC677bD022dA425d03',
                'link':         '0xf8Fb3713D459D7C1018BD0A49D19b4C44290EBE5',
            },
        }

        self.contract_addresses = {
            'mainnet': {
                'single_swap':              '0xf87F2b58162bA2140F2E92858e862Da6d2c47940',

            },

            'sepolia': {
                'flash_loan':               '0xe50A99785857340df82A4928932cBA81ef06B0d6',

                'hello':                    '0xb09B70CaA461e78Daf4e2321F167ba8F8b84584e',
                'arbitrage':                '0xA53a3782631eB5bCB6B64fF60B4CaE3367B25D1B',

                'dex':                      '0xb96c7E71F6611cffcE5d9B32f384F815f3216418',
                'flash_loan_arbitrage':     '0xBaD335D0d320034E8eF30375881a8D5ac1029Fa3',


                'single_swap':              '0xf87F2b58162bA2140F2E92858e862Da6d2c47940',

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

        with open(os.path.join(self.abis_folder, 'hello.json')) as f:
            self.abis['hello'] = json.load(f)

        with open(os.path.join(self.abis_folder, 'arbitrage.json')) as f:
            self.abis['arbitrage'] = json.load(f)


        with open(os.path.join(self.abis_folder, 'single_swap.json')) as f:
            self.abis['single_swap'] = json.load(f)





        self.max_gas_fee_multiplier = 2.5
        self.gas_custom_token_limit = 1_500_000


        
        # self.eth = Token(name='eth', network=self.network, address=self.token_addresses[self.network]['eth'], decimals=18, fee_tiers = 500,
        #                   abi=erc20_abi, w3=self.w3)
                
        self.weth = Token(name='weth', network=self.network, address=self.token_addresses[self.network]['weth'], decimals=18, fee_tiers = 500,
                          abi=self.abis['weth'], w3=self.w3)
                        
        # self.weth_uniswap = Token(name='weth_uniswap', network=self.network, address=self.token_addresses[self.network]['weth_uniswap'], decimals=18, fee_tiers = 500,
        #                   abi=self.abis['weth'], w3=self.w3)
        
        self.dai = Token(name='dai', network=self.network, address=self.token_addresses[self.network]['dai'], decimals=18, fee_tiers = 500,
                         abi=self.abis['erc20'], w3=self.w3)

        self.usdc = Token(name='usdc', network=self.network, address=self.token_addresses[self.network]['usdc'], decimals=6, fee_tiers = 500,
                          abi=self.abis['erc20'], w3=self.w3)

        # self.wbtc = Token(name='wbtc', network=self.network, address=self.token_addresses[self.network]['wbtc'], decimals=8, fee_tiers = 500,
        #                   abi=wbtc_abi, w3=self.w3)


        # self.flash_loan             = Contract(name='flash_loan',           dapp=self)
        # self.flash_loan_arbitrage   = Contract(name='flash_loan_arbitrage', dapp=self)
        # self.dex                    = Contract(name='dex',                  dapp=self)
        # self.hello                  = Contract(name='hello',                dapp=self)
        # self.arbitrage              = Contract(name='arbitrage',            dapp=self)
        self.single_swap            = Contract(name='single_swap',          dapp=self)

        self.token_one = None
        self.token_two = None


    def get_balance(self):


        ret = {}
        # for contract in [self.dex, self.flash_loan_arbitrage, self.single_swap]:
        for contract in [self.single_swap]:
        # for contract in [self.arbitrage]:
            ret[contract.name] = {}
            for token in [self.dai, self.usdc, self.weth]:
                ret[contract.name][token.name] = contract.contract.functions.getBalance(
                    self.w3.to_checksum_address(self.token_addresses[self.network][token.name])
                ).call() / (10 ** token.decimals)

        # ret['dex_token_one_balances'] = self.dex.contract.functions.token_one_balances().call() / (10 ** self.token_one.decimals)
        # ret['dex_token_two_balances'] = self.dex.contract.functions.token_two_balances().call() / (10 ** self.token_two.decimals)

        tk.logger.info(ret)
        return ret





    def approve_token_for_flash_loan_arbitrage(self, token:Token, nonce=None):
        self.build_and_execute_tx(action=self.flash_loan_arbitrage.contract.functions.approveToken(token.address, 2**256 - 1), nonce=nonce)

    # def approve_usdc_for_flash_loan_arbitrage(self, nonce=None):
    #     self.build_and_execute_tx(action=self.flash_loan_arbitrage.contract.functions.approveToken(2**256 - 1), nonce=nonce)




    # def approve_dai_for_arbitrage(self, nonce=None):
    #     self.build_and_execute_tx(action=self.arbitrage.contract.functions.approveTokenTwo(2**256 - 1), nonce=nonce)

    # def approve_usdc_for_arbitrage(self, nonce=None):
    #     self.build_and_execute_tx(action=self.arbitrage.contract.functions.approveTokenOne(2**256 - 1), nonce=nonce)




    def approve_weth_for_single_swap(self, nonce=None):
        self.build_and_execute_tx(action=self.weth.contract.functions.approve(self.w3.to_checksum_address("0xE592427A0AEce92De3Edee1F18E0157C05861564"), 2**256 - 1))

    def approve_usdc_for_single_swap(self, nonce=None):
        self.build_and_execute_tx(action=self.usdc.contract.functions.approve(self.w3.to_checksum_address("0xE592427A0AEce92De3Edee1F18E0157C05861564"), 2**256 - 1))





    def approve_spenders(self):

        # self.approve(spender=self.dex.contract.address, token=self.dai)
        # self.approve(spender=self.dex.contract.address, token=self.usdc)
        # self.approve(spender=self.flash_loan_arbitrage.contract.address, token=self.dai)
        # self.approve(spender=self.flash_loan_arbitrage.contract.address, token=self.usdc)
        if settings.DEBUG:
            nonce = self.w3.eth.get_transaction_count(self.w3.eth.default_account)

            # t1 = Thread(target=self.approve_token_for_flash_loan_arbitrage,    args=(self.token_one, nonce + 0,))
            # t2 = Thread(target=self.approve_token_for_flash_loan_arbitrage,    args=(self.token_two, nonce + 1,))

            
            # t1 = Thread(target=self.approve_dai_for_arbitrage,    args=(nonce + 0,))
            # t2 = Thread(target=self.approve_usdc_for_arbitrage,   args=(nonce + 1,))
            t1 = Thread(target=self.approve_weth_for_single_swap,    args=(nonce + 0,))
            t2 = Thread(target=self.approve_usdc_for_single_swap,    args=(nonce + 1,))

            t1.start()
            time.sleep(4)
            # t2.start()

            t1.join()
            # t2.join()


        else:
            pass

            # self.approve_dai_for_flash_loan_arbitrage()
            # self.approve_usdc_for_flash_loan_arbitrage()

            # self.approve_dai_for_arbitrage()
            # self.approve_usdc_for_arbitrage()

        return True



    def get_allowance(self):
        ret = {}
        # for token in [self.dai, self.usdc]:
        #     ret[token.name] = {}
        #     # for contract in ['dex', 'flash_loan_arbitrage']:
        #     ret[token.name] = token.contract.functions.allowance(
        #         self.flash_loan_arbitrage.address,
        #         self.dex.address
        #     ).call()

        ret['allowanceUSDC'] = self.flash_loan_arbitrage.contract.functions.allowanceTokenOne().call()
        ret['allowanceDAI'] = self.flash_loan_arbitrage.contract.functions.allowanceTokenTwo().call()

        # ret['allowanceUSDC'] = self.arbitrage.contract.functionsapp..allowanceTokenOne().call()
        # ret['allowanceDAI'] = self.arbitrage.contract.functions.allowanceTokenTwo().call()

        tk.logger.info(ret)

        return ret




    def deposit_dai_to_dex(self, nonce=None):

        self.build_and_execute_tx(action=self.dai.contract.functions.transfer(
            self.dex.address,
            int(1000 * (10 ** self.dai.decimals)),
        ), nonce= nonce)

    def deposit_usdc_to_dex(self, nonce=None):

        self.build_and_execute_tx(action=self.usdc.contract.functions.transfer(
            self.dex.address,
            int(1000 * (10 ** self.usdc.decimals)),
        ), nonce= nonce)

    def deposit_dai_to_flash_loan_arbitrage(self, nonce=None):

        self.build_and_execute_tx(action=self.dai.contract.functions.transfer(
            self.flash_loan_arbitrage.address,
            int(1000 * (10 ** self.dai.decimals)),
        ), nonce= nonce)

    def deposit_usdc_to_flash_loan_arbitrage(self, nonce=None):

        self.build_and_execute_tx(action=self.usdc.contract.functions.transfer(
            self.flash_loan_arbitrage.address,
            int(1000 * (10 ** self.usdc.decimals)),
        ), nonce= nonce)


    def deposit_usdc_to_single_swap(self, nonce=None):

        self.build_and_execute_tx(action=self.usdc.contract.functions.transfer(
            self.single_swap.address,
            int(1000 * (10 ** self.usdc.decimals)),
        ), nonce= nonce)



    def deposit_weth_to_single_swap(self, nonce=None):

        self.build_and_execute_tx(action=self.weth.contract.functions.transfer(
            self.single_swap.address,
            int(0.001 * (10 ** self.weth.decimals)),
        ), nonce= nonce)


    # def deposit_dai_to_arbitrage(self, nonce=None):

    #     self.build_and_execute_tx(action=self.dai.contract.functions.transfer(
    #         self.arbitrage.address,
    #         int(1000 * (10 ** self.dai.decimals)),
    #     ), nonce= nonce)


    # def deposit_usdc_to_arbitrage(self, nonce=None):

    #     self.build_and_execute_tx(action=self.usdc.contract.functions.transfer(
    #         self.arbitrage.address,
    #         int(1000 * (10 ** self.usdc.decimals)),
    #     ), nonce= nonce)



    def deposit(self):
        if settings.DEBUG:
            nonce = self.w3.eth.get_transaction_count(self.w3.eth.default_account)
            
            # t1 = Thread(target=self.deposit_dai_to_dex,                      args=(nonce + 0,))
            # t2 = Thread(target=self.deposit_usdc_to_dex,                     args=(nonce + 1,))
            # t3 = Thread(target=self.deposit_dai_to_flash_loan_arbitrage,     args=(nonce + 2,))
            # t4 = Thread(target=self.deposit_usdc_to_flash_loan_arbitrage,    args=(nonce + 3,))
            # t5 = Thread(target=self.deposit_usdc_to_single_swap,    args=(nonce + 0,))
            t5 = Thread(target=self.deposit_weth_to_single_swap,    args=(nonce + 0,))

            # t1 = Thread(target=self.deposit_dai_to_arbitrage,                      args=(nonce + 0,))
            # t2 = Thread(target=self.deposit_usdc_to_arbitrage,                     args=(nonce + 1,))

            # t1.start()
            # time.sleep(2)
            # t2.start()
            # time.sleep(2)
            # t3.start()
            # time.sleep(2)
            # t4.start()
            # time.sleep(2)
            t5.start()

            # t1.join()
            # t2.join()
            # t3.join()
            # t4.join()
            t5.join()

        else:
            pass
            # self.deposit_dai_to_arbitrage()
            # self.deposit_usdc_to_arbitrage()

            # self.deposit_dai_to_dex()
            # self.deposit_usdc_to_dex()
            # self.deposit_dai_to_flash_loan_arbitrage()
            # self.deposit_usdc_to_flash_loan_arbitrage()



    def withdraw_dai_from_dex(self, nonce=None):
        self.build_and_execute_tx(action=self.dex.contract.functions.withdraw(self.dai.address),nonce=nonce)

    def withdraw_usdc_from_dex(self, nonce=None):
        self.build_and_execute_tx(action=self.dex.contract.functions.withdraw(self.usdc.address),nonce=nonce)

    def withdraw_dai_from_flash_loan_arbitrage(self, nonce=None):
        self.build_and_execute_tx(action=self.flash_loan_arbitrage.contract.functions.withdraw(self.dai.address),nonce=nonce)

    def withdraw_usdc_from_flash_loan_arbitrage(self, nonce=None):
        self.build_and_execute_tx(action=self.flash_loan_arbitrage.contract.functions.withdraw(self.usdc.address),nonce=nonce)

    # def withdraw_dai_from_arbitrage(self, nonce=None):
    #     self.build_and_execute_tx(action=self.arbitrage.contract.functions.withdraw(self.dai.address),nonce=nonce)

    # def withdraw_usdc_from_arbitrage(self, nonce=None):
    #     self.build_and_execute_tx(action=self.arbitrage.contract.functions.withdraw(self.usdc.address),nonce=nonce)


    def withdraw_weth_from_single_swap(self, nonce=None):
        self.build_and_execute_tx(action=self.single_swap.contract.functions.withdraw(self.weth.address),nonce=nonce)


    def withdraw_usdc_from_single_swap(self, nonce=None):
        self.build_and_execute_tx(action=self.single_swap.contract.functions.withdraw(self.usdc.address),nonce=nonce)



    def withdraw(self):

        if settings.DEBUG:
            nonce = self.w3.eth.get_transaction_count(self.w3.eth.default_account)

            # t1 = Thread(target=self.withdraw_dai_from_dex,                   args=(nonce + 0,))
            # t2 = Thread(target=self.withdraw_usdc_from_dex,                  args=(nonce + 1,))
            # t3 = Thread(target=self.withdraw_dai_from_flash_loan_arbitrage,  args=(nonce + 2,))
            # t4 = Thread(target=self.withdraw_usdc_from_flash_loan_arbitrage, args=(nonce + 3,))
            t5 = Thread(target=self.withdraw_weth_from_single_swap, args=(nonce + 0,))
            t6 = Thread(target=self.withdraw_usdc_from_single_swap, args=(nonce + 1,))

            # t1 = Thread(target=self.withdraw_dai_from_arbitrage,                   args=(nonce + 0,))
            # t2 = Thread(target=self.withdraw_usdc_from_arbitrage,                  args=(nonce + 1,))


            # t1.start()
            # time.sleep(3)
            # t2.start()
            # time.sleep(3)
            # t3.start()
            # time.sleep(2)
            # t4.start()
            # time.sleep(2)
            t5.start()
            time.sleep(2)
            t6.start()

            # t1.join()
            # t2.join()
            # t3.join()
            # t4.join()
            t5.join()
            t6.join()


        else:
            pass
            # self.withdraw_dai_from_dex()
            # self.withdraw_usdc_from_dex()
            # self.withdraw_dai_from_flash_loan_arbitrage()
            # self.withdraw_usdc_from_flash_loan_arbitrage()

            # self.withdraw_dai_from_arbitrage()
            # self.withdraw_usdc_from_arbitrage()

        tk.logger.info('withdraw')



    def wrap_eth(self, eth_amount):

        value = int(self.w3.to_wei(eth_amount, "ether"))
        action = self.weth.contract.functions.deposit()
        tx_return = self.build_and_execute_tx(action=action, value=value)
        return tx_return['successful']

    def unwrap_weth(self, eth_amount):

        value = int(self.w3.to_wei(eth_amount, "ether"))
        action = self.weth.contract.functions.withdraw(value)
        tx_return = self.build_and_execute_tx(action=action)
        return tx_return['successful']



    def perform_flash_loan(self, token_one:Token, token_two:Token, token_one_amount):
        # interface for contract function requestFlashLoan

        amount_by_token_decimal = int(token_one_amount * (10 ** token_one.decimals))
        

        # bare structure
        # action = self.flash_loan.contract.functions.requestFlashLoan(
        #     token.address,
        #     amount_by_token_decimal,
        # )

        # mock arbitrage
        action = self.flash_loan_arbitrage.contract.functions.requestFlashLoan(
            token_one.address,
            token_two.address,
            amount_by_token_decimal,
        )

        tx_return = self.build_and_execute_tx(action=action)
        
        
        events = self.flash_loan_arbitrage.contract.events.new_log.get_logs(fromBlock=0, toBlock="latest")
        for event in events:
            tk.logger.info(f"EVENT: {self.process_solidity_log(event)}")
            


    def hello_action(self):
        # calculator

        # tk.logger.info(self.hello.contract.functions.get().call())

        # self.build_and_execute_tx(action=self.hello.contract.functions.multiply(24))

        # tk.logger.info(self.hello.contract.functions.get().call())

        # TWEETER
        # tk.logger.info(f"tweet get: {self.hello.contract.functions.getTweet(self.w3.eth.default_account, 0).call()}")
        # tk.logger.info(f"tweet get: {self.hello.contract.functions.getTweet(self.w3.eth.default_account, 1).call()}")
        # self.build_and_execute_tx(action=self.hello.contract.functions.unpause())
        self.build_and_execute_tx(action=self.hello.contract.functions.createTweet("ZZZ BBB"))

        # tk.logger.info(f"tweet get all: {self.hello.contract.functions.getAllTweets().call()}")
        # tk.logger.info(f"tweet get: {self.hello.contract.functions.getTweet(0).call()}")



        events = self.hello.contract.events.new_log.get_logs(fromBlock=0, toBlock="latest")
        for event in events:
            tk.logger.info(f"EVENT: {event['args']}")


    def perform_single_swap(self):
        amount_by_token_decimal = int(0.0009 * (10 ** self.weth.decimals))

        self.build_and_execute_tx(action=self.single_swap.contract.functions.swapExactInputSingle(
            self.weth.address,
            self.usdc.address,
            amount_by_token_decimal,
            3000

            ))
