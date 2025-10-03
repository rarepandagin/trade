from traceback import format_exc
from dashboard.views_pages import toolkit as tk
from dashboard.models.models_position import models_position
from dashboard.models.models_position import models_order
from dashboard.models import models_alert
import json
from dashboard.modules.dapps.aave.aave_class import Aave




def handle_a_pulse(request):


    try:

        payload = json.loads(request.body.decode('utf-8'))

        assert payload.get('key', '') == 'XiKd2uXZuT5vBU5mr2Qi'
        # tk.logger.info(payload)

        admin_settings = tk.get_admin_settings()
        
        admin_settings.gas = json.loads(payload['gas']['price'])
        admin_settings.gas_update_epoch = payload['gas']['epoch']

        admin_settings.prices = json.loads(payload['price']['price'])
        admin_settings.prices_update_epoch = payload['price']['epoch']


        admin_settings.added_slippage_multiplier_fiat_to_coin = json.loads(payload['quote']['quote'])['fiat_to_coin']
        admin_settings.added_slippage_multiplier_coin_to_fiat = json.loads(payload['quote']['quote'])['coin_to_fiat']

        admin_settings.save()

        if admin_settings.pulses_are_being_blocked:
            tk.logger.info(f'--------> XXxXX pulses are being blocked.')
            raise

        else:
            # tk.logger.info(f'--------> effective pulse: {payload}')

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
            ret = order.evaluate()
            # if ret is not None:
            order.save()

        # handle aave
        if admin_settings.borrow_from_aave and admin_settings.pulse_counter % admin_settings.aave_info_update_pulse_steps == 0:
            aave = Aave()
            admin_settings.aave_user_account_data = aave.getUserAccountData()


        payload =  {
                "positions_dict": positions_dict,
                "alarm": "",
                "admin_settings": tk.serialize_object(admin_settings),
            }

        tk.send_message_to_frontend_dashboard(topic='update_positions_table', payload=payload)



        # handle alerts:
        for alert in models_alert.Alert.objects.filter(executed=False):
            alert.evaluate()
            alert.save()




        admin_settings.pulse_counter += 1

        admin_settings.pulses_are_being_blocked = False
        admin_settings.save()


        return {'interval': admin_settings.interval}

        

    except:
        admin_settings = tk.get_admin_settings()

        admin_settings.pulses_are_being_blocked = False
        admin_settings.save()

        tk.logger.info(format_exc())
        return {}
