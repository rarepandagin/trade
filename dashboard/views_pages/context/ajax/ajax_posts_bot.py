
import os
from dashboard import models
import dashboard.views_pages.toolkit as tk
import csv
from dashboard.models import models_tick
from tqdm import tqdm
import pandas as pd

from django.db.models import Count, Sum
from django.db.models.functions import TruncHour
from datetime import datetime

import numpy as np

def calculate_ema(prices, periods, smoothing=2):
    """
    Calculate the Exponential Moving Average (EMA) for a list of price values.
    
    The EMA gives greater weight to recent prices, making it more responsive to new information
    compared to a Simple Moving Average (SMA). The first EMA value is calculated as the SMA
    of the initial 'periods'
    
    $$ EMA_t = (price_t \times \alpha) + (EMA_{t-1} \times (1 - \alpha)) $$
    
    where $$ \alpha = \frac{2}{(periods + 1)} $$ is the smoothing factor.
    
    Args:
        prices (list): List of price values.
        periods (int): The number of periods for the EMA calculation.
        smoothing (float): The smoothing factor; commonly set to 2, which corresponds to the standard EMA formula.
        
    Returns:
        list: A list of EMA values, starting from the (periods)th element.
    """
    # Calculate the initial SMA for the first 'periods' prices
    ema = [sum(prices[:periods]) / periods]
    
    # Calculate the smoothing factor
    alpha = smoothing / (1 + periods)
    
    # Calculate the EMA for the remaining prices
    for price in prices[periods:]:
        ema.append((price * alpha) + (ema[-1] * (1 - alpha)))
    
    return ema



def handle_ajax_posts_bot(req, payload):

    if  req == 'bot_download':

        from dashboard.modules.bots.utilities.download_binance_data import download_binance_data

        download_binance_data()



    elif req == 'bot_draw_data':
        data = [{'epoch': x.epoch, 'price': x.price} for x in models_tick.Tick.objects.all().order_by('epoch')]

        # Assuming your model is named StoreVideoEventSummary and has an 'epoch' field
        # Convert epoch to datetime if necessary, or use TruncHour directly on the timestamp field




        minutely_data_groups = list(zip(*(iter(data),) * 3600))
        minutely_data = []
        for minutely_data_group in minutely_data_groups:
            minutely_data.append({
                'epoch':minutely_data_group[-1]['epoch'],
                # 'price': round(sum([x['price'] for x in minutely_data_group])/ len(minutely_data_group), 2)
                'price': minutely_data_group[-1]['price']
                
                })

        periods = 200
        minutely_ema = calculate_ema([x['price'] for x in minutely_data], periods=periods)
        minutely_ema = (periods-1) * [minutely_ema[0]] + minutely_ema

        assert len(minutely_ema) == len(minutely_data)

        # hourly_data_groups = list(zip(*(iter(minutely_data_groups),) * 60))   
        d=4




        return {
            'price':            [x['price'] for x in data],
            'epoch_seconds':    [x['epoch'] for x in data],

            'epoch_minutes':    [x['epoch'] for x in minutely_data],
            'minutely_ema':     minutely_ema
        }



    elif req == 'bot_import_data':
        models_tick.Tick.objects.all().delete()

        for root, dirs, files in os.walk(tk.bot_tmp_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                
                df = pd.read_csv(file_path, delimiter=',', header=None)

                # with open(file_path, 'r', encoding='utf-8') as file:

                    # csv_reader = csv.reader(file)

                model_instances = [models_tick.Tick(
                    epoch=int(row[0] / 1000),
                    price=row[4]) for _, row in df.iterrows()
                    ]

                models_tick.Tick.objects.bulk_create(model_instances)   


                
                # for row in tqdm(csv_reader):
                #     try:
                #         models_price.Price(
                #             epoch = int(row[0]) / 1000000,
                #             price = eval(row[4]),
                #         ).save()
                #     except:
                #         pass
                os.remove(file_path)