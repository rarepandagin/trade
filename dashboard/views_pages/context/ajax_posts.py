import json
from dashboard.views_pages import toolkit as tk
from dashboard.models import models_position
from traceback import format_exc

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
        from dashboard.modules.uniswap.v3_class import Uniswap

        try:
            tk.send_message_to_frontend(topic='display_toaster', payload={'message': f'starting update_balances', 'color': 'green'})

            uniswap = Uniswap()


            balances = uniswap.check_balance()
            admin_settings = tk.get_admin_settings()
            admin_settings.balances = balances
            admin_settings.save()

            tk.send_message_to_frontend(topic='display_toaster', payload={'message': f'finished update_balances', 'color': 'green'})

        except:
            tk.logger.info(format_exc())

    elif  request.POST['req'] == 'update_both_way_quotes':
        from dashboard.modules.uniswap.v3_class import Uniswap

        uniswap = Uniswap()
        fiat_amount_in = payload['fiat_amount_in']
        uniswap.create_new_quote_and_save_to_db(fiat_to_coin=True, fiat_amount_in=fiat_amount_in)

        admin_settings = tk.get_admin_settings()

        coin_amount_in = payload['fiat_amount_in'] / admin_settings.prices['weth']
        uniswap.create_new_quote_and_save_to_db(fiat_to_coin=False, coin_amount_in=coin_amount_in)

