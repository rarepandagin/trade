
import os
import dashboard.views_pages.toolkit as tk
from dashboard.models import models_tick
import pandas as pd
from dashboard.modules.indicators.indicators import IndicatorsClass



def handle_ajax_posts_bot(req, payload):

    if  req == 'bot_download':

        from dashboard.modules.bots.utilities.download_binance_data import download_binance_data

        download_binance_data()



    elif req == 'bot_draw_data':

        print('loading df...')

        df = pd.read_pickle('./df.pickle')


        # data = [{
        #     'epoch': x.epoch,
        #     'price': x.price,
        #     'indicator_ema_minutely_200': x.indicator_ema_minutely_200,
        #     'indicator_ema_hourly_200': x.indicator_ema_hourly_200,
            
        #     } for x in models_tick.Tick.objects.all().order_by('epoch')]



        print('serializing data...')

        df.reset_index(drop=True)
        result = df.to_dict()

        sdf=3

        ret =  {
            'price':            [value  for key, value in result['price'].items()],
            'epoch':            [key    for key, value in result['price'].items()],
        }

        for key in result:
            if 'indicator_' in key:
                print(key)
                ret[key] = [value  for _, value in result[key].items()]

        print('plotting data...')

        return ret




    elif req == 'bot_import_data':
        models_tick.Tick.objects.all().delete()

        for root, dirs, files in os.walk(tk.bot_tmp_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                print('loading csv')

                df = pd.read_csv(file_path, usecols=[0, 4], delimiter=',', header=None, index_col=0, names=['index', 'price']
                , nrows=2_000_000
                )
                
                print('proccesing..')
                

                indicators_handler = IndicatorsClass(df)
                processed_df = indicators_handler.calculate_indicators()


                print('starting to bulk_create ')
                processed_df.to_pickle('./df.pickle')


                # model_instances = [models_tick.Tick(
                #         epoch                       =row.name,
                #         price                       =row['price'],
                #         indicator_ema_minutely_200  = row['indicator_ema_minutely_200'],
                #         indicator_ema_hourly_200  = row['indicator_ema_hourly_200'],
                #     ) for _, row in df.iterrows()
                #     ]

                # models_tick.Tick.objects.bulk_create(model_instances)   


                
                
                # os.remove(file_path)