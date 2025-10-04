from dashboard.modules.dapps.dapp_class import *





class Sushiswap(Dapp):
    def __init__(self):

        super().__init__('mainnet')

        self.dapp_name = 'sushiswap'

        tk.logger.info(f"initiating {self.dapp_name} W3...")




        self.token_addresses = {
            'mainnet': {
                'weth': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
                'usdc': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
            },
            'sepolia': {
                'weth': '0xfff9976782d46cc05630d1f6ebab18b2324d6b14',
                'usdc': '0x94a9D9AC8a22534E3FaCa9F4e7F2E2cf85d5E4C8',
            },
        }
        self.contract_addresses = {
            'mainnet': {
                'router':           '0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506',
                'quoter':           '0xC35DADB65012eC5796536bD9864eD8773aBc74C4',
                'factory':          '0x1F98431c8aD98523631AE4a59f267346ea31F984',
                'red_snwapper':     '0xAC4c6e212A361c968F1725b4d055b47E63F80b75',
                'blade':            '0x655eDCE464CC797526600a462A8154650EEe4B77',
            }
        }



        self.abis_folder = os.path.join(tk.sushiswap_dapp_folder_path, 'abis')

        self.abis = {}
        
        
        with open(os.path.join(self.abis_folder, 'weth_abi.json')) as f:
            self.abis['weth'] = json.load(f)

        with open(os.path.join(self.abis_folder, 'usdc_abi.json')) as f:
            self.abis['usdc'] = json.load(f)

        with open(os.path.join(self.abis_folder, 'erc20Abi.json')) as f:
            self.abis['erc20'] = json.load(f)

        with open(os.path.join(self.abis_folder, 'sushiswap_quoter_abi.json')) as f:
            self.abis['quoter'] = json.load(f)

        with open(os.path.join(self.abis_folder, 'sushiswap_factory_abi.json')) as f:
            self.abis['sushiswap_factory_abi'] = json.load(f)

        with open(os.path.join(self.abis_folder, 'sushiswap_pool_abi.json')) as f:
            self.abis['sushiswap_pool_abi'] = json.load(f)

        with open(os.path.join(self.abis_folder, 'sushiswap_red_snwapper_abi.json')) as f:
            self.abis['red_snwapper'] = json.load(f)

        with open(os.path.join(self.abis_folder, 'sushiswap_blade_abi.json')) as f:
            self.abis['blade'] = json.load(f)



        self.max_gas_fee_multiplier = 1.5
        self.gas_custom_token_limit = 160_000


        """
        0.01% : 0.0001 : 100   / 1_000_000
        0.05% : 0.0005 : 500   / 1_000_000
        0.30% : 0.0030 : 3000  / 1_000_000
        1.00% : 0.0100 : 10000 / 1_000_000
        """


                
        self.weth = Token(name='weth', network=self.network, address=self.token_addresses[self.network]['weth'], decimals=18, fee_tiers = 500,
                          abi=self.abis['weth'], w3=self.w3)
                        
        self.usdc = Token(name='usdc', network=self.network, address=self.token_addresses[self.network]['usdc'], decimals=6, fee_tiers = 500,
                          abi=self.abis['erc20'], w3=self.w3)


        self.red_snwapper           = Contract(name='red_snwapper',         dapp=self)
        self.blade                  = Contract(name='blade',                dapp=self)

        tk.logger.info("sushiswap fully initiated")













    # def v3_quote(self, token_in_name, token_out_name, amount_in, fee):
    #     """
    #     quoteExactInputSingle

    #     tokenIn	:	The token being swapped in
    #     tokenOut	:	The token being swapped out
    #     fee	:	The fee of the token pool to consider for the pair
    #     amountIn	:	The desired input amount
    #     sqrtPriceLimitX96	:	The price limit of the pool that cannot be exceeded by the swap

    #     returns: amountOut:	The amount of tokenOut that would be received
    #     """
    #     tk.logger.info(f'performing V3 Quote')

    #     token_in = self.get_token_object(token_in_name)
    #     token_out = self.get_token_object(token_out_name)

    #     amountIn = int(amount_in * pow(10, token_in.decimals))

    #     sqrtPriceLimitX96 = 0

    #     quote = self.sushiswap_quoter.functions.quoteExactInputSingle(
    #         token_in.address,
    #         token_out.address,
    #         fee,
    #         amountIn,
    #         sqrtPriceLimitX96
    #     ).call()

    #     quote =  quote / pow(10, token_out.decimals)
    #     tk.logger.info(f'quote: {quote}')

    #     return quote



    # def create_new_quote_and_save_to_db(
    #         self,
    #         fiat_to_coin=True,
    #         fiat_amount_in=0.0,
    #         coin_amount_in=0.0,
    #         calls=3,
    #         fee=500
    #     ):

    #     admin_settings = tk.get_admin_settings()

    #     def trim_slippage(slippage, safty_margin):


    #         slippage_to_fee = int(slippage * 1_000_000) / fee
    #         slippage_to_fee = max(slippage_to_fee, 1.0)
    #         slippage_to_fee = min(slippage_to_fee, 5.0)

    #         slippage_to_fee += safty_margin

    #         return round(slippage_to_fee, 4)



    #     if fiat_to_coin:

    #         quoted_coin_amounts = []
            
    #         for i in range(calls):
    #             quoted_coin_amounts.append(
    #                 self.v3_quote(
    #                     token_in_name=admin_settings.fiat_coin,
    #                     token_out_name='weth',
    #                     amount_in=fiat_amount_in,
    #                     fee=fee,
    #                 )
    #             )

    #         quoted_coin_amount = min(quoted_coin_amounts)

    #         expected_coin_amount = fiat_amount_in / admin_settings.prices['weth']

    #         slippage = (expected_coin_amount - quoted_coin_amount) / expected_coin_amount

    #         slippage_to_fee = trim_slippage(slippage, 0.3)
    #         admin_settings.added_slippage_multiplier_fiat_to_coin = slippage_to_fee
    #         admin_settings.save()
    #         tk.logger.info(f"slippage_to_fee: {slippage}")
    #         tk.send_message_to_frontend_dashboard(topic="display_toaster", payload={'message': f"Slippage fiat to coin: {slippage_to_fee}"})

    #     else:


    #         quoted_fiat_amounts = []
            
    #         for i in range(calls):
    #             quoted_fiat_amounts.append(
    #                 self.v3_quote(
    #                     token_in_name='weth',
    #                     token_out_name=admin_settings.fiat_coin,
    #                     amount_in=coin_amount_in,
    #                     fee=fee,
    #                 )
    #             )

    #         quoted_fiat_amount = min(quoted_fiat_amounts)
    #         expected_fiat_amount = coin_amount_in * admin_settings.prices['weth']
    #         slippage = (expected_fiat_amount - quoted_fiat_amount) / expected_fiat_amount

    #         slippage_to_fee = trim_slippage(slippage, 0.15)
    #         admin_settings.added_slippage_multiplier_coin_to_fiat = slippage_to_fee
    #         admin_settings.save()

    #         tk.logger.info(f"slippage_to_fee: {slippage}")
    #         tk.send_message_to_frontend_dashboard(topic="display_toaster", payload={'message': f"Slippage coin to fiat: {slippage_to_fee}"})
















    def approve_spenders(self):
        # dai

        # self.approve(spender=uniswap_contract_addresses['SwapRouter'], token=self.dai)

        # weth DONE
        # self.approve(spender=uniswap_contract_addresses['SwapRouter'], token=self.weth)

        # wbtc
        # self.approve(spender=uniswap.wbtc_exchange_address, token=uniswap.wbtc)
        # self.approve(spender=uniswap_contract_addresses['SwapRouter'], token=self.wbtc)
        
        # wsol
        # self.approve(spender=self.wsol_exchange_address, token=self.wsol)
        
        # usdt
        # self.approve(spender=uniswap_contract_addresses['SwapRouter'], token=self.usdt)

        self.approve(spender=self.red_snwapper.address, token=self.usdc)
        self.approve(spender=self.red_snwapper.address, token=self.weth)
        pass










    # COMPLETE
    def fiat_to_token(self, fiat_amount, token, tries, transaction_object):

        # self.approve_spenders()
        """
        V3:
            fiat -> weth -> token
        """

        admin_settings = tk.get_admin_settings()
        fiat_coin = self.get_token_object(admin_settings.fiat_coin)


        for i in range(tries):

            tk.logger.info(f'performing fiat_to_token ({fiat_coin.name} -> {token})     fiat_amount: {fiat_amount}     V3')

            tx_fee = 0

            weth_price = admin_settings.prices['weth']

            weth_to_buy = fiat_amount / weth_price

            got_weth, weth_bought, tx_hash, tx_fee_in_eth = self.swap(
                                            token_in=fiat_coin,
                                            token_out=self.weth,
                                            amount_in=fiat_amount,
                                            amount_out=weth_to_buy,
                                            transaction_object=transaction_object,
                                        )


            if got_weth:

                tk.logger.info(f'V3: got_weth: {weth_bought}')
                
                tx_fee += tx_fee_in_eth * weth_price

                if token.lower() == 'weth':
                    # we are done
                    return got_weth, weth_bought, tx_hash, weth_price, tx_fee
                
                else:

                    token_price = self.get_coin_price(token)
                    weth_price = self.get_coin_price('eth')

                    token_to_buy = weth_bought * weth_price / token_price

                    got_token, token_bought, tx_hash, tx_fee_in_eth = self.swap(
                                                    token_in=self.weth,
                                                    token_out=self.get_token_object(token),
                                                    amount_in=weth_bought,
                                                    amount_out=token_to_buy,
                                                    transaction_object=transaction_object,
                                                )


                    if got_token:
                        tk.logger.info(f'got_token: {token_bought} of {token}')

                        tx_fee += tx_fee_in_eth * weth_price

                        return got_token, token_bought, tx_hash, token_price, tx_fee


        return False, None, None, None, None












    # COMPLETE
    def token_to_fiat(self, token_amount, token, tries, transaction_object):

        """
        V3:
            token -> weth -> fiat
        """
        admin_settings = tk.get_admin_settings()
        fiat_coin = self.get_token_object(admin_settings.fiat_coin)

        for i in range(tries):

            tk.logger.info(f'performing token_to_fiat: {token_amount} of {token} -> {fiat_coin.name}')

            tx_fee = 0

            weth_price = self.get_coin_price('eth')

            if token.lower() == 'weth':
                token_price = weth_price

            else:
                token_price = self.get_coin_price(token)


            # V3
            if token.lower() == 'weth':
                # no need to get weth
                got_weth = True
                weth_return = token_amount

            else:
                # firs we neet to swap token for weth
                weth_amount = token_amount * token_price / weth_price

                got_weth, weth_return, tx_hash, tx_fee_in_eth  = self.swap(
                                                    token_in=self.get_token_object(token),
                                                    token_out=self.weth,
                                                    amount_in=token_amount,
                                                    amount_out=weth_amount,
                                                    transaction_object=transaction_object,
                                                )

                tx_fee += tx_fee_in_eth * weth_price

                # update the eth price
                weth_price = self.get_coin_price('eth')


            if got_weth:
                
                # weth -> fiat

                fiat_return = weth_return * weth_price

                tk.logger.info(f'V3 got_weth: {weth_return}')

                got_fiat, fiat_return, tx_hash, tx_fee_in_eth  = self.swap(
                                                    token_in=self.weth,
                                                    token_out=fiat_coin,
                                                    amount_in=weth_return,
                                                    amount_out=fiat_return,
                                                    transaction_object=transaction_object,
                                                )



                if got_fiat:
                    tx_fee += tx_fee_in_eth * weth_price
                    return got_fiat, fiat_return, tx_hash, token_price, tx_fee


        return False, None, None, None, None







































    def swap(self, token_in, token_out, amount_in, amount_out, transaction_object):
        try:

            """
            on side of the swap is always weth
            the other side of the swap defines, which fee tiers are to be used
            """
            if token_in.name == 'weth':
                fee_tier = token_out.fee_tiers
                fiat_to_coin = False
            else:
                fee_tier = token_in.fee_tiers
                fiat_to_coin = True

            action = self.snwap_action(fiat_to_coin, token_in, token_out, amount_in, amount_out, fee_tier)

            tx_return = self.build_and_execute_tx(action=action, transaction_object=transaction_object)

            successful = tx_return['successful']
            tx_hash = tx_return['tx_hash']
            tx_fee_in_eth = tx_return['tx_fee_in_eth']

            if successful:
                token_out_bought = tx_return['logs_results'][token_out.name]['amount']

                return successful, token_out_bought, tx_hash, tx_fee_in_eth

            return False, None, None, None

        except:
            tk.logger.info(format_exc())

            return False, None, None, None








    def snwap_action(self, fiat_to_coin, token_in, token_out, amount_in, amount_out, fee_tier):

        tk.logger.info(f"<-> swapping {amount_in} {token_in.name} for {amount_out} {token_out.name} -- fee_tier: {fee_tier}")

        amount_in = int(amount_in * pow(10, token_in.decimals))
        amount_out = int(amount_out * pow(10, token_out.decimals))

        deadline = int(time.time() + 3 * 60)  # 3 minutes

        # admin_settings = tk.get_admin_settings()

        # if fiat_to_coin:
        #     max_allowed_slippage = (admin_settings.added_slippage_multiplier_fiat_to_coin * fee_tier) / 1_000_000
        # else:
        #     max_allowed_slippage = (admin_settings.added_slippage_multiplier_coin_to_fiat * fee_tier) / 1_000_000
        
        max_allowed_slippage = (1.1 * fee_tier) / 1_000_000

        tokenIn = token_in.address
        tokenOut = token_out.address
        fee = int(fee_tier)
        recipient = self.w3.eth.default_account
        deadline = int(deadline)
        amountIn = int(amount_in)
        amountOutMinimum = int((1. - max_allowed_slippage) * amount_out)
        sqrtPriceLimitX96 = int(0)


        action = self.red_snwapper.contract.functions.snwap(
                tokenIn,
                amountIn,
                recipient,
                tokenOut,
                amountOutMinimum,
                self.w3.to_checksum_address("0x3B0AA7d38Bf3C103bf02d1De2E37568cBED3D6e8"),
                b''
            ) 
            

        return action


































