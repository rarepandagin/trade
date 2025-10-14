import pandas as pd
import numpy as np


class IndicatorsClass:
    def __init__(self, df):
        self.df = df

    
    def merge_and_fillna(self, indicator_name):
        self.df = self.df.merge(self.df_minutely_up_sampled_down_sampled[indicator_name],      on='epoch', how='left').set_axis(self.df.index)




    def calculate_indicators(self) -> pd.DataFrame:
            
        indicators = ['ema', 'macd', 'rsi', 'bb']
        ema_ranges = [200, 50, 26, 20, 12]
        minutes_time_frames = [60]
        

        # the price for the current minute is the price of the last second of the previous minute (closing)
        self.df['epoch'] =  pd.to_datetime(self.df.index / 1_000_000, unit='s')

        for minutes_time_frame in minutes_time_frames:

            df_minutely_up_sampled                                                              = self.df.resample(f'{minutes_time_frame}min', on='epoch').last().shift()


            """
            EMA
            """
            if 'ema' in indicators:
                for ema_range in ema_ranges:                
                    df_minutely_up_sampled[f'indicator_{minutes_time_frame}_ema_{ema_range}']      = df_minutely_up_sampled['price'].ewm(span=ema_range, adjust=False).mean()


            """
            MACD
            """
            if 'macd' in indicators:
                df_minutely_up_sampled[f'indicator_{minutes_time_frame}_macd']                     = df_minutely_up_sampled[f'indicator_{minutes_time_frame}_ema_12'] - df_minutely_up_sampled[f'indicator_{minutes_time_frame}_ema_26']
                df_minutely_up_sampled[f'indicator_{minutes_time_frame}_macd_signal']              = df_minutely_up_sampled[f'indicator_{minutes_time_frame}_macd'].ewm(span=9, adjust=False).mean()
                df_minutely_up_sampled[f'indicator_{minutes_time_frame}_macd_histogram']           = df_minutely_up_sampled[f'indicator_{minutes_time_frame}_macd'] - df_minutely_up_sampled[f'indicator_{minutes_time_frame}_macd_signal']



            """
            RSI
            """
            if 'rsi' in indicators:
                rsi_periods = 14
                price_diff = df_minutely_up_sampled['price'].diff()
                gain = price_diff.clip(lower=0)
                loss = -1 * price_diff.clip(upper=0)
                avg_gain = gain.rolling(window=rsi_periods).mean()
                avg_loss = loss.rolling(window=rsi_periods).mean()
                rs = avg_gain / avg_loss
                df_minutely_up_sampled[f'indicator_{minutes_time_frame}_rsi'] = 100 - (100 / (1 + rs))


            """
            BB
            """
            if 'bb' in indicators:
                bb_window = 20
                bb_num_of_std = 2

                # Calculate rolling mean and standard deviation
                rolling_mean = df_minutely_up_sampled['price'].rolling(window=bb_window).mean()
                rolling_std  = df_minutely_up_sampled['price'].rolling(window=bb_window).std()

                df_minutely_up_sampled[f'indicator_{minutes_time_frame}_bb_ub'] = rolling_mean + (rolling_std * bb_num_of_std)
                df_minutely_up_sampled[f'indicator_{minutes_time_frame}_bb_lb'] = rolling_mean - (rolling_std * bb_num_of_std)



            """
            Undoing the sampling
            """
            self.df_minutely_up_sampled_down_sampled                                                 = df_minutely_up_sampled.resample('s').asfreq()



            """
            Merge and Fillna 
            """

            # EMAs
            if 'ema' in indicators:
                for ema_range in ema_ranges:
                    self.merge_and_fillna(indicator_name=f'indicator_{minutes_time_frame}_ema_{ema_range}')


            # MACD
            if 'macd' in indicators:
                self.merge_and_fillna(indicator_name=f'indicator_{minutes_time_frame}_macd')
                self.merge_and_fillna(indicator_name=f'indicator_{minutes_time_frame}_macd_signal')
                self.merge_and_fillna(indicator_name=f'indicator_{minutes_time_frame}_macd_histogram')


            # RSI
            if 'rsi' in indicators:
                self.merge_and_fillna(indicator_name=f'indicator_{minutes_time_frame}_rsi')

            # BB
            if 'bb' in indicators:
                self.merge_and_fillna(indicator_name=f'indicator_{minutes_time_frame}_bb_ub')
                self.merge_and_fillna(indicator_name=f'indicator_{minutes_time_frame}_bb_lb')



            # df_minutely =   df.resample('1Min', on='epoch').last().shift()
            # df_minutely['indicator_ema_minutely_200'] = df_minutely['price'].ewm(span=200, adjust=False).mean()
            # df_minutely_up_sampled = df_minutely.resample('S').ffill()
            # df = df.merge(df_minutely_up_sampled['indicator_ema_minutely_200'],  on='epoch', how='left').set_axis(df.index)
            # df['indicator_ema_minutely_200'].fillna(method='ffill', inplace=True)   
            # df['indicator_ema_minutely_200'].fillna(method='bfill', inplace=True)   


        self.df = self.df.round(2)

        return self.df

        # except:
        #     try:
        #         tk.logger.info(format_exc())    
        #     except:
        #         pass

