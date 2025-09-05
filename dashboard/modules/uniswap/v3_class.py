from web3 import Web3
import time
import json
import os

from traceback import format_exc

from dashboard.views_pages import toolkit as tk
import os

# UNISWAP
token_address = {
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
    'ropsten': {
        'weth': '0xc778417e063141139fce010982780140aa0cd5ab',
        'mkr': '0xa117d4635d4e04e81fa775e2803010166ada5506',
        'dai': '0xad6d458402f60fd3bd25163575031acdce07538d',
        'wbtc': '0xd992CdEA5B16EaF7681fe85b4d537Efb64a1B0F1',
        'usdc': '0x9c8FA1ee532f8Afe9F2E27f06FD836F3C9572f71',
    },
}
v3_addresses = {
    'UniswapV3Factory': '0x1F98431c8aD98523631AE4a59f267346ea31F984',
    'Multicall2': '0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696',
    'ProxyAdmin': '0xB753548F6E010e7e680BA186F9Ca1BdAB2E90cf2',
    'TickLens': '0xbfd8137f7d1516D3ea5cA83523914859ec47F573',
    'Quoter': '0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6',
    'SwapRouter': '0xE592427A0AEce92De3Edee1F18E0157C05861564',
    'SwapRouter02': '0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45',
    'NFTDescriptor': '0x42B24A95702b9986e82d421cC3568932790A48Ec',
    'NonfungibleTokenPositionDescriptor': '0x91ae842A5Ffd8d12023116943e72A606179294f3',
    'TransparentUpgradeableProxy': '0xEe6A57eC80ea46401049E92587E52f5Ec1c24785',
    'NonfungiblePositionManager': '0xC36442b4a4522E871399CD717aBDD847Ab11FE88',
    'V3Migrator': '0xA5644E29708357803b5A882D272c41cC0dF92B34',
    'UniswapV3Staker': '0xe34139463bA50bD61336E0c446Bd8C0867c6fE65',
}


v2_addresses = {
    'dai': '0x2a1530C4C41db0B0b2bB646CB5Eb1A67b7158667',
}

with open(os.path.join(tk.abi_folder_path, 'uniswap_quoter_abi.json')) as f:
    uniswap_quoter_abi = json.load(f)

with open(os.path.join(tk.abi_folder_path, 'erc20ABI.json')) as f:
    erc20_abi = json.load(f)

with open(os.path.join(tk.abi_folder_path, 'v3SwapRouterABI.json')) as f:
    v3_swap_router_abi = json.load(f)

with open(os.path.join(tk.abi_folder_path, 'weth_abi.json')) as f:
    weth_abi = json.load(f)

with open(os.path.join(tk.abi_folder_path, 'wbtc_abi.json')) as f:
    wbtc_abi = json.load(f)

with open(os.path.join(tk.abi_folder_path, 'wsol_abi.json')) as f:
    wsol_abi = json.load(f)

with open(os.path.join(tk.abi_folder_path, 'uniswap_quoter_abi.json')) as f:
    uniswap_quoter_abi = json.load(f)


uniswap_mainnet_factory_address = "0xc0a47dFe034B400B47bDaD5FecDa2621de6c4d95"
uniswap_ropsten_factory_address = "0x9c83dCE8CA20E9aAF9D3efc003b2ea62aBC08351"
uniswap_rinkeby_factory_address = "0xf5D915570BC477f9B8D6C0E980aA81757A3AaC36"
uniswap_kovan_factory_address = "0xD3E51Ef092B2845f10401a0159B2B96e8B6c3D30"
uniswap_gorli_factory_address = "0x6Ce570d02D73d4c384b46135E87f8C592A8c86dA"

uniswap_factory_abi = '[{"name":"NewExchange","inputs":[{"type":"address","name":"token","indexed":true},{"type":"address","name":"exchange","indexed":true}],"anonymous":false,"type":"event"},{"name":"initializeFactory","outputs":[],"inputs":[{"type":"address","name":"template"}],"constant":false,"payable":false,"type":"function","gas":35725},{"name":"createExchange","outputs":[{"type":"address","name":"out"}],"inputs":[{"type":"address","name":"token"}],"constant":false,"payable":false,"type":"function","gas":187911},{"name":"getExchange","outputs":[{"type":"address","name":"out"}],"inputs":[{"type":"address","name":"token"}],"constant":true,"payable":false,"type":"function","gas":715},{"name":"getToken","outputs":[{"type":"address","name":"out"}],"inputs":[{"type":"address","name":"exchange"}],"constant":true,"payable":false,"type":"function","gas":745},{"name":"getTokenWithId","outputs":[{"type":"address","name":"out"}],"inputs":[{"type":"uint256","name":"token_id"}],"constant":true,"payable":false,"type":"function","gas":736},{"name":"exchangeTemplate","outputs":[{"type":"address","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":633},{"name":"tokenCount","outputs":[{"type":"uint256","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":663}]'
uniswap_exchange_abi = '[{"name":"TokenPurchase","inputs":[{"type":"address","name":"buyer","indexed":true},{"type":"uint256","name":"eth_sold","indexed":true},{"type":"uint256","name":"tokens_bought","indexed":true}],"anonymous":false,"type":"event"},{"name":"EthPurchase","inputs":[{"type":"address","name":"buyer","indexed":true},{"type":"uint256","name":"tokens_sold","indexed":true},{"type":"uint256","name":"eth_bought","indexed":true}],"anonymous":false,"type":"event"},{"name":"AddLiquidity","inputs":[{"type":"address","name":"provider","indexed":true},{"type":"uint256","name":"eth_amount","indexed":true},{"type":"uint256","name":"token_amount","indexed":true}],"anonymous":false,"type":"event"},{"name":"RemoveLiquidity","inputs":[{"type":"address","name":"provider","indexed":true},{"type":"uint256","name":"eth_amount","indexed":true},{"type":"uint256","name":"token_amount","indexed":true}],"anonymous":false,"type":"event"},{"name":"Transfer","inputs":[{"type":"address","name":"_from","indexed":true},{"type":"address","name":"_to","indexed":true},{"type":"uint256","name":"_value","indexed":false}],"anonymous":false,"type":"event"},{"name":"Approval","inputs":[{"type":"address","name":"_owner","indexed":true},{"type":"address","name":"_spender","indexed":true},{"type":"uint256","name":"_value","indexed":false}],"anonymous":false,"type":"event"},{"name":"setup","outputs":[],"inputs":[{"type":"address","name":"token_addr"}],"constant":false,"payable":false,"type":"function","gas":175875},{"name":"addLiquidity","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"uint256","name":"min_liquidity"},{"type":"uint256","name":"max_tokens"},{"type":"uint256","name":"deadline"}],"constant":false,"payable":true,"type":"function","gas":82605},{"name":"removeLiquidity","outputs":[{"type":"uint256","name":"out"},{"type":"uint256","name":"out"}],"inputs":[{"type":"uint256","name":"amount"},{"type":"uint256","name":"min_eth"},{"type":"uint256","name":"min_tokens"},{"type":"uint256","name":"deadline"}],"constant":false,"payable":false,"type":"function","gas":116814},{"name":"__default__","outputs":[],"inputs":[],"constant":false,"payable":true,"type":"function"},{"name":"ethToTokenSwapInput","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"uint256","name":"min_tokens"},{"type":"uint256","name":"deadline"}],"constant":false,"payable":true,"type":"function","gas":12757},{"name":"ethToTokenTransferInput","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"uint256","name":"min_tokens"},{"type":"uint256","name":"deadline"},{"type":"address","name":"recipient"}],"constant":false,"payable":true,"type":"function","gas":12965},{"name":"ethToTokenSwapOutput","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"uint256","name":"tokens_bought"},{"type":"uint256","name":"deadline"}],"constant":false,"payable":true,"type":"function","gas":50455},{"name":"ethToTokenTransferOutput","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"uint256","name":"tokens_bought"},{"type":"uint256","name":"deadline"},{"type":"address","name":"recipient"}],"constant":false,"payable":true,"type":"function","gas":50663},{"name":"tokenToEthSwapInput","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"uint256","name":"tokens_sold"},{"type":"uint256","name":"min_eth"},{"type":"uint256","name":"deadline"}],"constant":false,"payable":false,"type":"function","gas":47503},{"name":"tokenToEthTransferInput","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"uint256","name":"tokens_sold"},{"type":"uint256","name":"min_eth"},{"type":"uint256","name":"deadline"},{"type":"address","name":"recipient"}],"constant":false,"payable":false,"type":"function","gas":47712},{"name":"tokenToEthSwapOutput","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"uint256","name":"eth_bought"},{"type":"uint256","name":"max_tokens"},{"type":"uint256","name":"deadline"}],"constant":false,"payable":false,"type":"function","gas":50175},{"name":"tokenToEthTransferOutput","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"uint256","name":"eth_bought"},{"type":"uint256","name":"max_tokens"},{"type":"uint256","name":"deadline"},{"type":"address","name":"recipient"}],"constant":false,"payable":false,"type":"function","gas":50384},{"name":"tokenToTokenSwapInput","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"uint256","name":"tokens_sold"},{"type":"uint256","name":"min_tokens_bought"},{"type":"uint256","name":"min_eth_bought"},{"type":"uint256","name":"deadline"},{"type":"address","name":"token_addr"}],"constant":false,"payable":false,"type":"function","gas":51007},{"name":"tokenToTokenTransferInput","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"uint256","name":"tokens_sold"},{"type":"uint256","name":"min_tokens_bought"},{"type":"uint256","name":"min_eth_bought"},{"type":"uint256","name":"deadline"},{"type":"address","name":"recipient"},{"type":"address","name":"token_addr"}],"constant":false,"payable":false,"type":"function","gas":51098},{"name":"tokenToTokenSwapOutput","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"uint256","name":"tokens_bought"},{"type":"uint256","name":"max_tokens_sold"},{"type":"uint256","name":"max_eth_sold"},{"type":"uint256","name":"deadline"},{"type":"address","name":"token_addr"}],"constant":false,"payable":false,"type":"function","gas":54928},{"name":"tokenToTokenTransferOutput","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"uint256","name":"tokens_bought"},{"type":"uint256","name":"max_tokens_sold"},{"type":"uint256","name":"max_eth_sold"},{"type":"uint256","name":"deadline"},{"type":"address","name":"recipient"},{"type":"address","name":"token_addr"}],"constant":false,"payable":false,"type":"function","gas":55019},{"name":"tokenToExchangeSwapInput","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"uint256","name":"tokens_sold"},{"type":"uint256","name":"min_tokens_bought"},{"type":"uint256","name":"min_eth_bought"},{"type":"uint256","name":"deadline"},{"type":"address","name":"exchange_addr"}],"constant":false,"payable":false,"type":"function","gas":49342},{"name":"tokenToExchangeTransferInput","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"uint256","name":"tokens_sold"},{"type":"uint256","name":"min_tokens_bought"},{"type":"uint256","name":"min_eth_bought"},{"type":"uint256","name":"deadline"},{"type":"address","name":"recipient"},{"type":"address","name":"exchange_addr"}],"constant":false,"payable":false,"type":"function","gas":49532},{"name":"tokenToExchangeSwapOutput","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"uint256","name":"tokens_bought"},{"type":"uint256","name":"max_tokens_sold"},{"type":"uint256","name":"max_eth_sold"},{"type":"uint256","name":"deadline"},{"type":"address","name":"exchange_addr"}],"constant":false,"payable":false,"type":"function","gas":53233},{"name":"tokenToExchangeTransferOutput","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"uint256","name":"tokens_bought"},{"type":"uint256","name":"max_tokens_sold"},{"type":"uint256","name":"max_eth_sold"},{"type":"uint256","name":"deadline"},{"type":"address","name":"recipient"},{"type":"address","name":"exchange_addr"}],"constant":false,"payable":false,"type":"function","gas":53423},{"name":"getEthToTokenInputPrice","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"uint256","name":"eth_sold"}],"constant":true,"payable":false,"type":"function","gas":5542},{"name":"getEthToTokenOutputPrice","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"uint256","name":"tokens_bought"}],"constant":true,"payable":false,"type":"function","gas":6872},{"name":"getTokenToEthInputPrice","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"uint256","name":"tokens_sold"}],"constant":true,"payable":false,"type":"function","gas":5637},{"name":"getTokenToEthOutputPrice","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"uint256","name":"eth_bought"}],"constant":true,"payable":false,"type":"function","gas":6897},{"name":"tokenAddress","outputs":[{"type":"address","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":1413},{"name":"factoryAddress","outputs":[{"type":"address","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":1443},{"name":"balanceOf","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"address","name":"_owner"}],"constant":true,"payable":false,"type":"function","gas":1645},{"name":"transfer","outputs":[{"type":"bool","name":"out"}],"inputs":[{"type":"address","name":"_to"},{"type":"uint256","name":"_value"}],"constant":false,"payable":false,"type":"function","gas":75034},{"name":"transferFrom","outputs":[{"type":"bool","name":"out"}],"inputs":[{"type":"address","name":"_from"},{"type":"address","name":"_to"},{"type":"uint256","name":"_value"}],"constant":false,"payable":false,"type":"function","gas":110907},{"name":"approve","outputs":[{"type":"bool","name":"out"}],"inputs":[{"type":"address","name":"_spender"},{"type":"uint256","name":"_value"}],"constant":false,"payable":false,"type":"function","gas":38769},{"name":"allowance","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"address","name":"_owner"},{"type":"address","name":"_spender"}],"constant":true,"payable":false,"type":"function","gas":1925},{"name":"name","outputs":[{"type":"bytes32","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":1623},{"name":"symbol","outputs":[{"type":"bytes32","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":1653},{"name":"decimals","outputs":[{"type":"uint256","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":1683},{"name":"totalSupply","outputs":[{"type":"uint256","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":1713}]'
uniswap_token_abi = '[{"name":"Transfer","inputs":[{"type":"address","name":"_from","indexed":true},{"type":"address","name":"_to","indexed":true},{"type":"uint256","name":"_value","indexed":false}],"anonymous":false,"type":"event"},{"name":"Approval","inputs":[{"type":"address","name":"_owner","indexed":true},{"type":"address","name":"_spender","indexed":true},{"type":"uint256","name":"_value","indexed":false}],"anonymous":false,"type":"event"},{"name":"__init__","outputs":[],"inputs":[{"type":"bytes32","name":"_name"},{"type":"bytes32","name":"_symbol"},{"type":"uint256","name":"_decimals"},{"type":"uint256","name":"_supply"}],"constant":false,"payable":false,"type":"constructor"},{"name":"deposit","outputs":[],"inputs":[],"constant":false,"payable":true,"type":"function","gas":74279},{"name":"withdraw","outputs":[{"type":"bool","name":"out"}],"inputs":[{"type":"uint256","name":"_value"}],"constant":false,"payable":false,"type":"function","gas":108706},{"name":"totalSupply","outputs":[{"type":"uint256","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":543},{"name":"balanceOf","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"address","name":"_owner"}],"constant":true,"payable":false,"type":"function","gas":745},{"name":"transfer","outputs":[{"type":"bool","name":"out"}],"inputs":[{"type":"address","name":"_to"},{"type":"uint256","name":"_value"}],"constant":false,"payable":false,"type":"function","gas":74698},{"name":"transferFrom","outputs":[{"type":"bool","name":"out"}],"inputs":[{"type":"address","name":"_from"},{"type":"address","name":"_to"},{"type":"uint256","name":"_value"}],"constant":false,"payable":false,"type":"function","gas":110600},{"name":"approve","outputs":[{"type":"bool","name":"out"}],"inputs":[{"type":"address","name":"_spender"},{"type":"uint256","name":"_value"}],"constant":false,"payable":false,"type":"function","gas":37888},{"name":"allowance","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"address","name":"_owner"},{"type":"address","name":"_spender"}],"constant":true,"payable":false,"type":"function","gas":1025},{"name":"name","outputs":[{"type":"bytes32","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":723},{"name":"symbol","outputs":[{"type":"bytes32","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":753},{"name":"decimals","outputs":[{"type":"uint256","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":783}]'




class CustomException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Token():
    def __init__(self, name, network, address, abi, decimals, fee_teirs, w3):
        self.name = name
        self.network = network
        self.w3 = w3
        self.address = self.w3.to_checksum_address(address)
        self.abi = abi
        self.contract = self.w3.eth.contract(abi=self.abi, address=self.address)
        self.decimals = decimals
        self.fee_teirs = fee_teirs




class Uniswap():
    def __init__(self, network='mainnet'):
        
        self.network = network
        
        self.mainnet_infura_url = f"https://{self.network}.infura.io/v3/3f440b85f4ab47{os.getenv('trader_mainnet_infura_url')}" 
        
        
        self.default_account_address = f"0x2Ac4E9192846BeC854{os.getenv('trader_default_account_address')}"

        self.account_private_key = f"702e0b04f43b0993ee2e33049953b8602{os.getenv('trader_account_private_key')}"


        self.max_gas_fee_multiplier = 1.5

        self.gas_limit = 22_000
        self.gas_custom_token_limit = 160_000


        """
        0.01% : 0.0001 : 100   / 1_000_000
        0.05% : 0.0005 : 500   / 1_000_000
        0.30% : 0.0030 : 3000  / 1_000_000
        1.00% : 0.0100 : 10000 / 1_000_000
        """

        tk.logger.info("initiating W3...")

        self.w3 = Web3(Web3.HTTPProvider(self.mainnet_infura_url))
        self.w3.eth.default_account = self.w3.to_checksum_address(self.default_account_address)

        

        
        self.weth = Token(name='weth', network=self.network, address=token_address[self.network]['weth'], decimals=18, fee_teirs = [500],
                          abi=weth_abi, w3=self.w3)
        
        self.wsol = Token(name='wsol', network=self.network, address=token_address[self.network]['wsol'], decimals=9, fee_teirs = [3000],
                          abi=erc20_abi, w3=self.w3)

        self.wbtc = Token(name='wbtc', network=self.network, address=token_address[self.network]['wbtc'], decimals=8, fee_teirs = [500, 3000],
                          abi=wbtc_abi, w3=self.w3)



        self.dai = Token(name='dai', network=self.network, address=token_address[self.network]['dai'], decimals=18, fee_teirs = [500],
                         abi=erc20_abi, w3=self.w3)

        self.usdc = Token(name='usdc', network=self.network, address=token_address[self.network]['usdc'], decimals=6, fee_teirs = [500],
                          abi=erc20_abi, w3=self.w3)

        self.usdt = Token(name='usdt', network=self.network, address=token_address[self.network]['usdt'], decimals=6, fee_teirs = [500],
                          abi=erc20_abi, w3=self.w3)



        # V3
        self.v3_swap_router_contract = self.w3.eth.contract(abi=v3_swap_router_abi,
                                                            address=self.w3.to_checksum_address(
                                                                v3_addresses['SwapRouter']))

        # V2
        # self.v2_factory_contract = self.w3.eth.contract(abi=json.loads(uniswap_factory_abi),
        #                                                 address=self.w3.to_checksum_address(
        #                                                     uniswap_mainnet_factory_address))

        # self.dai_exchange_address_v2 = self.v2_factory_contract.functions.getExchange(self.dai.address).call()
        # self.dai_exchange_contract = self.w3.eth.contract(abi=json.loads(uniswap_exchange_abi),
        #                                                   address=self.dai_exchange_address_v2)

        # self.wbtc_exchange_address = self.v2_factory_contract.functions.getExchange(self.wbtc.address).call()
        # self.wbtc_exchange_contract = self.w3.eth.contract(abi=json.loads(uniswap_exchange_abi),
        #                                                    address=self.wbtc_exchange_address)
        # Quoter
        self.uniswap_quoter = self.w3.eth.contract(
                abi=uniswap_quoter_abi,
                address=self.w3.to_checksum_address(v3_addresses['Quoter'])
            )

        tk.logger.info("uniswap fully initiated")


    def get_token_object(self, token_string) -> Token:
        
        if token_string.lower() in ['eth', 'weth']:
            return self.weth

        elif token_string.lower() == 'dai':
            return self.dai
        
        elif token_string.lower() == 'wbtc':
            return self.wbtc

        elif token_string.lower() == 'wsol':
            return self.wsol

        elif token_string.lower() == 'usdc':
            return self.usdc

        elif token_string.lower() == 'usdt':
            return self.usdt
        
        else:
            raise


    def get_coin_price(self, coin):
        admin_settings = tk.get_admin_settings()
        return admin_settings.prices[coin.lower()]


    def check_balance(self):
        tk.logger.info("check_balance...")

        return {
            'eth': self.eth_balance(),
            'weth': self.weth_balance(),
            'dai': self.dai_balance(),
            'wbtc': self.wbtc_balance(),
            'wsol': self.wsol_balance(),
            'usdc': self.usdc_balance(),
            'usdt': self.usdt_balance(),
        }

    def dai_balance(self):
        tk.logger.info("dai_balance...")
        return self.dai.contract.functions.balanceOf(self.w3.eth.default_account).call() / pow(10, self.dai.decimals)

    def usdc_balance(self):
        tk.logger.info("usdc_balance...")
        return self.usdc.contract.functions.balanceOf(self.w3.eth.default_account).call() / pow(10, self.usdc.decimals)

    def usdt_balance(self):
        tk.logger.info("usdt_balance...")
        return self.usdt.contract.functions.balanceOf(self.w3.eth.default_account).call() / pow(10, self.usdt.decimals)

    def eth_balance(self):
        tk.logger.info("eth_balance...")
        return self.w3.eth.get_balance(self.w3.eth.default_account) / pow(10, self.weth.decimals)

    def weth_balance(self):
        tk.logger.info("weth_balance...")
        return self.weth.contract.functions.balanceOf(self.w3.eth.default_account).call() / pow(10, self.weth.decimals)

    def wbtc_balance(self):
        tk.logger.info("wbtc_balance...")
        return self.wbtc.contract.functions.balanceOf(self.w3.eth.default_account).call() / pow(10, self.wbtc.decimals)

    def wsol_balance(self):
        tk.logger.info("wsol_balance...")
        return self.wsol.contract.functions.balanceOf(self.w3.eth.default_account).call() / pow(10, self.wsol.decimals)


    def get_network_gas_price(self):

        admin_settings = tk.get_admin_settings()

        full_gas_info = admin_settings.gas

        gas_price_gwei = full_gas_info['gas_basic_price'] + full_gas_info['FastGasPrice']

        return {
            'maxPriorityFeePerGas_gwei': full_gas_info['FastGasPrice'],
            'maxFeePerGas_gwei': self.max_gas_fee_multiplier * gas_price_gwei,
            'tx_fee_eth': gas_price_gwei * self.gas_custom_token_limit / (10 ** 9),
        }


    def approve_spenders(self):
        # dai
        # uniswap.approve(spender=uniswap.dai_exchange_address_v2, token=uniswap.dai)
        # uniswap.approve(spender=v3_addresses['SwapRouter'], token=uniswap.dai)

        # weth
        # uniswap.approve(spender=v3_addresses['SwapRouter'], token=uniswap.weth)

        # wbtc
        # uniswap.approve(spender=uniswap.wbtc_exchange_address, token=uniswap.wbtc)
        # uniswap.approve(spender=tk.v3_addresses['SwapRouter'], token=uniswap.wbtc)
        
        # wsol
        # uniswap.approve(spender=uniswap.wsol_exchange_address, token=uniswap.wsol)
        
        # usdt
        # self.approve(spender=v3_addresses['SwapRouter'], token=self.usdt)

        # usdc
        # self.approve(spender=v3_addresses['SwapRouter'], token=self.usdc)
        pass


    def approve(self, spender, token):

        action = token.contract.functions.approve(self.w3.to_checksum_address(spender), 2**256 - 1)

        self.build_and_execute_tx(action=action)




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





    def v3_quote(self, token_in_name, token_out_name, amount_in, fee):
        """
        quoteExactInputSingle

        tokenIn	:	The token being swapped in
        tokenOut	:	The token being swapped out
        fee	:	The fee of the token pool to consider for the pair
        amountIn	:	The desired input amount
        sqrtPriceLimitX96	:	The price limit of the pool that cannot be exceeded by the swap

        returns: amountOut:	The amount of tokenOut that would be received
        """
        tk.logger.info(f'performing V3 Quote')

        token_in = self.get_token_object(token_in_name)
        token_out = self.get_token_object(token_out_name)

        amountIn = int(amount_in * pow(10, token_in.decimals))

        sqrtPriceLimitX96 = 0

        quote = self.uniswap_quoter.functions.quoteExactInputSingle(
            token_in.address,
            token_out.address,
            fee,
            amountIn,
            sqrtPriceLimitX96
        ).call()

        quote =  quote / pow(10, token_out.decimals)
        tk.logger.info(f'quote: {quote}')

        return quote



    def create_new_quote_and_save_to_db(
            self,
            fiat_to_coin=True,
            fiat_amount_in=0.0,
            coin_amount_in=0.0,
            calls=2,
            fee=500
        ):

        admin_settings = tk.get_admin_settings()

        def trim_slipage(slipage, safty_margin):


            slipage_to_fee = int(slipage * 1_000_000) / fee
            slipage_to_fee = max(slipage_to_fee, 1.0)
            slipage_to_fee = min(slipage_to_fee, 5.0)

            slipage_to_fee += safty_margin

            return round(slipage_to_fee, 4)



        if fiat_to_coin:

            quoted_coin_amounts = []
            
            for i in range(calls):
                quoted_coin_amounts.append(
                    self.v3_quote(
                        token_in_name=admin_settings.fiat_coin,
                        token_out_name='weth',
                        amount_in=fiat_amount_in,
                        fee=fee,
                    )
                )

            quoted_coin_amount = min(quoted_coin_amounts)

            expected_coin_amount = fiat_amount_in / admin_settings.prices['weth']

            slipage = (expected_coin_amount - quoted_coin_amount) / expected_coin_amount

            slipage_to_fee = trim_slipage(slipage, 0.3)
            admin_settings.added_slipage_multiplier_fiat_to_coin = slipage_to_fee
            admin_settings.save()
            tk.logger.info(f"slipage_to_fee: {slipage}")

        else:


            quoted_fiat_amounts = []
            
            for i in range(calls):
                quoted_fiat_amounts.append(
                    self.v3_quote(
                        token_in_name='weth',
                        token_out_name=admin_settings.fiat_coin,
                        amount_in=coin_amount_in,
                        fee=fee,
                    )
                )

            quoted_fiat_amount = min(quoted_fiat_amounts)
            expected_fiat_amount = coin_amount_in * admin_settings.prices['weth']
            slipage = (expected_fiat_amount - quoted_fiat_amount) / expected_fiat_amount

            slipage_to_fee = trim_slipage(slipage, 0.1)
            admin_settings.added_slipage_multiplier_coin_to_fiat = slipage_to_fee
            admin_settings.save()

            tk.logger.info(f"slipage_to_fee: {slipage}")























    ##############################################################################
    # ETH WORKS


    # LAGACY
    def eth_to_dai(self, eth_amount, tries):

        for i in range(tries):
            tk.logger.info(f'performing eth_to_dai     eth_amount: {eth_amount}     V3')

            eth_price = self.get_coin_price('eth')

            dai_return = eth_amount * eth_price

            # V3 eth -> weth -> dai
            got_dai, dai_return, tx_hash, tx_fee_in_eth, version  = self.swap(
                                                token_in=self.weth,
                                                token_out=self.dai,
                                                amount_in=eth_amount,
                                                amount_out=dai_return
                                            )

            tx_fee = tx_fee_in_eth * eth_price

            if got_dai:
                return got_dai, dai_return, tx_hash, eth_price, tx_fee, version

            # V2

            tk.logger.info(f'!!!!!!     performing eth_to_dai     eth_amount: {eth_amount}     V2')

            tk.logger.info(f'unwraping eth...')

            got_eth = self.unwrap_weth(eth_amount)

            if got_eth:
                got_dai, dai_bought, tx_hash, tx_fee_in_eth = self.v2_ethToTokenSwapInput(
                                                                        token_out=self.dai,
                                                                        eth_to_sell=eth_amount,
                                                                        token_amount_return=dai_return
                                                                    )
                if got_dai:
                    tx_fee = tx_fee_in_eth * eth_price
                    return got_dai, dai_bought, tx_hash, eth_price, tx_fee, 'V2'

        return False, None, None, None, None, None



    # COMPLETE
    def fiat_to_token(self, fiat_amount, token, tries):


        """
        V3:
            fiat -> weth -> token
        """
        # V3

        eth_price = self.get_coin_price('eth')

        weth_to_buy = fiat_amount / eth_price

        tx_fee = 0


        admin_settings = tk.get_admin_settings()
        fiat_coin = self.get_token_object(admin_settings.fiat_coin)

        tk.logger.info(f'performing fiat_to_token ({fiat_coin.name} -> {token})     fiat_amount: {fiat_amount}     V3')

        got_weth, weth_bought, tx_hash, tx_fee_in_eth, version = self.swap(
                                        token_in=fiat_coin,
                                        token_out=self.weth,
                                        amount_in=fiat_amount,
                                        amount_out=weth_to_buy
                                    )


        if got_weth:

            tk.logger.info(f'V3: got_weth: {weth_bought}')
            tx_fee += tx_fee_in_eth * eth_price
            if token.lower() == 'weth':
                # we are done
                return got_weth, weth_bought, tx_hash, eth_price, tx_fee, version
            
            else:

                token_price = self.get_coin_price(token)
                eth_price = self.get_coin_price('eth')

                token_to_buy = weth_bought * eth_price / token_price

                got_token, token_bought, tx_hash, tx_fee_in_eth, version = self.swap(
                                                token_in=self.weth,
                                                token_out=self.get_token_object(token),
                                                amount_in=weth_bought,
                                                amount_out=token_to_buy
                                            )


                if got_token:
                    tk.logger.info(f'got_token: {token_bought} of {token}')

                    tx_fee += tx_fee_in_eth * eth_price

                    return got_token, token_bought, tx_hash, token_price, tx_fee, version





        """
        V2:
            dai -> eth -> token
        """

        # # V2
        # tk.logger.info(f'!!!!!!  V2   performing fiat_to_token     fiat_amount: {fiat_amount}     V2')

        # if got_weth:
        #     # V3 has got weth already so no need for V2 to buy eth
        #     tk.logger.info('V3 got_weth but failed to buy token. so no need for V2 to buy eth.')
        #     tk.logger.info('V2 unwraps the weth and uses that to buy token')
        #     got_eth = self.unwrap_weth(weth_bought)
        #     eth_bought = weth_bought
        
        
        # else:
        #     got_eth, eth_bought, tx_hash, tx_fee_in_eth = self.v2_tokenToEthSwapInput(
        #                                                         self.dai,
        #                                                         token_in_amount=fiat_amount,
        #                                                         eth_to_buy=weth_to_buy
        #                                                     )
                                                            
        # if got_eth:
        #     tk.logger.info(f'V2: got_eth: {eth_bought}')

        #     tx_fee += tx_fee_in_eth * eth_price

        #     token_price = self.get_coin_price(token)
        #     token_amount = eth_bought * eth_price / token_price


        #     got_token, token_bought, tx_hash, tx_fee_in_eth = self.v2_ethToTokenSwapInput(
        #                                                             token_out=self.get_token_object(token),
        #                                                             eth_to_sell=eth_bought,
        #                                                             token_amount_return=token_amount
        #                                                         )


        #     if got_token:
        #         tx_fee += tx_fee_in_eth * eth_price

        #         tk.logger.info(f'V2: got_token: {token_bought}')
        #         return got_token, token_bought, tx_hash, token_price, tx_fee, 'V2'




        return False, None, None, None, None, None


    # COMPLETE
    def token_to_fiat(self, token_amount, token, tries):

        """
        V3:
            token -> weth -> fiat
        """
        admin_settings = tk.get_admin_settings()
        fiat_coin = self.get_token_object(admin_settings.fiat_coin)


        tk.logger.info(f'performing token_to_fiat: {token_amount} of {token} -> {fiat_coin.name}')

        tx_fee = 0

        eth_price = self.get_coin_price('eth')

        if token.lower() == 'weth':
            token_price = eth_price

        else:
            token_price = self.get_coin_price(token)


        # V3
        if token.lower() == 'weth':
            # no need to get weth
            got_weth = True
            weth_return = token_amount

        else:
            # firs we neet to swap token for weth
            weth_amount = token_amount * token_price / eth_price

            got_weth, weth_return, tx_hash, tx_fee_in_eth, version  = self.swap(
                                                token_in=self.get_token_object(token),
                                                token_out=self.weth,
                                                amount_in=token_amount,
                                                amount_out=weth_amount
                                            )

            tx_fee += tx_fee_in_eth * eth_price

            # update the eth price
            eth_price = self.get_coin_price('eth')


        if got_weth:
            
            # weth -> fiat

            fiat_return = weth_return * eth_price

            tk.logger.info(f'V3 got_weth: {weth_return}')

            got_fiat, fiat_return, tx_hash, tx_fee_in_eth, version  = self.swap(
                                                token_in=self.weth,
                                                token_out=fiat_coin,
                                                amount_in=weth_return,
                                                amount_out=fiat_return
                                            )

            tx_fee += tx_fee_in_eth * eth_price


            if got_fiat:
                return got_fiat, fiat_return, tx_hash, token_price, tx_fee, version


        # V2

        """
        V2:
            token -> eth -> dai

            if token is eth:
                unwrap eth
                eth -> dai
            
            else:
                token -> eth
                eth -> dai




        """

        # token_price = self.get_coin_price(token)
        # eth_price = self.get_coin_price('eth')

        # weth_to_buy = token_amount * token_price / eth_price


        # if token.lower == 'weth':
        #     got_weth = True
        #     weth_amount = weth_to_buy

        # else:
        #     # token -> eth

        #     got_weth, weth_amount, tx_hash, tx_fee_in_eth = self.v2_tokenToEthSwapInput(
        #                                         self.get_token_object(token),
        #                                         token_in_amount=token_amount,
        #                                         eth_to_buy=weth_to_buy
        #                                     )


        # if got_weth:

        #     # now we have weth

        #     tk.logger.info(f'!!!!!!     performing eth_to_dai     weth_amount: {weth_amount}     V2')

        #     tk.logger.info(f'unwraping eth...')

        #     dai_return = weth_amount * eth_price

        #     got_eth = self.unwrap_weth(weth_amount)

        #     if got_eth:
        #         got_dai, dai_bought, tx_hash, tx_fee_in_eth = self.v2_ethToTokenSwapInput(
        #                                                                 token_out=self.dai,
        #                                                                 eth_to_sell=weth_amount,
        #                                                                 token_amount_return=dai_return
        #                                                             )
        #         if got_dai:
        #             tx_fee = tx_fee_in_eth * eth_price
        #             return got_dai, dai_bought, tx_hash, token_price, tx_fee, 'V2'

            



        return False, None, None, None, None, None






































    ########################################
    # V3


    def swap(self, token_in, token_out, amount_in, amount_out):
        try:

            """
            on side of the swap is always weth
            the other side of the swap defines, which fee teirs are to be used
            """
            if token_in.name == 'weth':
                fee_teirs = token_out.fee_teirs
                fiat_to_coin = False
            else:
                fee_teirs = token_in.fee_teirs
                fiat_to_coin = True


            for fee_teir in fee_teirs:

                action = self.exactInputSingle(fiat_to_coin, token_in, token_out, amount_in, amount_out, fee_teir)

                tx_return = self.build_and_execute_tx(action=action)

                successful = tx_return['successful']
                tx_hash = tx_return['tx_hash']
                tx_fee_in_eth = tx_return['tx_fee_in_eth']

                if successful:
                    token_out_bought = tx_return['logs_results'][token_out.name]['amount']

                    return successful, token_out_bought, tx_hash, tx_fee_in_eth, f"V3({fee_teir})"

            return False, None, None, None, None

        except:
            tk.logger.info(format_exc())

            return False, None, None, None, None








    def exactInputSingle(self, fiat_to_coin, token_in, token_out, amount_in, amount_out, fee_teir):

        tk.logger.info(f"<-> swapping {amount_in} {token_in.name} for {amount_out} {token_out.name} -- fee_teir: {fee_teir}")

        amount_in = int(amount_in * pow(10, token_in.decimals))
        amount_out = int(amount_out * pow(10, token_out.decimals))

        deadline = int(time.time() + 300)  # 5 minutes

        admin_settings = tk.get_admin_settings()

        if fiat_to_coin:
            max_allowed_slipage = (admin_settings.added_slipage_multiplier_fiat_to_coin * fee_teir) / 1_000_000
        else:
            max_allowed_slipage = (admin_settings.added_slipage_multiplier_coin_to_fiat * fee_teir) / 1_000_000

        tokenIn = token_in.address
        tokenOut = token_out.address
        fee = int(fee_teir)
        recipient = self.w3.eth.default_account
        deadline = int(deadline)
        amountIn = int(amount_in)
        amountOutMinimum = int((1. - max_allowed_slipage) * amount_out)
        sqrtPriceLimitX96 = int(0)

        action = self.v3_swap_router_contract.functions.exactInputSingle((tokenIn,
                                                                          tokenOut,
                                                                          fee,
                                                                          recipient,
                                                                          deadline,
                                                                          amountIn,
                                                                          amountOutMinimum,
                                                                          sqrtPriceLimitX96))

        return action



















    ########################################
    # V2


    def v2_ethToTokenSwapInput(self, token_out, eth_to_sell, token_amount_return):
        try:
            tk.logger.info(f"<-> V2 sell {eth_to_sell} eth for {token_amount_return} {token_out.name}")

            eth_to_sell = int(eth_to_sell * pow(10, self.weth.decimals))
            min_tokens = int((1 - 0.0031) * token_amount_return * pow(10, token_out.decimals))
            deadline = int(time.time() + 300)  # 5 minutes

            if token_out.name == 'dai':
                action = self.dai_exchange_contract.functions.ethToTokenSwapInput(min_tokens, deadline)

            else:
                return False, None, None, None

            tx_return = self.build_and_execute_tx(action=action, value=eth_to_sell)

            successful = tx_return['successful']
            tx_hash = tx_return['tx_hash']
            tx_fee_in_eth = tx_return['tx_fee_in_eth']

            if successful:
                token_bought = tx_return['logs_results'][token_out.name]['amount']

                return successful, token_bought, tx_hash, tx_fee_in_eth

            return False, None, None, None

        except:
            tk.logger.info(format_exc())

            return False, None, None, None

    def v2_tokenToEthSwapInput(self, token_in, token_in_amount, eth_to_buy):
        try:
            tk.logger.info(f"<-> V2 buy {eth_to_buy} eth for {token_in_amount} {token_in.name}")

            eth_to_buy = int(eth_to_buy * pow(10, self.weth.decimals))
            token_in_amount = int(token_in_amount * pow(10, token_in.decimals))

            tokens_sold = token_in_amount
            min_eth = int((1 - 0.0031) * eth_to_buy)  # minimum eth bought
            deadline = int(time.time() + 300)  # 5 minutes

            if token_in.name == 'dai':
                action = self.dai_exchange_contract.functions.tokenToEthSwapInput(tokens_sold, min_eth, deadline)
            else:
                return False, None, None, None

            tx_return = self.build_and_execute_tx(action=action)
            
            successful = tx_return['successful']
            tx_hash = tx_return['tx_hash']
            tx_fee_in_eth = tx_return['tx_fee_in_eth']

            if successful:

                eth_bought = tx_return['logs_results']['eth']['amount']

                return successful, eth_bought, tx_hash, tx_fee_in_eth

            return False, None, None, None
        except:
            tk.logger.info(format_exc())

            return False, None, None, None






















    def build_and_execute_tx(self, action, value=0):

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

            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)


            tk.logger.info(
                f'waiting for https://{"" if self.network == "mainnet" else self.network + "."}etherscan.io/tx/{self.w3.to_hex(tx_hash)} \n')

            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)


        except:
            tk.logger.info(format_exc())

        finally:
            return self.process_receipt(receipt)



    def process_log(self, log):
        log_token = None
        for token in token_address['mainnet']:
            if token_address['mainnet'][token].lower() == log.address.lower():
                log_token = token
                break
        
        if log_token is None:
            for token in v2_addresses:
                if v2_addresses[token].lower() == log.address.lower():
                    if token == 'dai':
                        log_token = 'eth'
                        amount = self.w3.to_int(log['topics'][-1])
                        return 'eth', self.w3.to_int(log['topics'][-1]) / (10 ** 18)


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


            for idx, log in enumerate(receipt.logs):
                token_name, token_amount = self.process_log(log)
                logs_results[f"{token_name}"] = {"idx": idx, "amount": token_amount}


            return {
                'successful': successful,
                'tx_hash': tx_hash,
                'tx_fee_in_eth': tx_fee_in_eth,
                'logs_results': logs_results,
            }