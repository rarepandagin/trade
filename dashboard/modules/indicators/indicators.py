import os
from traceback import format_exc
from dashboard.views_pages import toolkit as tk
import pandas as pd

class IndicatorsClass:
    def __init__(self, df):
        self.df = df

    

    def merge_and_fillna(self, indicator_name):
        self.df = self.df.merge(self.df_minutely_up_sampled_down_sampled[indicator_name],      on='epoch', how='left').set_axis(self.df.index)
        self.df[indicator_name].fillna(method='ffill', inplace=True)   
        self.df[indicator_name].fillna(method='bfill', inplace=True)   
                

        

    def calculate_indicators(self) -> pd.DataFrame:
        # try:
            
            # the price for the current minute is the price of the last second of the previous minute (opening)
        self.df['epoch'] =   pd.to_datetime(self.df.index / 1_000_000, unit='s')

        ema_ranges = [200, 50, 26, 20, 12]

        for minutes_sample_size in [60]:

            df_minutely_up_sampled                                                              = self.df.resample(f'{minutes_sample_size}min', on='epoch').last().shift()


            """
            EMA
            """
            for ema_range in ema_ranges:                
                df_minutely_up_sampled[f'indicator_ema_{minutes_sample_size}_{ema_range}']      = df_minutely_up_sampled['price'].ewm(span=ema_range, adjust=False).mean()


            """
            MACD
            """
            df_minutely_up_sampled[f'indicator_macd_{minutes_sample_size}']                     = df_minutely_up_sampled[f'indicator_ema_{minutes_sample_size}_12'] - df_minutely_up_sampled[f'indicator_ema_{minutes_sample_size}_26']
            df_minutely_up_sampled[f'indicator_macd_signal_{minutes_sample_size}']              = df_minutely_up_sampled[f'indicator_macd_{minutes_sample_size}'].ewm(span=9, adjust=False).mean()
            df_minutely_up_sampled[f'indicator_macd_histogram_{minutes_sample_size}']           = df_minutely_up_sampled[f'indicator_macd_{minutes_sample_size}'] - df_minutely_up_sampled[f'indicator_macd_signal_{minutes_sample_size}']



            """
            RSI
            """
            rsi_periods = 14
            price_diff = df_minutely_up_sampled['price'].diff()
            gain = price_diff.clip(lower=0)
            loss = -1 * price_diff.clip(upper=0)
            avg_gain = gain.rolling(window=rsi_periods).mean()
            avg_loss = loss.rolling(window=rsi_periods).mean()
            rs = avg_gain / avg_loss
            # rs = gain / loss
            df_minutely_up_sampled[f'indicator_rsi_{minutes_sample_size}'] = 100 - (100 / (1 + rs))



            """
            Undoing the sampling
            """
            self.df_minutely_up_sampled_down_sampled                                                 = df_minutely_up_sampled.resample('S').ffill()



            """
            Merge and Fillna 
            """

            # EMAs
            for ema_range in ema_ranges:
                self.merge_and_fillna(indicator_name=f'indicator_ema_{minutes_sample_size}_{ema_range}')


            # MACD
            self.merge_and_fillna(indicator_name=f'indicator_macd_{minutes_sample_size}')
            self.merge_and_fillna(indicator_name=f'indicator_macd_signal_{minutes_sample_size}')
            self.merge_and_fillna(indicator_name=f'indicator_macd_histogram_{minutes_sample_size}')

            # RSI
            self.merge_and_fillna(indicator_name=f'indicator_rsi_{minutes_sample_size}')



            # df_minutely =   df.resample('1Min', on='epoch').last().shift()
            # df_minutely['indicator_ema_minutely_200'] = df_minutely['price'].ewm(span=200, adjust=False).mean()
            # df_minutely_up_sampled = df_minutely.resample('S').ffill()
            # df = df.merge(df_minutely_up_sampled['indicator_ema_minutely_200'],  on='epoch', how='left').set_axis(df.index)
            # df['indicator_ema_minutely_200'].fillna(method='ffill', inplace=True)   
            # df['indicator_ema_minutely_200'].fillna(method='bfill', inplace=True)   

        return self.df

        # except:
        #     try:
        #         tk.logger.info(format_exc())    
        #     except:
        #         pass

