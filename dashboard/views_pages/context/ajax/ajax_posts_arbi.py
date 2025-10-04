from dashboard.views_pages import transaction_dispatch   


def handle_ajax_posts_arbi(req, payload):
    pass


    if  req == 'arbi_balance':
        transaction = transaction_dispatch.create_and_actualize_arbi_balance_transaction()

    elif  req == 'arbi_deposit':
        transaction = transaction_dispatch.create_and_actualize_arbi_deposit_transaction()

    elif  req == 'arbi_withdraw':
        transaction = transaction_dispatch.create_and_actualize_arbi_withdraw_transaction()

    elif  req == 'arbi_action_2':
        fiat_loan_amount = eval(payload['fiat_loan_amount'])
        transaction = transaction_dispatch.create_and_actualize_arbi_action_2_transaction(fiat_loan_amount=fiat_loan_amount)

    elif  req == 'arbi_approve':
        transaction = transaction_dispatch.create_and_actualize_arbi_approve_transaction()

    elif  req == 'arbi_allowance':
        transaction = transaction_dispatch.create_and_actualize_arbi_allowance_transaction()


    elif  req == 'arbi_wrap_eth':
        amount = eval(payload['amount'])
        transaction = transaction_dispatch.create_and_actualize_arbi_wrap_eth(amount)


    elif  req == 'arbi_unwrap_weth':
        amount = eval(payload['amount'])
        transaction = transaction_dispatch.create_and_actualize_arbi_unwrap_weth(amount)

    elif  req == 'arbi_single_swap':
        transaction = transaction_dispatch.create_and_actualize_arbi_single_swap()


