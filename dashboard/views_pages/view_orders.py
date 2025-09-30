import json
from dashboard.views_pages import toolkit as tk
from django.http import HttpResponse
from .context import context_class

from dashboard.models import models_transaction, models_order, models_pair

                
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
                order.order_entry_price               = eval(request.POST['order_action_set_order_entry_price'])
                order.profit_take_price         = eval(request.POST['order_action_set_profit_take_price'])
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

                which_order             = request.POST['which_order']

                entry_capital_long      = eval(request.POST['entry_capital_long'])
                stop_loss_price_long    = eval(request.POST['stop_loss_price_long'])
                profit_take_price_long  = eval(request.POST['profit_take_price_long'])

                entry_capital_short     = eval(request.POST['entry_capital_short'])
                stop_loss_price_short   = eval(request.POST['stop_loss_price_short'])
                profit_take_price_short = eval(request.POST['profit_take_price_short'])

                entry_price_long        = eval(request.POST['entry_price_long'])
                entry_price_short       = eval(request.POST['entry_price_short'])

                entry_condition_short   = request.POST['entry_condition_short']
                entry_condition_long    = request.POST['entry_condition_long']
                coin                    = models_order.weth
                new_order_name_from_post= request.POST['new_order_name']

                valid_long_data = True
                valid_short_data = True

                pair = None
                if which_order == 'both':
                    pair = models_pair.Pair()
                    pair.save()

                admin_settings = tk.get_admin_settings()

                if which_order in ['long', 'both']:
                    # check if long inputs are valid
                    valid_long_data = (stop_loss_price_long < entry_price_long < profit_take_price_long) and (0 < entry_capital_long < admin_settings.balances[admin_settings.fiat_coin])

                if which_order in ['short', 'both']:
                    # check if short inputs are valid
                    valid_short_data = (profit_take_price_short < entry_price_short < stop_loss_price_short)
                    if valid_short_data and admin_settings.borrow_from_aave:

                            valid_short_data = 0 < entry_capital_short < admin_settings.aave_borrow_to_collateral_added_safety_ratio * admin_settings.aave_user_account_data['availableBorrowsBase']

                if valid_long_data and valid_short_data:




                    if which_order in ['short', 'both']:

                        new_order_short = models_order.Order(
                            name                = f"{new_order_name_from_post} (short)",
                            coin                = coin,
                            entry_condition     = entry_condition_short,
                            order_entry_price    = entry_price_short,

                            position_type       = models_order.short,
                            entry_capital       = entry_capital_short,
                            profit_take_price   = profit_take_price_short,
                            stop_loss_price     = stop_loss_price_short,
                            
                        )


                        if pair is not None:
                            new_order_short.pair_uuid = pair.uuid

                        new_order_short.save()


                    if which_order in ['long', 'both']:

                        new_order_long = models_order.Order(
                            name                = f"{new_order_name_from_post} (long)",
                            coin                = coin,
                            entry_condition     = entry_condition_long,
                            order_entry_price   = entry_price_long,

                            position_type       = models_order.long,
                            entry_capital       = entry_capital_long,
                            profit_take_price   = profit_take_price_long,
                            stop_loss_price     = stop_loss_price_long,
                            
                        )

                        if pair is not None:
                            new_order_long.pair_uuid = pair.uuid

                        new_order_long.save()





                else:
                    tk.logger.info('Invalid order')



    admin_settings = tk.get_admin_settings()


    context.dict['admin_settings'] =  admin_settings
    context.dict['orders'] =  models_order.Order.objects.filter(archived=False).order_by('-id')

    context.dict['new_random_name'] =  tk.get_new_random_name()
    context.dict['coins'] =  models_transaction.coins
    context.dict['fiat_coins'] =  models_transaction.fiat_coins
    context.dict['auto_exit_styles'] =  models_order.auto_exit_styles
    context.dict['entry_conditions'] =  models_order.entry_conditions
    context.dict['position_types'] =  models_order.position_types


    context.dict['new_position_entry_price']        = admin_settings.prices['weth']
    context.dict['new_position_short_stop_loss']    = int(1.01 * admin_settings.prices['weth'])
    context.dict['new_position_short_profit_take']    = int(0.98 * admin_settings.prices['weth'])
    context.dict['new_position_long_stop_loss']    = int(0.99 * admin_settings.prices['weth'])
    context.dict['new_position_long_profit_take']    = int(1.02 * admin_settings.prices['weth'])


    return context.response()

