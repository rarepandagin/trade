

def perform_transaction_actualization(transaction):
    transaction.save()
    transaction.actualize()
    transaction.save()
    return transaction

    
# UNISWAP

def create_and_actualize_uniswap_approve_transaction():
    from dashboard.models import models_transaction

    transaction = models_transaction.Transaction(
        coin=models_transaction.weth,
        transaction_type=models_transaction.uniswap_approve,
        token_amount_spent=0,
    )

    return perform_transaction_actualization(transaction)



def create_and_actualize_uniswap_fiat_to_token_transaction(fiat_to_token_amount, coin):
    from dashboard.models import models_transaction

    transaction = models_transaction.Transaction(
        coin=coin,
        transaction_type=models_transaction.uniswap_fiat_to_token,
        fiat_amount_spent=fiat_to_token_amount,
    )

    return perform_transaction_actualization(transaction)


def create_and_actualize_uniswap_token_to_fiat_transaction(token_to_fiat_amount, coin):
    from dashboard.models import models_transaction

    transaction = models_transaction.Transaction(
        coin=coin,
        transaction_type=models_transaction.uniswap_token_to_fiat,
        token_amount_spent=token_to_fiat_amount,
    )

    return perform_transaction_actualization(transaction)



def create_and_actualize_uniswap_wrap_eth(eth_amount_to_wrap):
    from dashboard.models import models_transaction

    transaction = models_transaction.Transaction(
        coin=models_transaction.weth,
        transaction_type=models_transaction.uniswap_wrap_eth,
        token_amount_spent=eth_amount_to_wrap,
    )

    return perform_transaction_actualization(transaction)



def create_and_actualize_uniswap_unwrap_weth(eth_amount_to_wrap):
    from dashboard.models import models_transaction

    transaction = models_transaction.Transaction(
        coin=models_transaction.weth,
        transaction_type=models_transaction.uniswap_unwrap_weth,
        token_amount_spent=eth_amount_to_wrap,
    )

    return perform_transaction_actualization(transaction)





# AVEE

def create_and_actualize_aave_approve_transaction():
    from dashboard.models import models_transaction

    transaction = models_transaction.Transaction(
        coin=models_transaction.weth,
        transaction_type=models_transaction.aave_approve,
        token_amount_spent=0,
    )

    return perform_transaction_actualization(transaction)



def create_and_actualize_aave_supply_transaction(supply_amount):
    from dashboard.models import models_transaction

    transaction = models_transaction.Transaction(
        coin=models_transaction.weth,
        transaction_type=models_transaction.aave_supply,
        token_amount_spent=supply_amount,
    )

    return perform_transaction_actualization(transaction)




def create_and_actualize_aave_withdraw_transaction(withdraw_amount):
    from dashboard.models import models_transaction

    transaction = models_transaction.Transaction(
        coin=models_transaction.weth,
        transaction_type=models_transaction.aave_withdraw,
        token_amount_spent=withdraw_amount,
    )

    return perform_transaction_actualization(transaction)



def create_and_actualize_aave_borrow_transaction(borrow_amount):
    from dashboard.models import models_transaction

    transaction = models_transaction.Transaction(
        coin=models_transaction.weth,
        transaction_type=models_transaction.aave_borrow,
        token_amount_spent=borrow_amount,
    )

    return perform_transaction_actualization(transaction)



def create_and_actualize_aave_repay_transaction(repay_amount):
    from dashboard.models import models_transaction

    transaction = models_transaction.Transaction(
        coin=models_transaction.weth,
        transaction_type=models_transaction.aave_repay,
        token_amount_spent=repay_amount,
    )

    return perform_transaction_actualization(transaction)




# ARBI


def create_and_actualize_arbi_balance_transaction():
    from dashboard.models import models_transaction

    transaction = models_transaction.Transaction(
        coin=models_transaction.weth,
        transaction_type=models_transaction.arbi_balance,
    )

    return perform_transaction_actualization(transaction)



def create_and_actualize_arbi_action_2_transaction(fiat_loan_amount):
    from dashboard.models import models_transaction

    transaction = models_transaction.Transaction(
        coin=models_transaction.weth,
        transaction_type=models_transaction.arbi_action_2,
        fiat_loan_amount=fiat_loan_amount,
    )

    return perform_transaction_actualization(transaction)


def create_and_actualize_arbi_approve_transaction():
    from dashboard.models import models_transaction

    transaction = models_transaction.Transaction(
        coin=models_transaction.weth,
        transaction_type=models_transaction.arbi_approve,
    )

    return perform_transaction_actualization(transaction)


def create_and_actualize_arbi_allowance_transaction():
    from dashboard.models import models_transaction

    transaction = models_transaction.Transaction(
        coin=models_transaction.weth,
        transaction_type=models_transaction.arbi_allowance,
    )

    return perform_transaction_actualization(transaction)


def create_and_actualize_arbi_deposit_transaction():
    from dashboard.models import models_transaction

    transaction = models_transaction.Transaction(
        coin=models_transaction.weth,
        transaction_type=models_transaction.arbi_deposit,
    )

    return perform_transaction_actualization(transaction)


def create_and_actualize_arbi_withdraw_transaction():
    from dashboard.models import models_transaction

    transaction = models_transaction.Transaction(
        coin=models_transaction.weth,
        transaction_type=models_transaction.arbi_withdraw,
    )

    return perform_transaction_actualization(transaction)


def create_and_actualize_arbi_wrap_eth(eth_amount_to_wrap):
    from dashboard.models import models_transaction

    transaction = models_transaction.Transaction(
        coin=models_transaction.weth,
        transaction_type=models_transaction.arbi_wrap_eth,
        token_amount_spent=eth_amount_to_wrap,
    )

    return perform_transaction_actualization(transaction)



def create_and_actualize_arbi_unwrap_weth(eth_amount_to_wrap):
    from dashboard.models import models_transaction

    transaction = models_transaction.Transaction(
        coin=models_transaction.weth,
        transaction_type=models_transaction.arbi_unwrap_weth,
        token_amount_spent=eth_amount_to_wrap,
    )

    return perform_transaction_actualization(transaction)


def create_and_actualize_arbi_single_swap():
    from dashboard.models import models_transaction

    transaction = models_transaction.Transaction(
        coin=models_transaction.weth,
        transaction_type=models_transaction.arbi_single_swap,
    )

    return perform_transaction_actualization(transaction)






















def create_and_actualize_sushiswap_fiat_to_token_transaction(fiat_to_token_amount, coin):
    from dashboard.models import models_transaction

    transaction = models_transaction.Transaction(
        coin=coin,
        transaction_type=models_transaction.sushiswap_fiat_to_token,
        fiat_amount_spent=fiat_to_token_amount,
    )

    return perform_transaction_actualization(transaction)

