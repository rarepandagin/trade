import json
from dashboard.views_pages import toolkit as tk
from dashboard.models import models_position
from dashboard.models import models_order
from dashboard.models import models_transaction
from traceback import format_exc
from dashboard.views_pages import transaction_dispatch    

def handle_ajax_posts(self, request):

    payload = json.loads(request.POST['payload'])

    if request.POST['req'] == 'display_position_on_chart':

        position_uuid = payload['position_uuid']

        position = models_position.Position.objects.get(uuid=position_uuid)


        if position.display_on_chart:
            position.display_on_chart=False
        else:
            position.display_on_chart=True

        position.save()




    elif request.POST['req'] == 'update_balances':
        from dashboard.modules.dapps.uniswap.uniswap_class import Uniswap

        try:
            tk.send_message_to_frontend_dashboard(topic='display_toaster', payload={'message': f'starting update_balances', 'color': 'green'})

            uniswap = Uniswap()


            balances = uniswap.check_balance()
            admin_settings = tk.get_admin_settings()
            admin_settings.balances = balances
            admin_settings.save()

            tk.send_message_to_frontend_dashboard(topic='display_toaster', payload={'message': f'finished update_balances', 'color': 'green'})

        except:
            tk.logger.info(format_exc())


    elif  request.POST['req'] == 'update_both_way_quotes':
        from dashboard.modules.dapps.uniswap.uniswap_class import Uniswap

        uniswap = Uniswap()
        fiat_amount_in = payload['fiat_amount_in']
        uniswap.create_new_quote_and_save_to_db(fiat_to_coin=True, fiat_amount_in=fiat_amount_in)

        admin_settings = tk.get_admin_settings()

        coin_amount_in = payload['fiat_amount_in'] / admin_settings.prices['weth']
        uniswap.create_new_quote_and_save_to_db(fiat_to_coin=False, coin_amount_in=coin_amount_in)


    elif  request.POST['req'] == 'execute_order':
        # import time
        order = models_order.Order.objects.get(uuid=payload['order_uuid'])
        order.execute()
        # time.sleep(2)
        order.save()
        return {'req': request.POST['req'], 'success': order.fulfilled}



    elif  request.POST['req'] == 'exit_position':
        # import time
        position = models_position.Position.objects.get(uuid=payload['position_uuid'])
        position.exit_position()
        # time.sleep(2)
        position.save()

        return {'req': request.POST['req'], 'success': position.exited_gracefully}





    elif  request.POST['req'] in 'arbi_balance':
        transaction = transaction_dispatch.create_and_actualize_arbi_balance_transaction()
        tk.create_new_notification(title="Manual operation completed", message=f'tx name: {transaction.transaction_type} ({transaction.name}), state: {transaction.state}, fee: {transaction.fee}')

        return {'req': request.POST['req'], 'success': True}




    elif  request.POST['req'] in 'arbi_deposit':
        transaction = transaction_dispatch.create_and_actualize_arbi_deposit_transaction()
        tk.create_new_notification(title="Manual operation completed", message=f'tx name: {transaction.transaction_type} ({transaction.name}), state: {transaction.state}, fee: {transaction.fee}')

        return {'req': request.POST['req'], 'success': True}



    elif  request.POST['req'] in 'arbi_withdraw':
        transaction = transaction_dispatch.create_and_actualize_arbi_withdraw_transaction()
        tk.create_new_notification(title="Manual operation completed", message=f'tx name: {transaction.transaction_type} ({transaction.name}), state: {transaction.state}, fee: {transaction.fee}')

        return {'req': request.POST['req'], 'success': True}

    elif  request.POST['req'] in 'arbi_action_2':
        fiat_loan_amount = eval(payload['fiat_loan_amount'])
        transaction = transaction_dispatch.create_and_actualize_arbi_action_2_transaction(fiat_loan_amount=fiat_loan_amount)
        tk.create_new_notification(title="Manual operation completed", message=f'tx name: {transaction.transaction_type} ({transaction.name}), state: {transaction.state}, fee: {transaction.fee}')

        return {'req': request.POST['req'], 'success': True}

    elif  request.POST['req'] in 'arbi_approve':
        transaction = transaction_dispatch.create_and_actualize_arbi_approve_transaction()
        tk.create_new_notification(title="Manual operation completed", message=f'tx name: {transaction.transaction_type} ({transaction.name}), state: {transaction.state}, fee: {transaction.fee}')

        return {'req': request.POST['req'], 'success': True}

    elif  request.POST['req'] in 'arbi_allowance':
        transaction = transaction_dispatch.create_and_actualize_arbi_allowance_transaction()
        tk.create_new_notification(title="Manual operation completed", message=f'tx name: {transaction.transaction_type} ({transaction.name}), state: {transaction.state}, fee: {transaction.fee}')

        return {'req': request.POST['req'], 'success': True}




