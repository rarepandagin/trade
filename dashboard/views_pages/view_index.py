import json
from dashboard.views_pages import toolkit as tk
from django.http import HttpResponse
from .context import context_class

from dashboard.models import models_position, models_order

                
def get_response(request):

    context = context_class.context_class(request, template='dashboard/index.html')

    if request.method == "POST":
        if 'req' in request.POST:
            ret = context.handle_ajax_post(request)

            return HttpResponse(json.dumps(ret), content_type='application/json')


        else:

            if 'position_action_activate' in request.POST:
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
            
            elif 'position_action_set_profit_take_price' in request.POST:
                position_uuid = request.POST['position_uuid']
                position = models_position.Position.objects.get(uuid=position_uuid)
                position.reset()
                position_profit_take_price = eval(request.POST['position_profit_take_price'])
                position.profit_take_price = position_profit_take_price
                position.save()

            elif 'position_action_archive' in request.POST:
                position_uuid = request.POST['position_uuid']
                position = models_position.Position.objects.get(uuid=position_uuid)

                position.archived = True
                position.save()


            elif 'auto_exit_style' in request.POST:
                position_uuid = request.POST['position_uuid']
                position = models_position.Position.objects.get(uuid=position_uuid)
                position.reset()
                position.auto_exit_style = request.POST['auto_exit_style']
                position.save()




    context.dict['positions'] =  models_position.Position.objects.filter(archived=False).order_by('-id')
    context.dict['orders'] =  models_order.Order.objects.filter(executed=False).order_by('-id')


    return context.response()

