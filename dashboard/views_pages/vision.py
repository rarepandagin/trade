from traceback import format_exc
from dashboard.views_pages import toolkit as tk
import json
import copy
from enum import StrEnum


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
    plus_counts = items.count('+')
    minus_counts = items.count('-')

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



def count_and_describe_lineup(items):
    longest_ascending_sequence  = find_longest_ascending_sequence(items)
    longest_descending_sequence = find_longest_ascending_sequence([-x for x in items])

    n = len(items)

    n_asc = len(longest_ascending_sequence)
    n_des = len(longest_descending_sequence)

    ret = 'not aligned'
    if n == n_asc:
        ret = 'full bearish alignment'
    elif n_asc > (n / 2):
        ret = 'some bearish alignment'
    
    elif n == n_des:
        ret = 'full bullish alignment'
    elif n_des > (n / 2):
        ret = 'some bullish alignment'
    
    return ret



reason_strength_weak = 'reason_strength_weak'
reason_strength_strong = 'reason_strength_strong'


class Reason:
    def __init__(self, strength, description, minute) -> None:
        self.strength = strength
        self.description = description
        self.minute = minute


class Vision:
    def __init__(self):
        
        self.ema_lags = [12, 20, 26, 50, 200]

        self.slow_lags = [50, 200]
        self.fast_lags = [12, 20, 26]

        self.ema_lag_direction = {}
        self.ema_lineup = {}
        self.ema_200_comparison = {}

        self.reasons_pro_long = []
        self.reasons_pro_short = []

        self.reasons_against_long = []
        self.reasons_against_short = []



    def serialize(self):
        return {
            'ema_lag_direction': self.ema_lag_direction,
            'ema_lineup': self.ema_lineup,
            'ema_200_comparison': self.ema_200_comparison,

            'reasons_pro_long': [x.__dict__ for x in self.reasons_pro_long],
            'reasons_pro_short': [x.__dict__ for x in self.reasons_pro_short],
            'reasons_against_long': [x.__dict__ for x in self.reasons_against_long],
            'reasons_against_short': [x.__dict__ for x in self.reasons_against_short],
        }

    def look_around(self):

        admin_settings = tk.get_admin_settings()

        live_indicators = admin_settings.live_indicators

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


            # REASONING
            if (
                slow_lags_directions_description in [ema_group_shows_absolutely_bullish_direction, ema_group_shows_mostly_bullish_direction]
                ) and (
                fast_lags_directions_description in [ema_group_shows_absolutely_bullish_direction, ema_group_shows_mostly_bullish_direction]
                ) :
                self.reasons_pro_long.append(    Reason(strength=reason_strength_weak,   description="EMAs indicate bullish trend", minute=minute))
            else:
                self.reasons_against_long.append(Reason(strength=reason_strength_strong, description="EMAs do not indicate bullish trend", minute=minute))

            if (
                slow_lags_directions_description in [ema_group_shows_absolutely_bearish_direction, ema_group_shows_mostly_bearish_direction]
                ) and (
                fast_lags_directions_description in [ema_group_shows_absolutely_bearish_direction, ema_group_shows_mostly_bearish_direction]
                ) :
                self.reasons_pro_short.append(    Reason(strength=reason_strength_weak,   description="EMAs indicate bearish trend", minute=minute))
            else:
                self.reasons_against_short.append(Reason(strength=reason_strength_strong, description="EMAs do not indicate bearish trend", minute=minute))





            lag_values = [live_indicators[f'minutes_{minute}'][f'ema_{lag}']['v'] for lag in self.ema_lags]

            self.ema_lineup[minute] = count_and_describe_lineup(lag_values)


            self.ema_200_comparison[minute] = 'above' if admin_settings.prices['weth'] > live_indicators[f'minutes_{minute}'][f'ema_200']['v'] else 'below'
            

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
                self.reasons_pro_long.append(Reason(strength=reason_strength_strong,   description="MACD hist fully agrees with long", minute=minute))
                self.reasons_against_short.append(Reason(strength=reason_strength_strong,   description="MACD hist fully disagrees with shorting", minute=minute))

            elif (macd_histogram_value < 0) and (macd_histogram_direction == '-'):
                self.reasons_against_long.append(Reason(strength=reason_strength_strong,   description="MACD hist fully disagrees with long", minute=minute))
                self.reasons_pro_short.append(Reason(strength=reason_strength_strong,   description="MACD hist fully agrees with shorting", minute=minute))

            else:

                if macd_histogram_value > 0:
                    self.reasons_pro_long.append(Reason(strength=reason_strength_weak,   description="MACD hist is ok with long", minute=minute))
                    self.reasons_against_short.append(Reason(strength=reason_strength_weak,   description="MACD hist is not ok with shorting", minute=minute))

                else:
                    self.reasons_against_long.append(Reason(strength=reason_strength_weak,   description="MACD hist is not ok with long", minute=minute))
                    self.reasons_pro_short.append(Reason(strength=reason_strength_weak,   description="MACD hist is ok with shorting", minute=minute))



    def generate_reasons(self):
        pass