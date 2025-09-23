import json
from dashboard.views_pages import toolkit as tk
from django.http import HttpResponse
from .context import context_class

from dashboard.models import models_position,  models_transaction, models_order

from dashboard.views_pages import transaction_dispatch    
                
def get_response(request):

    context = context_class.context_class(request, template='dashboard/manual.html')

    if request.method == "POST":
        if 'req' in request.POST:
            ret = context.handle_ajax_post(request)

            return HttpResponse(json.dumps(ret), content_type='application/json')


        else:

            if 'uniswap_approve' in request.POST:
                transaction = transaction_dispatch.create_and_actualize_uniswap_approve_transaction()


            elif 'fiat_to_token_amount' in request.POST:
                fiat_to_token_amount = eval(request.POST['fiat_to_token_amount'])
                coin = request.POST['coin']
                transaction = transaction_dispatch.create_and_actualize_uniswap_fiat_to_token_transaction(fiat_to_token_amount, coin=coin)
                


            elif 'token_to_fiat_amount' in request.POST:
                token_to_fiat_amount = eval(request.POST['token_to_fiat_amount'])
                coin = request.POST['coin']
                transaction = transaction_dispatch.create_and_actualize_uniswap_token_to_fiat_transaction(token_to_fiat_amount, coin=coin)


            elif 'eth_amount_to_wrap' in request.POST:
                eth_amount_to_wrap = eval(request.POST['eth_amount_to_wrap'])
                transaction = transaction_dispatch.create_and_actualize_uniswap_wrap_eth(eth_amount_to_wrap)

            elif 'weth_amount_to_unwrap' in request.POST:
                weth_amount_to_unwrap = eval(request.POST['weth_amount_to_unwrap'])
                transaction = transaction_dispatch.create_and_actualize_uniswap_unwrap_weth(weth_amount_to_unwrap)





            elif 'aave_approve' in request.POST:
                transaction = transaction_dispatch.create_and_actualize_aave_approve_transaction()


            elif 'aave_supply_amount' in request.POST:
                amount = eval(request.POST['aave_supply_amount'])
                transaction = transaction_dispatch.create_and_actualize_aave_supply_transaction(amount)

            elif 'aave_withdraw_amount' in request.POST:
                amount = eval(request.POST['aave_withdraw_amount'])
                transaction = transaction_dispatch.create_and_actualize_aave_withdraw_transaction(amount)


            elif 'aave_borrow_amount' in request.POST:
                amount = eval(request.POST['aave_borrow_amount'])
                transaction = transaction_dispatch.create_and_actualize_aave_borrow_transaction(amount)


            elif 'aave_repay_amount' in request.POST:
                amount = eval(request.POST['aave_repay_amount'])
                transaction = transaction_dispatch.create_and_actualize_aave_repay_transaction(amount)








            tk.create_new_notification(title="Manual operation completed", message=f'tx name: {transaction.transaction_type} ({transaction.name}), state: {transaction.state}, fee: {transaction.fee}')




    context.dict['admin_settings'] =  tk.get_admin_settings()
    context.dict['positions'] =  models_position.Position.objects.all().order_by('-id')
    context.dict['orders'] =  models_order.Order.objects.filter(executed=False).order_by('-id')

    context.dict['new_random_name'] =  tk.get_new_random_name()
    context.dict['coins'] =  models_transaction.coins
    context.dict['fiat_coins'] =  models_transaction.fiat_coins
    context.dict['auto_exit_styles'] =  models_order.auto_exit_styles
    context.dict['entry_conditions'] =  models_order.entry_conditions


    return context.response()

