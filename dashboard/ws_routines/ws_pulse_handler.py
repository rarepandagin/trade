from traceback import format_exc
from dashboard.views_pages import toolkit as tk
from dashboard.models.models_position import models_position
from dashboard.models.models_position import models_order
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync   




def handle_ws_pulse(request):

        payload = json.loads(request.body.decode('utf-8'))

        if payload.get('key', '') != 'XiKd2uXZuT5vBU5mr2Qi':
            return {}

        else:

            try:
                admin_settings = tk.get_admin_settings()

                if admin_settings.pulses_are_being_blocked:
                    tk.logger.info(f'pulses_are_being_blocked in on. rejecting the pulse...')
                    return {}

                else:
                    tk.logger.info(f'effective pulse: {payload}')

                    admin_settings.pulses_are_being_blocked = True
                    admin_settings.save()



                positions = models_position.Position.objects.filter(active=True)

                for position in positions:

                    position.price = admin_settings.prices[position.order.coin.lower()]

                    position.evaluate()

                    position.save()

                
                # positions final report
                positions = models_position.Position.objects.all()
                positions_dict = [tk.serialize_object(x) for x in positions]
                for position in positions_dict:
                    position['order'] = tk.serialize_object(models_order.Order.objects.get(id=position['order']))


                orders = models_order.Order.objects.filter(active=True, executed=False)
                for order in orders:
                    order.evaluate()
                    order.save()



                message = {
                    "topic": "update_positions_table",
                    "payload": {
                        "positions_dict": positions_dict,
                        "alarm": "",
                        "admin_settings": tk.serialize_object(admin_settings),
                    }
                }
                
                channel_layer = get_channel_layer()

                async_to_sync(channel_layer.group_send)(
                    'chat_1',  # The group name
                    {
                        'type': 'message_channel_dashboard',
                        'message': message
                    }
                )



                admin_settings.pulses_are_being_blocked = False
                admin_settings.save()


                return {'interval': admin_settings.interval}

                

            except:
                tk.logger.info(format_exc())
                return {}
