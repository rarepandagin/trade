import json
from dashboard.views_pages import toolkit as tk
from django.http import HttpResponse
from .context import context_class

from dashboard.models import models_transaction, models_order

                
def get_response(request):

    context = context_class.context_class(request, template='dashboard/orders.html')

    if request.method == "POST":
        if 'req' in request.POST:
            ret = context.handle_ajax_post(request)

            return HttpResponse(json.dumps(ret), content_type='application/json')


        else:


            if 'update_order' in request.POST:
                order_uuid = request.POST['order_uuid']
                order = models_order.Order.objects.get(uuid=order_uuid)

                order.name                      = request.POST['order_action_set_name']
                order.entry_capital             = eval(request.POST['order_action_set_entry_capital'])
                order.order_price               = eval(request.POST['order_action_set_order_price'])
                order.min_profit_exit_price     = eval(request.POST['order_action_set_min_profit_exit_price'])
                order.stop_loss_price           = eval(request.POST['order_action_set_stop_loss_price'])
                
                order.save()


            elif 'order_delete' in request.POST:
                order_uuid = request.POST['order_uuid']
                order = models_order.Order.objects.get(uuid=order_uuid)
                order.delete()

            elif 'order_archive' in request.POST:
                order_uuid = request.POST['order_uuid']
                order = models_order.Order.objects.get(uuid=order_uuid)
                order.archived = True
                order.save()

            elif 'order_deactivate' in request.POST:
                order_uuid = request.POST['order_uuid']
                order = models_order.Order.objects.get(uuid=order_uuid)
                if order.active:
                    order.active = False
                    order.save()

            elif 'order_activate' in request.POST:
                order_uuid = request.POST['order_uuid']
                order = models_order.Order.objects.get(uuid=order_uuid)
                if not order.active:
                    order.active = True
                    order.save()





            elif 'new_order_name' in request.POST:
                new_order_name          = request.POST['new_order_name']
                coin                    = request.POST['coin']
                order_mode              = request.POST['order_mode']

                entry_capital           = eval(request.POST['entry_capital'])
                order_price           = eval(request.POST['order_price'])
                
                min_profit_exit_price   = eval(request.POST['min_profit_exit_price'])
                stop_loss_price         = eval(request.POST['stop_loss_price'])

                new_order = models_order.Order(
                    name = new_order_name,
                    coin = coin,
                    mode = order_mode,
                    entry_capital = entry_capital,
                    order_price = order_price,
                    min_profit_exit_price = min_profit_exit_price,
                    stop_loss_price = stop_loss_price,
                    
                )

                new_order.save()








    context.dict['admin_settings'] =  tk.get_admin_settings()
    context.dict['orders'] =  models_order.Order.objects.filter(archived=False).order_by('-id')

    context.dict['new_random_name'] =  tk.get_new_random_name()
    context.dict['coins'] =  models_transaction.coins
    context.dict['fiat_coins'] =  models_transaction.fiat_coins
    context.dict['auto_exit_styles'] =  models_order.auto_exit_styles
    context.dict['order_modes'] =  models_order.order_modes


    return context.response()

