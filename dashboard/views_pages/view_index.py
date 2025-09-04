import json
from dashboard.views_pages import toolkit as tk
from django.http import HttpResponse
from .context import context_class
import time
from threading import Thread
import threading
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync   

from dashboard.models import models_position, models_candle, models_event, models_transaction
import numpy as np

stop_event = threading.Event()

def exponential_moving_average(values, window_size, alpha=None):
    """
    Calculate the Exponential Moving Average (EMA) for a list of values.
    
    Parameters:
    values (list or array-like): The input data series.
    window_size (int): The number of periods to use for the EMA calculation.
    alpha (float, optional): The smoothing factor (0 < alpha < 1). If None, it is calculated as 2/(1+window_size).
    
    Returns:
    numpy.ndarray: An array of EMA values.
    """
    # Convert input to numpy array
    values = np.array(values)
    
    # Validate inputs
    if window_size <= 0:
        raise ValueError("window_size must be a positive integer.")
    if alpha is None:
        alpha = 2 / (1 + window_size)
    if not (0 < alpha < 1):
        raise ValueError("alpha must be between 0 and 1.")
    
    # Initialize EMA array
    ema = np.zeros_like(values)
    
    # First EMA value is the first value in the series
    ema[0] = values[0]
    
    # Calculate EMA for the rest of the values
    for i in range(1, len(values)):
        ema[i] = alpha * values[i] + (1 - alpha) * ema[i-1]
    
    return ema





def heart_beat_thread(data):

    channel_layer = get_channel_layer()

    while True:
        admin_settings = tk.get_admin_settings()

        # print(data)

        positions = models_position.Position.objects.filter(active=True)

        for position in positions:

            position.price = admin_settings.prices[position.coin.lower()]

            position.evaluate()

            position.save()

        
        # positions final report
        positions = models_position.Position.objects.all()
        positions_dict = [tk.serialize_object(x) for x in positions]






        # candle
        # coin = "ETH"
        # interval = Client.KLINE_INTERVAL_1MINUTE

        # candles = binance.get_coin_candles(coin=coin, interval=interval)


        # for candle in candles:
        #     new_candle = models_candle.Candle(
        #         coin=coin,
        #         interval=interval,
        #         open_time   =        candle[0],
        #         open        = float( candle[1]),
        #         high        = float( candle[2]),
        #         low         = float( candle[3]),
        #         close       = float( candle[4]),
        #         volume      = float( candle[5]),
        #         close_time  =        candle[6],
        #     )

        #     candle_already_exist = models_candle.Candle.objects.filter(coin=coin, interval=interval, open_time=new_candle.open_time).exists()

        #     if not candle_already_exist:
        #         new_candle.save()


        # candles = models_candle.Candle.objects.filter(coin=coin, interval=interval)

        # candles_dict = [tk.serialize_object(x) for x in candles]

        # candles_dict = sorted(candles_dict, key=lambda x: x['open_time'])

        # ema = exponential_moving_average([x['close'] for x in candles_dict], 200)
        # ema = [round(float(x), 2) for x in ema]

        # for idx, candle_dict in enumerate(candles_dict):
        #     candle_dict['ema'] = ema[idx]

        async_to_sync(channel_layer.group_send)(
            'chat_1',  # The group name
            {
                'type': 'message_channel_dashboard',
                'message': {
                    "topic": "update_positions_table",
                    "payload": {
                        "positions_dict": positions_dict,
                        # "candles_dict": candles_dict,
                        # "ema": ema,
                        "alarm": "",
                        "admin_settings": tk.serialize_object(admin_settings),
                    }
                }
            }
        )

        time.sleep(admin_settings.interval)

        if stop_event.is_set():
            print(f"Thread received stop signal and is exiting.")
            break

def get_response(request):

    context = context_class.context_class(request, template='dashboard/index.html')
    events = None

    if request.method == "POST":
        if 'req' in request.POST:
            ret = context.handle_ajax_post(request)

            return HttpResponse(json.dumps(ret), content_type='application/json')


        else:
            if 'start' in request.POST:
                admin_settings = tk.get_admin_settings()

                # if not admin_settings['running']:
                if admin_settings.thread_name in [x.name for x in threading.enumerate()]:
                    admin_settings.running = True
                    admin_settings.save()
                
                else:
                    new_thread_name = tk.get_new_uuid()

                    stop_event.clear()
                    t = Thread(target=heart_beat_thread, args=(f"{new_thread_name} launched at {tk.get_epoch_now()}",))
                    t.name = new_thread_name
                    t.start()

                    admin_settings.thread_name = new_thread_name
                    admin_settings.running = True
                    admin_settings.save()
            
            
            elif 'stop' in request.POST:
                admin_settings = tk.get_admin_settings()

                if admin_settings.running:

                    # thread =  [x for x in threading.enumerate() if x.name == admin_settings.thread_name][0]

                    stop_event.set()
                    admin_settings.thread_name = ''
                    admin_settings.running = False
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

            elif 'new_position_name' in request.POST:
                new_position_name       = request.POST['new_position_name']
                entry_capital           = eval(request.POST['entry_capital'])
                min_profit_exit_price   = eval(request.POST['min_profit_exit_price'])
                stop_loss_price         = eval(request.POST['stop_loss_price'])
                coin                    = request.POST['coin']



                new_transaction = tk.create_fiat_to_token_transaction(entry_capital, coin)


                if new_transaction.state == models_transaction.transaction_state_succesful:

                    new_position = models_position.Position(
                        name = new_position_name,
                        coin = coin,
                        position_type = models_position.long,
                        coin_amount = new_transaction.token_amount_recieved,
                        entry_capital = entry_capital,

                        entry_price=new_transaction.token_effective_price,

                        min_profit_exit_price = min_profit_exit_price,
                        stop_loss_price = stop_loss_price,
                        initial_stop_loss_price = stop_loss_price,
                    )

                    new_position.save()

                    new_transaction.position = new_position
                    new_transaction.save()


                else:
                    print("TX failed")


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
                
                print(f'tx name: {transaction.name}')
                


            elif 'token_to_fiat_amount' in request.POST:
                token_to_fiat_amount = eval(request.POST['token_to_fiat_amount'])
                coin = request.POST['coin']

                transaction = tk.create_token_to_fiat_transaction(token_to_fiat_amount, coin=coin)

                print(f'tx name: {transaction.name}')



    admin_settings = tk.get_admin_settings()

    # make sure the thread is running or not
    thread = None
    try:
        thread =  [x for x in threading.enumerate() if x.name == admin_settings.thread_name][0]
    except:
        pass


    if thread is None:
        admin_settings.thread_name = ''
        admin_settings.running = False
        admin_settings.save()
            

    context.dict['admin_settings'] =  tk.get_admin_settings()
    context.dict['positions'] =  models_position.Position.objects.all().order_by('-id')
    context.dict['position_types'] =  models_position.position_types

    context.dict['new_position_name'] =  tk.get_new_random_name()
    context.dict['coins'] =  models_transaction.coins
    context.dict['fiat_coins'] =  models_transaction.fiat_coins
    context.dict['auto_exit_styles'] =  models_position.auto_exit_styles

    return context.response()

