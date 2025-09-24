import json

dex_abi_source = 'C:\\Users\\user\\Desktop\\flash_loan\\artifacts\\contracts\\Dex.sol\\Dex.json'
dex_abi_target = 'C:\\Users\\user\\Desktop\\trade\\dashboard\\modules\\dapps\\arbi\\abis\\dex.json'

dex_abi_source = 'C:\\Users\\user\\Desktop\\flash_loan\\artifacts\\contracts\\FlashLoanArbitrage.sol\\FlashLoanArbitrage.json'
dex_abi_target = 'C:\\Users\\user\\Desktop\\trade\\dashboard\\modules\\dapps\\arbi\\abis\\flash_loan_arbitrage.json'


def copy_abi(source, target):
    with open(source, 'r') as f:
        source = json.load(f)['abi']


    with open(target, 'w') as f:
        json.dump(source, f, indent=4)
        

copy_abi(dex_abi_source, dex_abi_target)
copy_abi(dex_abi_source, dex_abi_target)


