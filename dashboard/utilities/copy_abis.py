import json

dex_abi_source                  = 'C:\\Users\\user\\Desktop\\flash_loan\\artifacts\\contracts\\Dex.sol\\Dex.json'
flash_loan_arbitrage_abi_source = 'C:\\Users\\user\\Desktop\\flash_loan\\artifacts\\contracts\\FlashLoanArbitrage.sol\\FlashLoanArbitrage.json'
arbitrage_abi_source            = 'C:\\Users\\user\\Desktop\\flash_loan\\artifacts\\contracts\\Arbitrage.sol\\Arbitrage.json'
single_swap_abi_source          = 'C:\\Users\\user\\Desktop\\flash_loan\\artifacts\\contracts\\SingleSwap.sol\\SingleSwap.json'

dex_abi_target                  = 'C:\\Users\\user\\Desktop\\trade\\dashboard\\modules\\dapps\\arbi\\abis\\dex.json'
flash_loan_arbitrage_abi_target = 'C:\\Users\\user\\Desktop\\trade\\dashboard\\modules\\dapps\\arbi\\abis\\flash_loan_arbitrage.json'
arbitrage_abi_target            = 'C:\\Users\\user\\Desktop\\trade\\dashboard\\modules\\dapps\\arbi\\abis\\arbitrage.json'
single_swap_abi_target          = 'C:\\Users\\user\\Desktop\\trade\\dashboard\\modules\\dapps\\arbi\\abis\\single_swap.json'


def copy_abi(source, target):
    with open(source, 'r') as f:
        source = json.load(f)['abi']


    with open(target, 'w') as f:
        json.dump(source, f, indent=4)
        

copy_abi(dex_abi_source,                        dex_abi_target)
copy_abi(flash_loan_arbitrage_abi_source,       flash_loan_arbitrage_abi_target)
copy_abi(arbitrage_abi_source,                  arbitrage_abi_target)
copy_abi(single_swap_abi_source,                single_swap_abi_target)


