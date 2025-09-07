from traceback import format_exc
from dashboard.views_pages import toolkit as tk
from dashboard.models.models_position import models_position
from dashboard.models.models_position import models_order





def handle_ws_pulse(payload):

    try:

            admin_settings = tk.get_admin_settings()

            if admin_settings.pulses_are_being_blocked:
                tk.logger.info(f'pulses_are_being_blocked in on. rejecting the pulse...')
                return None

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

            # async_to_sync(channel_layer.group_send)(
            #     'chat_1',  # The group name
            #     {
            #         'type': 'message_channel_dashboard',
            #         'message': {
            #             "topic": "update_positions_table",
            #             "payload": {
            #                 "positions_dict": positions_dict,
            #                 # "candles_dict": candles_dict,
            #                 # "ema": ema,
            #                 "alarm": "",
            #                 "admin_settings": tk.serialize_object(admin_settings),
            #             }
            #         }
            #     }
            # )


            message = {
                "topic": "update_positions_table",
                "payload": {
                    "positions_dict": positions_dict,
                    # "candles_dict": candles_dict,
                    # "ema": ema,
                    "alarm": "",
                    "admin_settings": tk.serialize_object(admin_settings),
                }
            }


            admin_settings.pulses_are_being_blocked = False
            admin_settings.save()


            return message

            

    except:
        tk.logger.info(format_exc())
        return None
