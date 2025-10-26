from traceback import format_exc
from dashboard.views_pages import toolkit as tk
from dashboard.models.models_position import models_position
from dashboard.models.models_position import models_order
from dashboard.models import models_token
from dashboard.models import models_alert
import json
from dashboard.modules.dapps.aave.aave_class import Aave
import copy
from dashboard.views_pages.vision import Vision

def handle_a_pulse(request):

    try:

        payload = json.loads(request.body.decode('utf-8'))

        assert payload.get('key', '') == 'XiKd2uXZuT5vBU5mr2Qi'
        payload = tk.decompress_pickle_object(payload['payload'])

        admin_settings = tk.get_admin_settings()

        admin_settings.INDICATORS = payload['INDICATORS']
        admin_settings.MINUTES = payload['MINUTES']

        if 'live_indicators' in payload:
            admin_settings.live_indicators = payload['live_indicators']
            vision = Vision()
            vision.look_around()
            

            admin_settings.vision = vision.serialize()
            # tk.logger.info(admin_settings.vision)

        if 'tokens' in payload:
            # tk.logger.info(payload['tokens'])
            incoming_token_dict_list = [json.loads(x['fields']) for x in payload['tokens']]

            existing_token_contracts = [x.contract for x in models_token.Token.objects.all()]

            tokens_to_be_added = []

            contracts_to_update = []

            for incoming_token_dict in incoming_token_dict_list:

                if incoming_token_dict['contract'] in existing_token_contracts:
                    contracts_to_update.append(incoming_token_dict['contract'])

                else:
                    tokens_to_be_added.append(models_token.Token(**incoming_token_dict))

            if len(tokens_to_be_added) > 0:
                models_token.Token.objects.bulk_create(tokens_to_be_added, ignore_conflicts=True)

            if len(contracts_to_update) > 0:
                existing_token_to_be_updated = {obj.contract: obj for obj in models_token.Token.objects.filter(contract__in=contracts_to_update)}

                for item in incoming_token_dict_list:
                    obj = existing_token_to_be_updated.get(item['contract'])
                    if obj:
                        obj.price = item['price']
                        obj.volume = item['volume']
                        obj.makers = item['makers']
                        obj.liquidity = item['liquidity']
                        obj.cap = item['cap']
                        obj.locked_liquidity = item['locked_liquidity']
                        obj.has_website = item['has_website']
                        obj.has_twitter = item['has_twitter']
                        obj.has_telegram = item['has_telegram']
                        obj.go_security = item['go_security']
                        obj.quick_intel = item['quick_intel']
                        obj.token_sniffer = item['token_sniffer']
                        obj.honeypot_is = item['honeypot_is']

                # Bulk update by primary key
                models_token.Token.objects.bulk_update(existing_token_to_be_updated.values(), fields=[
                    'price',
                    'volume',
                    'makers',
                    'liquidity',
                    'cap',
                    'locked_liquidity',
                    'has_website',
                    'has_twitter',
                    'has_telegram',
                    'go_security',
                    'quick_intel',
                    'token_sniffer',
                    'honeypot_is',

                    ], batch_size=100)

            # send alerts for interesting tokens:
            # for token in models_token.Token.objects.all():
            #     if not token.already_alerted:
            #         criteria_liquidity = token.locked_liquidity and token.liquidity > 4000
            #         criteria_age = (tk.get_epoch_now() - token.epoch_created) < 30 * 60
            #         if criteria_liquidity and criteria_age:
            #             tk.create_new_notification(title="New Token", message=f"{token.name} with locked liquidity of {token.liquidity} detected.")

            #         token.already_alerted = True
            #         token.save()



            admin_settings.tokens = [tk.serialize_object(x) for x in models_token.Token.objects.all() if x.show]

        admin_settings.gas = json.loads(payload['gas']['price'])
        admin_settings.gas_update_epoch = payload['gas']['epoch']

        admin_settings.prices = {'weth': payload['price']['price']}
        admin_settings.prices_update_epoch = payload['price']['epoch']


        # admin_settings.uniswap_asm_fiat_to_token = payload['quote']['uniswap']['asm_fiat_to_token']
        # admin_settings.uniswap_asm_token_to_fiat = payload['quote']['uniswap']['asm_token_to_fiat']

        # admin_settings.sushiswap_asm_fiat_to_token = payload['quote']['sushiswap']['asm_fiat_to_token']
        # admin_settings.sushiswap_asm_token_to_fiat = payload['quote']['sushiswap']['asm_token_to_fiat']

        admin_settings.save()

        if admin_settings.pulses_are_being_blocked:
            tk.logger.info(f'--------> XXxXX pulses are being blocked.')
            # raise
            return {}

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
                "chart_df": payload['chart_df'],
            }

        tk.send_message_to_frontend_dashboard(topic='update_positions_table', payload=payload)



        # handle alerts:
        for alert in models_alert.Alert.objects.filter(executed=False):
            alert.evaluate()
            alert.save()

        # indicators
        



        to_return = copy.deepcopy(
            {
                'interval': admin_settings.interval,
                'command_function': admin_settings.command_function,
                'command_arguments': admin_settings.command_arguments,
                'active_time_frame_minutes': admin_settings.active_time_frame_minutes,
                'active_time_frame_length': admin_settings.active_time_frame_length,
            }
        )

        admin_settings.command_function = ''
        admin_settings.command_arguments = {}

        admin_settings.pulse_counter += 1

        admin_settings.pulses_are_being_blocked = False
        admin_settings.save()


        return to_return
        

    except:
        admin_settings = tk.get_admin_settings()

        admin_settings.pulses_are_being_blocked = False
        admin_settings.save()

        tk.logger.info(format_exc())
        return {}
