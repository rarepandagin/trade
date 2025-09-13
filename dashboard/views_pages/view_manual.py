import json
from dashboard.views_pages import toolkit as tk
from django.http import HttpResponse
from .context import context_class

from dashboard.models import models_position,  models_transaction, models_order

from mysite import settings    
                
def get_response(request):

    context = context_class.context_class(request, template='dashboard/manual.html')

    if request.method == "POST":
        if 'req' in request.POST:
            ret = context.handle_ajax_post(request)

            return HttpResponse(json.dumps(ret), content_type='application/json')


        else:

            if 'fiat_to_token_amount' in request.POST:
                fiat_to_token_amount = eval(request.POST['fiat_to_token_amount'])
                coin = request.POST['coin']
                transaction = tk.create_fiat_to_token_transaction(fiat_to_token_amount, coin=coin)
                
                tk.create_new_notification(title="Manual operation completed", message=f'tx name: {transaction.name}, state: {transaction.state}')



            elif 'token_to_fiat_amount' in request.POST:
                token_to_fiat_amount = eval(request.POST['token_to_fiat_amount'])
                coin = request.POST['coin']

                transaction = tk.create_token_to_fiat_transaction(token_to_fiat_amount, coin=coin)

                tk.create_new_notification(title="Manual operation completed", message=f'tx name: {transaction.name}, state: {transaction.state}')



            elif 'eth_amount_to_wrap' in request.POST:
                eth_amount_to_wrap = eval(request.POST['eth_amount_to_wrap'])

                transaction = tk.wrap_eth(eth_amount_to_wrap)

                tk.create_new_notification(title="Manual operation completed", message=f'tx name: {transaction.name}, state: {transaction.state}')


            elif 'weth_amount_to_unwrap' in request.POST:
                weth_amount_to_unwrap = eval(request.POST['weth_amount_to_unwrap'])

                transaction = tk.unwrap_weth(weth_amount_to_unwrap)

                tk.create_new_notification(title="Manual operation completed", message=f'tx name: {transaction.name}, state: {transaction.state}')



    context.dict['admin_settings'] =  tk.get_admin_settings()
    context.dict['positions'] =  models_position.Position.objects.all().order_by('-id')
    context.dict['orders'] =  models_order.Order.objects.filter(executed=False).order_by('-id')

    context.dict['new_random_name'] =  tk.get_new_random_name()
    context.dict['coins'] =  models_transaction.coins
    context.dict['fiat_coins'] =  models_transaction.fiat_coins
    context.dict['auto_exit_styles'] =  models_order.auto_exit_styles
    context.dict['order_modes'] =  models_order.order_modes


    return context.response()

