import json
from dashboard.views_pages import toolkit as tk
from django.http import HttpResponse
from .context import context_class
from dashboard.views_pages.pulse_handler import handle_a_pulse

from dashboard.models import models_position, models_candle, models_event, models_transaction, models_order
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync   
# from threading import Thread



# def heart_beat_thread(payload):


#     channel_layer = get_channel_layer()

#     async_to_sync(channel_layer.group_send)(
#         'room_group_name',  # The group name
#         {
#         'type': 'message_channel_dashboard',
#         'message': {
#             "topic": "update_positions_table",
#             "payload": payload
#             }
#         }
#     )
    
                
def get_response(request):

    context = context_class.context_class(request, template='dashboard/index.html')

    if request.method == "POST":
        if 'req' in request.POST:
            ret = context.handle_ajax_post(request)

            return HttpResponse(json.dumps(ret), content_type='application/json')


        else:


            if 'unblock_pulses' in request.POST:
                admin_settings = tk.get_admin_settings()
                admin_settings.pulses_are_being_blocked = False
                admin_settings.save()

            
            elif 'block_pulses' in request.POST:
                admin_settings = tk.get_admin_settings()
                admin_settings.pulses_are_being_blocked = True
                admin_settings.save()


            

            elif 'admin_settings_alarms' in request.POST:
                admin_settings = tk.get_admin_settings()
                admin_settings.alarms = not admin_settings.alarms
                admin_settings.save()

            elif 'admin_settings_interval' in request.POST:
                admin_settings = tk.get_admin_settings()
                admin_settings.interval = int(request.POST['admin_settings_interval'])
                admin_settings.save()

            elif 'admin_settings_fiat_coin' in request.POST:
                admin_settings = tk.get_admin_settings()
                admin_settings.fiat_coin = request.POST['admin_settings_fiat_coin']
                admin_settings.save()

            elif 'admin_settings_secure_profit_ratio' in request.POST:
                admin_settings = tk.get_admin_settings()
                admin_settings.secure_profit_ratio = eval(request.POST['admin_settings_secure_profit_ratio'])
                admin_settings.save()



            elif 'position_action_activate' in request.POST:
                position_uuid = request.POST['position_uuid']
                position = models_position.Position.objects.get(uuid=position_uuid)
                position.active = not position.active
                position.reset()
                position.save()

            elif 'position_action_display_on_chart' in request.POST:
                position_uuid = request.POST['position_uuid']
                position = models_position.Position.objects.get(uuid=position_uuid)
                position.display_on_chart = not position.display_on_chart
                position.save()
            
            elif 'position_action_set_stop_loss_price' in request.POST:
                position_uuid = request.POST['position_uuid']
                position = models_position.Position.objects.get(uuid=position_uuid)
                position.reset()
                position_stop_loss_price = eval(request.POST['position_stop_loss_price'])
                position.stop_loss_price = position_stop_loss_price
                position.initial_stop_loss_price = position_stop_loss_price
                position.save()
            
            elif 'position_action_set_min_profit_exit_price' in request.POST:
                position_uuid = request.POST['position_uuid']
                position = models_position.Position.objects.get(uuid=position_uuid)
                position.reset()
                position_min_profit_exit_price = eval(request.POST['position_min_profit_exit_price'])
                position.min_profit_exit_price = position_min_profit_exit_price
                position.save()

            elif 'auto_exit_style' in request.POST:
                position_uuid = request.POST['position_uuid']
                position = models_position.Position.objects.get(uuid=position_uuid)
                position.reset()
                position.auto_exit_style = request.POST['auto_exit_style']
                position.save()






            elif 'update_order' in request.POST:
                order_uuid = request.POST['order_uuid']
                order = models_order.Order.objects.get(uuid=order_uuid)

                order.name                      = request.POST['order_action_set_name']
                order.entry_capital             = eval(request.POST['order_action_set_entry_capital'])
                order.order_price               = eval(request.POST['order_action_set_order_price'])
                order.min_profit_exit_price     = eval(request.POST['order_action_set_min_profit_exit_price'])
                order.stop_loss_price           = eval(request.POST['order_action_set_stop_loss_price'])
                
                order.save()



            elif 'order_execute_now' in request.POST:
                order_uuid = request.POST['order_uuid']
                order = models_order.Order.objects.get(uuid=order_uuid)
                if order.active and (not order.fullfiled):
                    order.execute()
                    order.save()

            elif 'order_delete' in request.POST:
                order_uuid = request.POST['order_uuid']
                order = models_order.Order.objects.get(uuid=order_uuid)
                order.delete()

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








            elif 'event_delete' in request.POST:
                event_uuids = request.POST.getlist('event_delete')
                for event_uuid in event_uuids:
                    event = models_event.Event.objects.get(uuid=event_uuid)
                    event.delete()

            elif 'delete_position_events' in request.POST:
                position_uuid = request.POST['position_uuid']
                position = models_position.Position.objects.get(uuid=position_uuid)
                models_event.Event.objects.filter(position=position).delete()




            elif 'new_order_name' in request.POST:
                new_order_name          = request.POST['new_order_name']
                coin                    = request.POST['coin']
                order_mode              = request.POST['order_mode']

                entry_capital           = eval(request.POST['entry_capital'])
                order_price           = eval(request.POST['order_price'])
                
                min_profit_exit_price   = eval(request.POST['min_profit_exit_price'])
                stop_loss_price         = eval(request.POST['stop_loss_price'])

                execute_order_now_with_live_price = 'execute_order_now_with_live_price' in request.POST

                new_order = models_order.Order(
                    name = new_order_name,
                    coin = coin,
                    mode = order_mode,
                    entry_capital = entry_capital,
                    order_price = order_price,
                    min_profit_exit_price = min_profit_exit_price,
                    stop_loss_price = stop_loss_price,
                )

                if execute_order_now_with_live_price:
                    admin_settings = tk.get_admin_settings()
                    new_order.order_price = admin_settings.prices[coin.lower()]
                else:
                    new_order.order_price = order_price


                new_order.save()

                if execute_order_now_with_live_price:
                    new_order.execute()

                    new_order.save()



            elif 'position_action_exit_now' in request.POST:
                position_uuid = request.POST['position_uuid']
                position = models_position.Position.objects.get(uuid=position_uuid)

                position.exit_position()
                position.save()

            elif 'position_action_delete' in request.POST:
                position_uuid = request.POST['position_uuid']
                position = models_position.Position.objects.get(uuid=position_uuid)

                position.delete()


            elif 'fiat_to_token_amount' in request.POST:
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


    # ret_handle_a_pulse = handle_a_pulse(request)

    
    # if 'payload' in ret_handle_a_pulse:

    #     t = Thread(target=heart_beat_thread, args=(ret_handle_a_pulse['payload'],))
    #     t.start()


    context.dict['admin_settings'] =  tk.get_admin_settings()
    context.dict['positions'] =  models_position.Position.objects.all().order_by('-id')
    context.dict['orders'] =  models_order.Order.objects.filter(executed=False).order_by('-id')

    context.dict['new_random_name'] =  tk.get_new_random_name()
    context.dict['coins'] =  models_transaction.coins
    context.dict['fiat_coins'] =  models_transaction.fiat_coins
    context.dict['auto_exit_styles'] =  models_order.auto_exit_styles
    context.dict['order_modes'] =  models_order.order_modes

    return context.response()

