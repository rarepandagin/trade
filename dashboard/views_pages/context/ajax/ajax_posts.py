import json
from dashboard.views_pages import toolkit as tk
from dashboard.models import models_position
from dashboard.models import models_order
from dashboard.views_pages.context.ajax.ajax_posts_arbi import handle_ajax_posts_arbi
from dashboard.views_pages.context.ajax.ajax_posts_bot import handle_ajax_posts_bot
from dashboard.views_pages.context.ajax.ajax_posts_db import handle_ajax_posts_db
from traceback import format_exc

def handle_ajax_posts(self, request):

    req = request.POST['req']

    payload = json.loads(request.POST['payload'])

    success = True

    returned_payload = {}

    if 'arbi_' in req[:6]:
        handle_ajax_posts_arbi(req, payload)

    elif 'bot_' in req[:5]:
        returned_payload = handle_ajax_posts_bot(req, payload)

    elif 'db_' in req[:5]:
        returned_payload = handle_ajax_posts_db(req, payload)

    else:

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




        # elif  request.POST['req'] == 'update_both_way_quotes':
        #     from dashboard.modules.dapps.uniswap.uniswap_class import Uniswap

        #     uniswap = Uniswap()
        #     fiat_amount_in = payload['fiat_amount_in']
        #     uniswap.create_new_quote_and_save_to_db(fiat_to_coin=True, fiat_amount_in=fiat_amount_in)

        #     admin_settings = tk.get_admin_settings()

        #     coin_amount_in = payload['fiat_amount_in'] / admin_settings.prices['weth']
        #     uniswap.create_new_quote_and_save_to_db(fiat_to_coin=False, coin_amount_in=coin_amount_in)




        elif  request.POST['req'] == 'execute_order':
            # import time
            order = models_order.Order.objects.get(uuid=payload['order_uuid'])
            order.execute()
            # time.sleep(2)
            order.save()

            success = order.fulfilled




        elif  request.POST['req'] == 'exit_position':
            # import time
            position = models_position.Position.objects.get(uuid=payload['position_uuid'])
            position.exit_position()
            # time.sleep(2)
            position.save()

            success = position.exited_gracefully








    return {'req': req, 'success': success, 'returned_payload': returned_payload}