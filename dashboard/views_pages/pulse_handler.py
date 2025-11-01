from traceback import format_exc
from dashboard.views_pages import toolkit as tk
from dashboard.models.models_position import models_position
from dashboard.models.models_position import models_order
from dashboard.models import models_token
from dashboard.models import models_alert
from dashboard.models import models_adminsettings
import json
from dashboard.modules.dapps.aave.aave_class import Aave
import copy
from dashboard.views_pages.vision import Vision
# import time
# from dashboard.modules.dapps.dex.dex_class import Dex
from dashboard.views_pages import transaction_dispatch

def handle_tokens(payload):
    # tk.logger.info(f'handling tokens')

    # filter incoming tokens with unknown contract
    models_token.Token.objects.filter(imported=False).delete()

    incoming_token_dict_list = payload['tokens']

    locally_existing_token_contracts = [x.contract for x in models_token.Token.objects.all()]

    tokens_to_be_added = []

    contracts_to_update = []

    for incoming_token_dict in incoming_token_dict_list:

        if incoming_token_dict['contract'] in locally_existing_token_contracts:
            # these contracts already exist, we need to update our local copy
            contracts_to_update.append(incoming_token_dict['contract'])

        else:
            # these are tokens that their contract is new for us
            tokens_to_be_added.append(models_token.Token(**incoming_token_dict))

    if len(tokens_to_be_added) > 0:
        # tk.logger.info(f'++++++++++++adding {len(tokens_to_be_added)} new tokens')
        models_token.Token.objects.bulk_create(tokens_to_be_added, ignore_conflicts=True)

    if len(contracts_to_update) > 0:
        # tk.logger.info(f'-----------updating {len(contracts_to_update)} exiting tokens')

        existing_token_to_be_updated = {obj.contract: obj for obj in models_token.Token.objects.filter(contract__in=contracts_to_update)}

        for item in incoming_token_dict_list:
            obj = existing_token_to_be_updated.get(item['contract'])
            if obj:

                obj.weth_pair_reserves          = item['weth_pair_reserves']
                obj.token_pair_reserves         = item['token_pair_reserves']
                obj.price_per_weth              = item['price_per_weth']
                obj.volume                      = item['volume']

                obj.uncx_user                   = item['uncx_user']
                obj.uncx_token_amount           = item['uncx_token_amount']
                obj.uncx_pool_lock_ratio        = item['uncx_pool_lock_ratio']
                obj.uncx_epoch_start_lock       = item['uncx_epoch_start_lock']
                obj.uncx_epoch_end_lock         = item['uncx_epoch_end_lock']
                
                obj.go_plus_lp_total_supply     = item['go_plus_lp_total_supply']
                obj.go_plus_locked_lp_ratio     = item['go_plus_locked_lp_ratio']
                obj.go_plus_dex_liquidity       = item['go_plus_dex_liquidity']
                obj.go_plus_security_issues     = item['go_plus_security_issues']
                
                obj.keep_investigating          = item['keep_investigating']
                obj.epoch_investigated          = item['epoch_investigated']
                obj.investigation_pass          = item['investigation_pass']
                obj.investigation_red_flag      = item['investigation_red_flag']
                obj.investigated                = item['investigated']


        models_token.Token.objects.bulk_update(existing_token_to_be_updated.values(), fields=[

                'weth_pair_reserves',
                'token_pair_reserves',
                'price_per_weth',
                'volume',
                'uncx_user',
                'uncx_token_amount',
                'uncx_pool_lock_ratio',
                'uncx_epoch_start_lock',
                'uncx_epoch_end_lock',
                'go_plus_lp_total_supply',
                'go_plus_locked_lp_ratio',
                'go_plus_dex_liquidity',
                'go_plus_security_issues',
                'keep_investigating',
                'epoch_investigated',
                'investigation_pass',
                'investigation_red_flag',
                'investigated',

            ], batch_size=100)


    for token in models_token.Token.objects.all():
        if (token.investigated) and(token.investigation_pass) and (not token.already_alerted) :

            message = f"{token.name} passed investigation\npair created: {tk.epoch_to_datetime(token.pair_creation_epoch)}\nuncx locked: {tk.epoch_to_datetime(token.uncx_epoch_start_lock)}"

            
            tk.create_new_notification(title="New Token", message=message)

            token.imported = True
            token.already_alerted = True
            token.save()


            admin_settings = tk.get_admin_settings()

            # attempting to auto-buy
            if (admin_settings.allow_auto_purchase) and (not token.auto_purchased):

                fiat_amount = admin_settings.auto_purchase_fiat_amount
                
                tk.logger.info(f"executing auto buy order (fiat={fiat_amount} $) for {token.name}...")

                try:
                    tk.update_admin_settings('active_account', models_adminsettings.account_dex)
            
                    transaction_dispatch.create_and_actualize_dex_fiat_to_token_transaction(
                            fiat_to_token_amount=fiat_amount,
                            token_contract=token.contract
                        )

                except:
                    tk.logger.info(f"auto buy order ERROR:\n {format_exc()}")

                token.auto_purchased = True
                token.save()



    tk.update_admin_settings('tokens', [tk.serialize_object(x) for x in models_token.Token.objects.all() if x.show])


def handle_a_pulse(request):

    try:

        payload = json.loads(request.body.decode('utf-8'))

        assert payload.get('key', '') == 'XiKd2uXZuT5vBU5mr2Qi'
        payload = tk.decompress_pickle_object(payload['payload'])



        tk.update_admin_settings('INDICATORS', payload['INDICATORS'])
        tk.update_admin_settings('MINUTES', payload['MINUTES'])

        if 'live_indicators' in payload:
            tk.update_admin_settings('live_indicators', payload['live_indicators'])

            vision = Vision()
            vision.look_around()
            
            tk.update_admin_settings('vision', vision.serialize())


        if 'tokens' in payload:
            handle_tokens(payload)



        tk.update_admin_settings('gas', json.loads(payload['gas']['price']))
        tk.update_admin_settings('gas_update_epoch', payload['gas']['epoch'])
        tk.update_admin_settings('prices', {'weth': payload['price']['price']})
        tk.update_admin_settings('prices_update_epoch', payload['price']['epoch'])

        ##################################################################################
        admin_settings = tk.get_admin_settings()

        # tk.logger.info(f'<-------')

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

        # handle aave
        # if admin_settings.borrow_from_aave and admin_settings.pulse_counter % admin_settings.aave_info_update_pulse_steps == 0:
        #     aave = Aave()
        #     tk.update_admin_settings('aave_user_account_data', aave.getUserAccountData())


        payload =  {
                "positions_dict": positions_dict,
                "alarm": "",
                "admin_settings": tk.serialize_object(admin_settings),
                "chart_df": [],#payload['chart_df'],
            }

        tk.send_message_to_frontend_dashboard(topic='update_positions_table', payload=payload)



        # handle alerts:
        for alert in models_alert.Alert.objects.filter(executed=False):
            alert.evaluate()
            alert.save()

        # indicators
        



        to_return = copy.deepcopy(
            {
                'interval':                     copy.deepcopy(admin_settings.interval),
                'command_function':             copy.deepcopy(admin_settings.command_function),
                'command_arguments':            copy.deepcopy(admin_settings.command_arguments),
                'active_time_frame_minutes':    copy.deepcopy(admin_settings.active_time_frame_minutes),
                'active_time_frame_length':     copy.deepcopy(admin_settings.active_time_frame_length),
            }
        )


        tk.update_admin_settings('command_function', '')
        tk.update_admin_settings('command_arguments', {})
        tk.update_admin_settings('pulse_counter', admin_settings.pulse_counter+1)


        # tk.logger.info("FINISHED PULSE")
        return to_return
        

    except:



        tk.logger.info(format_exc())
        return {}
