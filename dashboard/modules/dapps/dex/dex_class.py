from dashboard.modules.dapps.dapp_class import *


# UNISWAP


abis_folder = os.path.join(tk.dex_dapp_folder_path, 'abis')



with open(os.path.join(abis_folder, 'erc20ABI.json')) as f:
    erc20_abi = json.load(f)

with open(os.path.join(abis_folder, 'weth_abi.json')) as f:
    weth_abi = json.load(f)

with open(os.path.join(abis_folder, 'v2_router_abi.json')) as f:
    V2_ROUTER_ABI = json.load(f)


# ABI for Uniswap V2 Router (minimal for getAmountsOut)

# Initialize contract



class Dex(Dapp):
    def __init__(self):

        super().__init__('mainnet')

        self.dapp_name = 'dex'
        tk.logger.info(f"initiating {self.dapp_name} W3...")

        self.uniswap_token_addresses = {
            'mainnet': {
                'dai': '0x6b175474e89094c44da98b954eedeac495271d0f',
                'weth': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
                'wbtc': '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599',
                'usdt': '0xdac17f958d2ee523a2206206994597c13d831ec7',
                'usdc': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
                'hex': '0x2b591e99afe9f32eaa6214f7b7629768c40eeb39',
                'mkr': '0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2',
                'link': '0x514910771af9ca656af840dff83e8264ecf986ca',
                'wsol': '0xd31a59c85ae9d8edefec411d448f90841571b89c',
            },
            'sepolia': {
                'weth': '0xfff9976782d46cc05630d1f6ebab18b2324d6b14',
                'usdc': '0x94a9D9AC8a22534E3FaCa9F4e7F2E2cf85d5E4C8',

            },
        }


        self.token_addresses = self.uniswap_token_addresses
        
        self.max_gas_fee_multiplier = 1.5
        self.gas_custom_token_limit = 400_000



        self.weth = Token(name='weth', network=self.network, address=self.uniswap_token_addresses[self.network]['weth'], decimals=18, fee_tiers = 500,
                          abi=weth_abi, w3=self.w3)
        

        self.usdc = Token(name='usdc', network=self.network, address=self.uniswap_token_addresses[self.network]['usdc'], decimals=6, fee_tiers = 500,
                          abi=erc20_abi, w3=self.w3)



        # uniswap_mainnet_factory_address = "0xc0a47dFe034B400B47bDaD5FecDa2621de6c4d95"

        # uniswap_factory_abi = '[{"name":"NewExchange","inputs":[{"type":"address","name":"token","indexed":true},{"type":"address","name":"exchange","indexed":true}],"anonymous":false,"type":"event"},{"name":"initializeFactory","outputs":[],"inputs":[{"type":"address","name":"template"}],"constant":false,"payable":false,"type":"function","gas":35725},{"name":"createExchange","outputs":[{"type":"address","name":"out"}],"inputs":[{"type":"address","name":"token"}],"constant":false,"payable":false,"type":"function","gas":187911},{"name":"getExchange","outputs":[{"type":"address","name":"out"}],"inputs":[{"type":"address","name":"token"}],"constant":true,"payable":false,"type":"function","gas":715},{"name":"getToken","outputs":[{"type":"address","name":"out"}],"inputs":[{"type":"address","name":"exchange"}],"constant":true,"payable":false,"type":"function","gas":745},{"name":"getTokenWithId","outputs":[{"type":"address","name":"out"}],"inputs":[{"type":"uint256","name":"token_id"}],"constant":true,"payable":false,"type":"function","gas":736},{"name":"exchangeTemplate","outputs":[{"type":"address","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":633},{"name":"tokenCount","outputs":[{"type":"uint256","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":663}]'
        # uniswap_token_abi = '[{"name":"Transfer","inputs":[{"type":"address","name":"_from","indexed":true},{"type":"address","name":"_to","indexed":true},{"type":"uint256","name":"_value","indexed":false}],"anonymous":false,"type":"event"},{"name":"Approval","inputs":[{"type":"address","name":"_owner","indexed":true},{"type":"address","name":"_spender","indexed":true},{"type":"uint256","name":"_value","indexed":false}],"anonymous":false,"type":"event"},{"name":"__init__","outputs":[],"inputs":[{"type":"bytes32","name":"_name"},{"type":"bytes32","name":"_symbol"},{"type":"uint256","name":"_decimals"},{"type":"uint256","name":"_supply"}],"constant":false,"payable":false,"type":"constructor"},{"name":"deposit","outputs":[],"inputs":[],"constant":false,"payable":true,"type":"function","gas":74279},{"name":"withdraw","outputs":[{"type":"bool","name":"out"}],"inputs":[{"type":"uint256","name":"_value"}],"constant":false,"payable":false,"type":"function","gas":108706},{"name":"totalSupply","outputs":[{"type":"uint256","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":543},{"name":"balanceOf","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"address","name":"_owner"}],"constant":true,"payable":false,"type":"function","gas":745},{"name":"transfer","outputs":[{"type":"bool","name":"out"}],"inputs":[{"type":"address","name":"_to"},{"type":"uint256","name":"_value"}],"constant":false,"payable":false,"type":"function","gas":74698},{"name":"transferFrom","outputs":[{"type":"bool","name":"out"}],"inputs":[{"type":"address","name":"_from"},{"type":"address","name":"_to"},{"type":"uint256","name":"_value"}],"constant":false,"payable":false,"type":"function","gas":110600},{"name":"approve","outputs":[{"type":"bool","name":"out"}],"inputs":[{"type":"address","name":"_spender"},{"type":"uint256","name":"_value"}],"constant":false,"payable":false,"type":"function","gas":37888},{"name":"allowance","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"address","name":"_owner"},{"type":"address","name":"_spender"}],"constant":true,"payable":false,"type":"function","gas":1025},{"name":"name","outputs":[{"type":"bytes32","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":723},{"name":"symbol","outputs":[{"type":"bytes32","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":753},{"name":"decimals","outputs":[{"type":"uint256","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":783}]'

        # Uniswap V2 Router address (Mainnet)
        self.V2_ROUTER_ADDRESS = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"


        # V2
        # self.v2_factory_contract = self.w3.eth.contract(abi=json.loads(uniswap_factory_abi), address=self.w3.to_checksum_address(uniswap_mainnet_factory_address))
        self.v2_router_contract  = self.w3.eth.contract(abi=V2_ROUTER_ABI, address=self.V2_ROUTER_ADDRESS)

        


        tk.logger.info("DEX V2 fully initiated")



    def get_coin_price(self, coin):
        admin_settings = tk.get_admin_settings()
        return admin_settings.prices[coin.lower()]


    def check_balance_of_token_by_contract_address(self, token_contract_address, token_decimals):
        tk.logger.info("checking balance of token by the contract address...")

        token_contract = self.get_token_contract_object(token_contract_address)
        # token_decimals = token_contract.functions.decimals.call()

        balance = token_contract.functions.balanceOf(self.account_public_checksum_address).call() / pow(10, token_decimals)
        tk.logger.info(f'balance: {balance}')
        return balance



    def eth_balance(self):
        tk.logger.info("eth_balance...")
        return self.w3.eth.get_balance(self.account_public_checksum_address) / pow(10, self.weth.decimals)

    def weth_balance(self):
        tk.logger.info("weth_balance...")
        return self.weth.contract.functions.balanceOf(self.w3.eth.default_account).call() / pow(10, self.weth.decimals)


    def usdc_balance(self):
        tk.logger.info("usdc_balance...")
        return self.usdc.contract.functions.balanceOf(self.w3.eth.default_account).call() / pow(10, self.usdc.decimals)



    def approve_spenders(self, token_contract_address):

        """
        To sell a token, it is needed to have approved the V2 Router contract to spend the token
        this approval is not needed for buying the token
        """
        token_contract = self.get_token_contract_object(token_contract_address)

        action = token_contract.functions.approve(self.v2_router_contract.address, 2**256 - 1)

        tx_return = self.build_and_execute_tx(action=action)

        tk.logger.info(tx_return)

        return tx_return['successful']



    def get_token_contract_object(self, token_contract_address):
        return self.w3.eth.contract(
                abi=erc20_abi, 
                address=self.w3.to_checksum_address(token_contract_address)
            )


    def v2_quote(self, token_contract_address, token_decimals,
    
                #buying token:
                buying_token=True,  fiat_amount=None,
                
                # selling token:
                                    token_amount_to_sell=None):

        token_price_usd = None

        try:

            # token_contract = self.get_token_contract_object(token_contract_address)
            # token_decimals = token_contract.functions.decimals.call()

            if buying_token:
                # pay weth, receive token
                if fiat_amount:
                    weth_amount_in = fiat_amount / self.get_coin_price('weth')
                    amount_in = self.w3.to_wei(weth_amount_in, 'ether')

                else:
                    amount_in = self.w3.to_wei(1, 'ether')



                swap_path = [self.w3.to_checksum_address(self.weth.address), self.w3.to_checksum_address(token_contract_address)]
                token_out_decimals = token_decimals
            else:
                # pay token, receive weth
                amount_in = int(token_amount_to_sell * pow(10, token_decimals))
                swap_path = [self.w3.to_checksum_address(token_contract_address), self.w3.to_checksum_address(self.weth.address)]
                token_out_decimals = self.weth.decimals


            quote = self.v2_router_contract.functions.getAmountsOut(
                amount_in, 
                swap_path
                ).call()

            if buying_token:

                token_price_usd = (self.get_coin_price('weth') / (quote[-1] / quote[0])) / pow(10, token_decimals)

            else:
                token_price_usd = (self.get_coin_price('weth') / (quote[0] / quote[-1])) / pow(10, token_decimals)

            tk.logger.info(f'quoted token price: {token_price_usd}')

        
        except:
            tk.logger.info(format_exc())

        finally:
            return token_price_usd





    def fiat_to_token(self, token_contract_address, token_decimals, fiat_amount, tries, transaction_object):


        """
        V2:
            eth -> token
        """

        for i in range(tries):

            # token_price_usd = self.v2_quote(
            #         token_contract_address, 
            #         token_decimals=token_decimals,
            #         buying_token=True,
            #         fiat_amount=fiat_amount
            #     )

            tk.logger.info(f'performing fiat_to_token (weth -> token)     fiat_amount: {fiat_amount}     V2')

            tx_fee = 0

            weth_price = self.get_coin_price('weth')

            weth_amount_in = fiat_amount / weth_price
            amount_in = self.w3.to_wei(weth_amount_in, 'ether')

            # amount_out_expected = fiat_amount / token_price_usd

            # amountOutMin = int(0.8 * amount_out_expected * pow(10, token_decimals))
            amountOutMin = 0

            deadline = int(time.time() + 300)  # 5 minutes
            # path = [WETH_ADDRESS, TOKEN_ADDRESS]
            path = [
                        self.w3.to_checksum_address(self.weth.address), 
                        self.w3.to_checksum_address(token_contract_address)
                    ]

            # action = self.v2_router_contract.functions.swapExactETHForTokens(
            #     amountOutMin,
            #     path,
            #     self.w3.eth.default_account,
            #     deadline
            # )


            action = self.v2_router_contract.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
                amountOutMin,
                path,
                self.w3.eth.default_account,
                deadline
            )

            tx_return = self.build_and_execute_tx(action=action, value=amount_in, transaction_object=transaction_object)

            tk.logger.info(tx_return)

            successful = tx_return['successful']
            tx_hash = tx_return['tx_hash']
            tx_fee_in_eth = tx_return['tx_fee_in_eth']

            if successful:
                token_out_bought = 0
                # token_out_bought = tx_return['logs_results'][token_out.name]['amount']

                return successful, token_out_bought, tx_hash, tx_fee_in_eth


        return False, None, None, None






    # selling the token
    def token_to_weth(self, token_contract_address, token_decimals, token_amount_to_sell, tries, transaction_object):


        """
        V2:
            token -> eth
        """

        for i in range(tries):

            token_price_usd = self.v2_quote(
                token_contract_address, 
                token_decimals=token_decimals,
                buying_token=False, 
                token_amount_to_sell=token_amount_to_sell)

            tk.logger.info(f'performing token_to_weth (token -> weth)     token_amount: {token_amount_to_sell}     V2')

            tx_fee = 0

            weth_price = self.get_coin_price('weth')

            weth_amount_expected = token_price_usd * token_amount_to_sell / weth_price


            weth_amount_out_min = int(0.8 * weth_amount_expected * pow(10, self.weth.decimals))
            # weth_amount_out_min=0

            token_amount_in = int(token_amount_to_sell * pow(10, token_decimals))
            # token_amount_in = int(token_amount_to_sell )

            deadline = int(time.time() + 300)  # 5 minutes

            path = [
                        self.w3.to_checksum_address(token_contract_address),
                        self.w3.to_checksum_address(self.weth.address)
                    ]

            action = self.v2_router_contract.functions.swapExactTokensForETH(

                amountIn=token_amount_in,
                amountOutMin=weth_amount_out_min,
                path=path,
                to=self.w3.eth.default_account,
                deadline=deadline,


            )

            tx_return = self.build_and_execute_tx(action=action, transaction_object=transaction_object)

            tk.logger.info(tx_return)

            successful = tx_return['successful']
            tx_fee_in_eth = tx_return['tx_fee_in_eth']

            if successful:
                weth_received = 0
                # token_out_bought = tx_return['logs_results'][token_out.name]['amount']

                return successful, weth_received, tx_fee_in_eth


        return False, None, None
