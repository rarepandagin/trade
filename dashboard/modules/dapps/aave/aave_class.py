from dashboard.modules.dapps.dapp_class import *

# AAVE
aave_token_addresses = {
    'mainnet': {
        'dai': '0x6B175474E89094C44Da98b954EedeAC495271d0F',
        # 'eth': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
        'weth': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
        'usdc': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
        'wbtc': '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599',
    },

    'sepolia': {
        'dai': '0xFF34B3d4Aee8ddCd6F9AFFFB6Fe49bD371b8a357',
        # 'eth':  '0xC558DBdd856501FCd9aaF1E62eae57A9F0629a3c',
        'weth': '0xC558DBdd856501FCd9aaF1E62eae57A9F0629a3c',
        'usdc': '0x94a9D9AC8a22534E3FaCa9F4e7F2E2cf85d5E4C8',
        'wbtc': '0x29f2D40B0605204364af54EC677bD022dA425d03',
        'link': '0xf8Fb3713D459D7C1018BD0A49D19b4C44290EBE5',
    },
}

aave_contract_addresses = {
    'mainnet': {
        'pool': '0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2',
    },

    'sepolia': {
        'pool': '0x6Ae43d3271ff6888e7Fc43Fd7321a503ff738951',

    }
}

abis_folder = os.path.join(tk.aave_dapp_folder_path, 'abis')


with open(os.path.join(abis_folder, "aave_pool_abi.json")) as f:
    pool_abi = json.load(f)

with open(os.path.join(abis_folder, 'erc20ABI.json')) as f:
    erc20_abi = json.load(f)

with open(os.path.join(abis_folder, 'aave_weth_abi.json')) as f:
    weth_abi = json.load(f)

with open(os.path.join(abis_folder, 'aave_wbtc_abi.json')) as f:
    wbtc_abi = json.load(f)





class Aave(Dapp):
    def __init__(self):

        super().__init__()

        self.dapp_name = "aave"
        tk.logger.info(f"initiating {self.dapp_name} W3...")

        self.token_addresses = aave_token_addresses

        self.max_gas_fee_multiplier = 1.5
        self.gas_limit = 22_0000
        self.gas_custom_token_limit = 300_000


        
        # self.eth = Token(name='eth', network=self.network, address=aave_token_addresses[self.network]['eth'], decimals=18, fee_tiers = 500,
        #                   abi=erc20_abi, w3=self.w3)
                
        self.weth = Token(name='weth', network=self.network, address=aave_token_addresses[self.network]['weth'], decimals=18, fee_tiers = 500,
                          abi=weth_abi, w3=self.w3)
        
        self.dai = Token(name='dai', network=self.network, address=aave_token_addresses[self.network]['dai'], decimals=18, fee_tiers = 500,
                         abi=erc20_abi, w3=self.w3)

        self.usdc = Token(name='usdc', network=self.network, address=aave_token_addresses[self.network]['usdc'], decimals=6, fee_tiers = 500,
                          abi=erc20_abi, w3=self.w3)

        self.wbtc = Token(name='wbtc', network=self.network, address=aave_token_addresses[self.network]['wbtc'], decimals=8, fee_tiers = 500,
                          abi=wbtc_abi, w3=self.w3)



        self.pool_contract = self.w3.eth.contract(abi=pool_abi,
                                                            address=self.w3.to_checksum_address(
                                                                aave_contract_addresses[self.network]['pool']))









    def approve_spenders(self):
        # self.approve(spender=aave_contract_addresses[self.network]['pool'], token=self.eth)
        # self.approve(spender=aave_contract_addresses[self.network]['pool'], token=self.usdc)
        # self.approve(spender=aave_contract_addresses[self.network]['pool'], token=self.dai)
        self.approve(spender=aave_contract_addresses[self.network]['pool'], token=self.weth)
        # self.approve(spender=aave_contract_addresses[self.network]['pool'], token=self.wbtc)
        return True




    def supply(self, token:Token, amount):
        # amount_to_supply will be internally devided by 10 ** token.decimals
        # for example, for wbtc with decimal equal to 8, a supply amount of 10000
        # is 10000 / 10^18, which equals to 0.0001 bitcoin

        amount_by_token_decimal = int(amount * (10 ** token.decimals))

        action = self.pool_contract.functions.supply(
            token.address,
            amount_by_token_decimal,
            self.w3.to_checksum_address(self.default_account_address),
            0
        )
        tx_return = self.build_and_execute_tx(action=action)
        return tx_return


    def withdraw(self, token:Token, amount):
        
        amount_by_token_decimal = int(amount * (10 ** token.decimals))
        
        action = self.pool_contract.functions.withdraw(
            token.address,
            amount_by_token_decimal,
            self.w3.to_checksum_address(self.default_account_address)
        )
        tx_return = self.build_and_execute_tx(action=action)
        return tx_return


    def borrow(self, token:Token, amount):

        amount_by_token_decimal = int(amount * (10 ** token.decimals))
        
        action = self.pool_contract.functions.borrow(
            token.address,
            amount_by_token_decimal,
            2,
            0,
            self.w3.to_checksum_address(self.default_account_address)
        )
        tx_return = self.build_and_execute_tx(action=action)
        return tx_return


    def repay(self, token:Token, amount):

        amount_by_token_decimal = int(amount * (10 ** token.decimals))
        
        action = self.pool_contract.functions.repay(
            token.address,
            amount_by_token_decimal,
            2,
            self.w3.to_checksum_address(self.default_account_address)
        )
        tx_return = self.build_and_execute_tx(action=action)
        return tx_return



    def getUserAccountData(self):
        results = self.pool_contract.functions.getUserAccountData(
            self.w3.to_checksum_address(self.default_account_address)
        ).call()

        results = { 
            'totalCollateralBase' : results[0] / (10 ** 8),
            'totalDebtBase' : results[1] / (10 ** 8),
            'availableBorrowsBase' : results[2] / (10 ** 8),
            'currentLiquidationThreshold' : results[3] / (10 ** 4),
            'ltv' : results[4] / (10 ** 4),
            'healthFactor' : results[5] / (10 ** 18),
            }

        return results






if __name__ == "__main__":
    pass
    # aave = Aave(network='mainnet')  
    # tk.logger.info(aave.check_balance())

    # aave.wrap_eth(0.0005)
    # aave.unwrap_weth(0.002)

    # aave.approve_spenders()

    # tk.logger.info(aave.getUserAccountData())

    # aave.supply(
    #     token=aave.weth,
    #     amount=0.0001,
    #     onBehalfOf=aave.w3.to_checksum_address(aave.default_account_address),
    #     referralCode=0
    # )

    # aave.withdraw(
    #     token=aave.wbtc,
    #     amount=0.0001,
    #     address=aave.w3.to_checksum_address(aave.default_account_address)
    # )

    # aave.borrow(
    #     token=aave.wbtc,
    #     amount=0.003,
    #     address=aave.w3.to_checksum_address(aave.default_account_address)
    # )


    # aave.repay(
    #     token=aave.usdc,
    #     amount=1,
    #     address=aave.w3.to_checksum_address(aave.default_account_address)
    # )

    # tk.logger.info(aave.getUserAccountData())
