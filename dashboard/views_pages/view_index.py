import json
from dashboard.views_pages import toolkit as tk
from django.http import HttpResponse
from .context import context_class
from dashboard.views_pages.pulse_handler import handle_a_pulse

from dashboard.models import models_position, models_candle, models_event, models_transaction, models_order

from mysite import settings    
                
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











            elif 'event_delete' in request.POST:
                event_uuids = request.POST.getlist('event_delete')
                for event_uuid in event_uuids:
                    event = models_event.Event.objects.get(uuid=event_uuid)
                    event.delete()

            elif 'delete_position_events' in request.POST:
                position_uuid = request.POST['position_uuid']
                position = models_position.Position.objects.get(uuid=position_uuid)
                models_event.Event.objects.filter(position=position).delete()





            elif 'position_action_archive' in request.POST:
                position_uuid = request.POST['position_uuid']
                position = models_position.Position.objects.get(uuid=position_uuid)

                position.archived = True
                position.save()




    context.dict['admin_settings'] =  tk.get_admin_settings()
    context.dict['positions'] =  models_position.Position.objects.filter(archived=False).order_by('-id')
    context.dict['orders'] =  models_order.Order.objects.filter(executed=False).order_by('-id')

    context.dict['new_random_name'] =  tk.get_new_random_name()
    context.dict['coins'] =  models_transaction.coins
    context.dict['fiat_coins'] =  models_transaction.fiat_coins
    context.dict['auto_exit_styles'] =  models_order.auto_exit_styles


    return context.response()

