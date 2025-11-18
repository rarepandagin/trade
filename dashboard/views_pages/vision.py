from traceback import format_exc
from dashboard.views_pages import toolkit as tk
import json
import copy
from dashboard.models.models_adminsettings import *


unclear_direction               = "unclear_direction"

ema_group_shows_absolutely_bullish_direction    = "ema_group_shows_absolutely_bullish_direction"
ema_group_shows_absolutely_bearish_direction    = "ema_group_shows_absolutely_bearish_direction"

ema_group_shows_mostly_bullish_direction        = "ema_group_shows_mostly_bullish_direction"
ema_group_shows_mostly_bearish_direction        = "ema_group_shows_mostly_bearish_direction"

def populate_list_by_index(items):
    ret = []
    for i in range(len(items)):
        ret += (i + 1) * (i + 1) * [items[i]]
    return ret


def count_and_describe_direction_of_ema_group(items):

    n = len(items)
    plus_counts = len([x for x in items if x >= 0])
    minus_counts = len([x for x in items if x < 0])

    ret = unclear_direction

    if plus_counts == n:
        ret = ema_group_shows_absolutely_bullish_direction
    
    elif minus_counts == n:
        ret = ema_group_shows_absolutely_bearish_direction
    
    elif (plus_counts / n) > 0.5:
        ret = ema_group_shows_mostly_bullish_direction
    
    elif (minus_counts / n) > 0.5:
        ret = ema_group_shows_mostly_bearish_direction

    return ret


def find_longest_ascending_sequence(arr):
    
    longest_start = longest_end = start = 0
    
    for i in range(1, len(arr)):
        if arr[i] < arr[i - 1]:
            start = i
        elif i - start > longest_end - longest_start:
            longest_start, longest_end = start, i
    
    return arr[longest_start:longest_end + 1]   


unclear_ema_lineup = "unclear_ema_lineup"
ema_lineup_shows_full_bullish_alignment = "ema_lineup_shows_full_bullish_alignment"
ema_lineup_shows_some_bullish_alignment = "ema_lineup_shows_some_bullish_alignment"
ema_lineup_shows_full_bearish_alignment = "ema_lineup_shows_full_bearish_alignment"
ema_lineup_shows_some_bearish_alignment = "ema_lineup_shows_some_bearish_alignment"


def count_and_describe_lineup(items):
    longest_ascending_sequence  = find_longest_ascending_sequence(items)
    longest_descending_sequence = find_longest_ascending_sequence([-x for x in items])

    n = len(items)

    n_asc = len(longest_ascending_sequence)
    n_des = len(longest_descending_sequence)

    ret = unclear_ema_lineup
    if n == n_asc:
        ret = ema_lineup_shows_full_bearish_alignment
    elif n_asc > (n / 2):
        ret = ema_lineup_shows_some_bearish_alignment
    
    elif n == n_des:
        ret = ema_lineup_shows_full_bullish_alignment
    elif n_des > (n / 2):
        ret = ema_lineup_shows_some_bullish_alignment
    
    return ret



weak = 'weak'
strong = 'strong'

pro     = "pro"
against = "against"

long   = "long" 
short  = "short" 



class Observation:
    def __init__(self, indicator, description) -> None:
        self.indicator = indicator
        self.description = description

    def declare(self, trade, bias, minute, strength):
        self.table[trade][bias].append([minute, strength])
        self.declared = True

    def reset(self):
        self.table = {
                long:  {pro:[], against:[]},
                short: {pro:[], against:[]},
            }
        self.declared = False



observation_ema_current_direction    = Observation(indicator="ema",               description="EMA current direction")

observation_emas_lineup              = Observation(indicator="ema",               description="EMA line up")

observation_macd_hist                = Observation(indicator="macd_histogram",    description="MACD histogram")
observation_macd                     = Observation(indicator="macd",              description="MACD line")


# observation_macd_hist_is_ok                 = Observation(indicator="macd_histogram",    description="MACD hist is ok")
# observation_macd_hist_is_not_ok             = Observation(indicator="macd_histogram",    description="MACD hist is not ok")


class Vision:
    def __init__(self):
        
        self.ema_lags = [12, 20, 26, 50, 200]
        self.ema_lags_for_lineup = [20, 50, 200]

        self.slow_lags = [50, 200]
        self.fast_lags = [12, 20, 26]

        self.ema_lag_direction = {}
        self.ema_lineup = {}
        self.ema_200_comparison = {}

        self.observations = [
            observation_ema_current_direction,
            observation_emas_lineup,
            observation_macd_hist,
            observation_macd,
        ]



        self.observations_pro_long      = []
        self.observations_pro_short     = []
        self.observations_against_long  = []
        self.observations_against_short = []


        self.observations_pro_long_strong_count      = 0
        self.observations_pro_short_strong_count     = 0
        self.observations_against_long_strong_count  = 0
        self.observations_against_short_strong_count = 0



    def serialize(self):
        return {
            'ema_lag_direction': self.ema_lag_direction,
            'ema_lineup': self.ema_lineup,
            'ema_200_comparison': self.ema_200_comparison,

            'observations_pro_long': [x.__dict__ for x in self.observations_pro_long],
            'observations_pro_short': [x.__dict__ for x in self.observations_pro_short],
            'observations_against_long': [x.__dict__ for x in self.observations_against_long],
            'observations_against_short': [x.__dict__ for x in self.observations_against_short],
        }

    def look_around(self):

        admin_settings = tk.get_admin_settings()

        live_indicators = admin_settings.live_indicators

        for observation in self.observations:
            observation.reset()


        """
        EMA
        """

        """
        # direction
        For every time-frame determine:
            determine if the ema-200 is rising or falling

            this explains if you should be looking for shorts or longs in each time frame


            here we count the number of ascending and descending EMA for a given time frame
            this is only to compare the current and previous time step
            it tells us if, right now, the EMA values are rising or falling
            it also categorizes the EMAs into slow and fast


        """
        for minute in admin_settings.MINUTES:
            slow_lags_directions = [live_indicators[f'minutes_{minute}'][f'ema_{lag}']['d'] for lag in self.slow_lags]
            fast_lags_directions = [live_indicators[f'minutes_{minute}'][f'ema_{lag}']['d'] for lag in self.fast_lags]

            slow_lags_directions_populated = populate_list_by_index(slow_lags_directions)
            fast_lags_directions_populated = populate_list_by_index(fast_lags_directions)

            slow_lags_directions_description = count_and_describe_direction_of_ema_group(slow_lags_directions_populated)
            fast_lags_directions_description = count_and_describe_direction_of_ema_group(fast_lags_directions_populated)

            self.ema_lag_direction[minute] = {
                'slow': slow_lags_directions_description,
                'fast': fast_lags_directions_description,
            }


            # observationING
            if (
                slow_lags_directions_description in [ema_group_shows_absolutely_bullish_direction, ema_group_shows_mostly_bullish_direction]
                ) and (
                fast_lags_directions_description in [ema_group_shows_absolutely_bullish_direction, ema_group_shows_mostly_bullish_direction]
                ) :

                observation_ema_current_direction.declare(trade=long, bias=pro, minute=minute, strength=weak)

            else:
                observation_ema_current_direction.declare(trade=long, bias=against, minute=minute, strength=strong)

            if (
                slow_lags_directions_description in [ema_group_shows_absolutely_bearish_direction, ema_group_shows_mostly_bearish_direction]
                ) and (
                fast_lags_directions_description in [ema_group_shows_absolutely_bearish_direction, ema_group_shows_mostly_bearish_direction]
                ) :
                observation_ema_current_direction.declare(trade=short, bias=pro, minute=minute, strength=weak)
            else:
                observation_ema_current_direction.declare(trade=short, bias=against, minute=minute, strength=strong)





            lag_values = [live_indicators[f'minutes_{minute}'][f'ema_{lag}']['v'] for lag in self.ema_lags_for_lineup]

            ema_lineup_description = count_and_describe_lineup(lag_values)
            self.ema_lineup[minute] = ema_lineup_description
            if ema_lineup_description == ema_lineup_shows_full_bearish_alignment:
                observation_emas_lineup.declare(bias=pro,   trade=short,    strength=strong,    minute=minute)
                observation_emas_lineup.declare(bias=against,   trade=long, strength=strong,    minute=minute)

            elif ema_lineup_description == ema_lineup_shows_full_bullish_alignment:
                observation_emas_lineup.declare(bias=pro,   trade=long,      strength=strong,    minute=minute)
                observation_emas_lineup.declare(bias=against,   trade=short, strength=strong,    minute=minute)


            if live_indicators[f'minutes_{minute}']['macd']['v'] > 0 and live_indicators[f'minutes_{minute}']['macd']['d'] > 0:
                observation_macd.declare(bias=pro,   trade=long,      strength=strong,    minute=minute)
                observation_macd.declare(bias=against,   trade=short, strength=strong,    minute=minute)

            elif live_indicators[f'minutes_{minute}']['macd']['v'] < 0 and live_indicators[f'minutes_{minute}']['macd']['d'] < 0:
                observation_macd.declare(bias=against,   trade=long,      strength=strong,    minute=minute)
                observation_macd.declare(bias=pro,       trade=short,     strength=strong,    minute=minute)




            # self.ema_200_comparison[minute] = 'above' if admin_settings.prices['weth'] > live_indicators[f'minutes_{minute}'][f'ema_200']['v'] else 'below'


        """
        # support/resistance

        For every time-frame determine:
            which ema-lag is acting as a support/resistance? (20, 50, or 200)
        """


        """
        # cross over

        do the three lags line up? (i.e., 20-50-200 or the reverse)

        a lineup indicates strength of a trend
        """




        """
        MACD
        """
        for minute in admin_settings.MINUTES:

            macd_histogram_value = live_indicators[f'minutes_{minute}']['macd_histogram']['v']
            macd_histogram_direction = live_indicators[f'minutes_{minute}']['macd_histogram']['d']

            if (macd_histogram_value > 0) and (macd_histogram_direction == '+'):

                observation_macd_hist.declare(bias=pro,     trade=long,  strength=strong,   minute=minute)
                observation_macd_hist.declare(bias=against, trade=short, strength=strong,   minute=minute)



            elif (macd_histogram_value < 0) and (macd_histogram_direction == '-'):
                
                observation_macd_hist.declare(bias=pro,     trade=short,    strength=strong,   minute=minute)
                observation_macd_hist.declare(bias=against, trade=long,     strength=strong,   minute=minute)


            else:

                if macd_histogram_value > 0:
                    observation_macd_hist.declare(bias=pro,     trade=long,     strength=weak, minute=minute)
                    observation_macd_hist.declare(bias=against, trade=short,    strength=weak, minute=minute)


                else:
                    observation_macd_hist.declare(bias=against,     trade=long,     strength=weak, minute=minute)
                    observation_macd_hist.declare(bias=pro,         trade=short,    strength=weak, minute=minute)




        for observation in self.observations:
            
            if observation.declared:
            
                for trade in [long, short]:
            
                    for bias in [pro, against]:

                        if len(observation.table[trade][bias]) > 0:

                            if trade == long:
                                if bias == pro:
                                    self.observations_pro_long.append(observation)
                                    self.observations_pro_long_strong_count += len([x for x in observation.table[trade][bias] if x[1]==strong])

                                elif bias == against:
                                    self.observations_against_long.append(observation)
                                    self.observations_against_long_strong_count += len([x for x in observation.table[trade][bias] if x[1]==strong])
                            
                            elif trade == short:
                                if bias == pro:
                                    self.observations_pro_short.append(observation)
                                    self.observations_pro_short_strong_count += len([x for x in observation.table[trade][bias] if x[1]==strong])

                                elif bias == against:
                                    self.observations_against_short.append(observation)
                                    self.observations_against_short_strong_count += len([x for x in observation.table[trade][bias] if x[1]==strong])

        

        old_vision_consensus = copy.deepcopy(admin_settings.vision_consensus)

        new_vision_consensus = vision_consensus_unsure





        if self.observations_pro_long_strong_count > 0 and self.observations_against_long_strong_count == 0:
            new_vision_consensus = vision_consensus_pro_long

        elif self.observations_pro_short_strong_count > 0 and self.observations_against_short_strong_count == 0:
            new_vision_consensus = vision_consensus_pro_short

        if new_vision_consensus != old_vision_consensus:
            if new_vision_consensus in [vision_consensus_pro_long , vision_consensus_pro_short]:
                pass
                # tk.create_new_notification("New consensus", f"consensus changed from {old_vision_consensus} to {new_vision_consensus}")


        tk.update_admin_settings('vision_consensus', new_vision_consensus)