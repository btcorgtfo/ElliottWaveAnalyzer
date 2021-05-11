from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Union
from abc import ABC, abstractmethod
from numba import njit, vectorize
from numba.experimental import jitclass

@njit
def next_max_np(arr, idx_start: int = 0, prev_high: float = 0):
    """
    Given idx_start (and a previous high), this returns the next high, high_idx

    :param idx_start:
    :param prev_high:
    :return:
    """
    high = arr[idx_start]
    high_idx = idx_start

    if prev_high == 0:
        prev_high = high

    prev_high_reached = False
    for idx in range(idx_start + 1, len(arr)):
        act_high = arr[idx]
        if act_high < prev_high and not prev_high_reached:
            high = act_high
            high_idx = idx

        elif act_high > high:
            prev_high_reached = True
            high = act_high
            high_idx = idx
        else:
            return high, high_idx

    return high, high_idx


def next_min_np(arr, idx_start, prev_low):
    low_idx = idx_start
    low = arr[idx_start]

    if prev_low == 0:
        prev_low = low

    prev_low_reached = False
    for idx in range(idx_start + 1, len(arr)):

        act_low = arr[idx]
        if act_low > prev_low and not prev_low_reached:
            low = act_low
            low_idx = idx

        elif act_low < low:
            prev_low_reached = True
            low = act_low
            low_idx = idx
        else:
            return low, low_idx

    return None, None


class WaveRule(ABC):
    def __init__(self, name: str):
        self.name = name
        self.conditions = self.set_conditions()

    @abstractmethod
    def set_conditions(self):
        pass

    def __repr__(self):
        return str(self.conditions)


class MonoWave:
    def __init__(self,
                 highs_arr: np.array,
                 lows_arr: np.array,
                 dates_arr: np.array,
                 idx_start,
                 skip_n: int = 0):

        self.highs_arr = highs_arr
        self.lows_arr = lows_arr
        self.dates_arr = dates_arr
        self.skip_n = skip_n
        self.idx_start = idx_start

        self.count = int  # the count of the monowave, e.g. 1, 2, A, B, etc
        self.degree = int  # 1 = lowest timeframe level, 2 as soon as a e.g. 12345 is found etc.

        self.__date_start = str
        self.__date_end = str

        self.__low = float
        self.__high = float
        self.__low_idx = int
        self.__high_idx = int
        self.__length = float
        self.__duration = int

    def find_end(self):
        pass

    def next_max_np(self, idx_start: int = 0, prev_high: float = 0):
        """
        Given idx_start (and a previous high), this returns the next high, high_idx

        :param idx_start:
        :param prev_high:
        :return:
        """
        high = self.highs_arr[idx_start]
        high_idx = idx_start

        if prev_high == 0:
            prev_high = high

        prev_high_reached = False
        for idx in range(idx_start + 1, len(self.highs_arr)):
            act_high = self.highs_arr[idx]
            if act_high < prev_high and not prev_high_reached:
                high = act_high
                high_idx = idx

            elif act_high > high:
                prev_high_reached = True
                high = act_high
                high_idx = idx
            else:
                return high, high_idx

        return high, high_idx

    def next_min_np(self, idx_start, prev_low):
        low_idx = idx_start
        low = self.lows_arr[idx_start]

        if prev_low == 0:
            prev_low = low

        prev_low_reached = False
        for idx in range(idx_start + 1, len(self.lows_arr)):
            act_low = self.lows_arr[idx]
            if act_low > prev_low and not prev_low_reached:
                low = act_low
                low_idx = idx

            elif act_low < low:
                prev_low_reached = True
                low = act_low
                low_idx = idx
            else:
                return low, low_idx

        return None, None

    @property
    def date_start(self):
        return self.__date_start

    @property
    def date_end(self):
        return self.__date_end

    @property
    def dates(self) -> list:
        return [self.date_start, self.date_end]

    @property
    def points(self):
        return self.low, self.high

    @property
    def low(self):
        return self.__low

    @property
    def high(self):
        return self.__high

    @property
    def low_idx(self):
        return self.__low_idx

    @property
    def high_idx(self):
        return self.__high_idx

    @property
    def length(self):
        return self.__length

    @property
    def duration(self):
        return self.__duration


class MonoWaveUp:
    """
    Describes a upwards movement, which can have [skip_n] smaller downtrends
    """

    def __init__(self,
                 df: pd.DataFrame,
                 idx_start,
                 skip_n: int = 0):

        self.df = df
        self.highs_arr = np.array(list(self.df['High']))
        self.lows_arr = np.array(list(self.df['Low']))
        self.skip_n = skip_n
        self.count = int
        self.label = str

        self.idx_start = idx_start

        self.__high, self.idx_end = self.find_end(self.idx_start)

        if self.__high is not None:
            self.__low = self.df.loc[idx_start]['Low']

            self.__date_start = df.loc[self.idx_start]['Date']
            self.__date_end = df.loc[self.idx_end]['Date']

            self.__duration = abs(self.idx_end - self.idx_start)
            self.__length = abs(self.__high - self.__low)

    @property
    def date_start(self):
        return self.__date_start

    @property
    def date_end(self):
        return self.__date_end

    @property
    def dates(self) -> list:
        return [self.date_start, self.date_end]

    @property
    def points(self):
        return self.low, self.high

    @property
    def low(self):
        return self.__low

    @property
    def high(self):
        return self.__high

    @property
    def length(self):
        return self.__length

    @property
    def duration(self):
        return self.__duration

    def find_end(self, idx_start: int):
        """
        Finds the end of this MonoWave

        :param idx_start:
        :return:
        """
        high, high_idx = next_max_np(self.highs_arr, idx_start)
        low_at_start = self.lows_arr[idx_start]

        if high is None:
            return None, None

        for _ in range(self.skip_n):

            act_high, act_high_idx = next_max_np(self.highs_arr, high_idx, high)
            if act_high is None:
                return None, None

            if act_high > high:
                high = act_high
                high_idx = act_high_idx
                if np.min(self.lows_arr[idx_start:act_high_idx] < low_at_start):
                    return None, None

        return high, high_idx


class MonoWaveDown:
    def __init__(self,
                 df: pd.DataFrame,
                 idx_start,
                 skip_n: int = 0):

        self.df = df
        self.lows_arr = np.array(list(self.df['Low']))
        self.highs_arr = np.array(list(self.df['High']))
        self.skip_n = skip_n
        self.count = int
        self.label = str
        self.idx_start = idx_start

        self.__low, self.idx_end = self.find_end(self.idx_start)

        if self.__low is not None:
            self.__high = self.df.loc[idx_start]['High']

            self.__date_start = df.loc[self.idx_start]['Date']
            self.__date_end = df.loc[self.idx_end]['Date']

            self.__duration = abs(self.idx_end - self.idx_start)
            self.__length = abs(self.__high - self.__low)

    @property
    def dates(self) -> list:
        return [self.date_start, self.date_end]

    @property
    def points(self):
        return self.high, self.low

    @property
    def date_start(self):
        return self.__date_start

    @property
    def date_end(self):
        return self.__date_end

    @property
    def low(self):
        return self.__low

    @property
    def high(self):
        return self.__high

    @property
    def length(self):
        return self.__length

    @property
    def duration(self):
        return self.__duration

    def find_end(self, idx_start: int):
        """
        Finds the end of this MonoWaveUp

        :param idx_start:
        :return:
        """

        low, low_idx = next_min_np(self.lows_arr, idx_start, 0)
        high_at_start = self.highs_arr[idx_start]

        if low is None:
            return None, None

        for _ in range(self.skip_n):

            act_low, act_low_idx = next_min_np(self.lows_arr, low_idx, low)
            #print(_, 'act_low:', act_low, 'low:', low, 'low_idx:', low_idx)
            if act_low is None:
                return None, None

            if act_low < low:
                low = act_low
                low_idx = act_low_idx
                if np.max(self.highs_arr[idx_start:act_low_idx]) > high_at_start:
                    return None, None

            #TODO what to do if no more minima can be found?
            #if act_low > low:
            #    return None, None

        return low, low_idx


class WaveAnalyzer:
    """
    Find impulse or corrective waves for given dataframe
    """
    def __init__(self,
                 df: pd.DataFrame,
                 verbose: bool = False):

        self.df = df
        self.verbose = verbose

    def find_impulsive_wave(self,
                            idx_start: int,
                            wave_config: list = None):
        # first wave, start at first low in the data

        if wave_config is None:
            wave_config = [0, 0, 0, 0, 0]

        wave1 = MonoWaveUp(self.df, idx_start=idx_start, skip_n=wave_config[0])
        wave1.label = '1'
        wave1_end = wave1.idx_end
        if wave1_end is None:
            if self.verbose: print("Wave 1 has no End in Data")
            return False

        wave2 = MonoWaveDown(self.df, idx_start=wave1_end, skip_n=wave_config[1])
        wave2.label = '2'
        wave2_end = wave2.idx_end
        if wave2_end is None:
            if self.verbose: print("Wave 2 has no End in Data")
            return False

        wave3 = MonoWaveUp(self.df, idx_start=wave2_end, skip_n=wave_config[2])
        wave3.label = '3'
        wave3_end = wave3.idx_end
        if wave3_end is None:
            if self.verbose: print("Wave 3 has no End in Data")
            return False

        wave4 = MonoWaveDown(self.df, idx_start=wave3_end, skip_n=wave_config[3])
        wave4.label = '4'
        wave4_end = wave4.idx_end

        if wave4_end is None:
            if self.verbose: print("Wave 4 has no End in Data")
            return False

        wave5 = MonoWaveUp(self.df, idx_start=wave4_end, skip_n=wave_config[4])
        wave5.label = '5'
        wave5_end = wave4.idx_end
        if wave5_end is None:
            if self.verbose: print("Wave 5 has no End in Data")
            return False

        return [wave1, wave2, wave3, wave4, wave5]

    def find_corrective_wave(self,
                             idx_start: int,
                             wave_config: list = None):
        if wave_config is None:
            wave_config = [0, 0, 0]

        waveA = MonoWaveDown(self.df, idx_start=idx_start, skip_n=wave_config[0])
        waveA.label = 'A'
        waveA_end = waveA.idx_end
        if waveA_end is None:
            return False

        waveB = MonoWaveUp(self.df, idx_start=waveA_end, skip_n=wave_config[1])
        waveB.label = 'B'
        waveB_end = waveB.idx_end
        if waveB_end is None:
            return False

        waveC = MonoWaveDown(self.df, idx_start=waveB_end, skip_n=wave_config[2])
        waveC.label = 'C'
        waveC_end = waveC.idx_end
        if waveC_end is None:
            return False

        return [waveA, waveB, waveC]

    def find_td_wave(self, idx_start: int, wave_config: list = None):
        if wave_config is None:
            wave_config = [0, 0]

        wave1 = MonoWaveUp(self.df, idx_start=idx_start, skip_n=wave_config[0])
        wave1.label = '1'
        wave1_end = wave1.idx_end
        if wave1_end is None:
            if self.verbose: print("Wave 1 has no End in Data")
            return False

        wave2 = MonoWaveDown(self.df, idx_start=wave1_end, skip_n=wave_config[1])
        wave2.label = '2'
        wave2_end = wave2.idx_end
        if wave2_end is None:
            if self.verbose: print("Wave 2 has no End in Data")
            return False

        return [wave1, wave2]

    def run(self):
        pass

class Impulse(WaveRule):
    """
    Das Ende der zweiten Welle kommt nie über den Anfang der ersten Welle;
    Die dritte Welle erstreckt sich immer jenseits der Spitze der ersten Welle;
    Das Ende der vierten Welle kommt nie über nie die Spitze der ersten Welle;
    Die dritte Welle ist niemals die kürzeste aller agierenden Wellen;

    Die dritte Welle ist immer ein Impuls;
    Die erste Welle ist entweder ein Impuls oder eine führende Diagonale;
    Die fünfte Welle kann entweder ein Impuls oder eine Diagonale sein;
    Die zweite Welle könnte die Form jeder Korrekturwelle annehmen, jedoch nie zu einem Dreieck werden;
    Die vierte Welle könnte die Form jeder Korrekturwelle annehmen.

    """
    def set_conditions(self):
        # conditon returns TRUE -> no exit
        conditions = {# WAVE 2
                      'w2_1': {'waves': ['wave1', 'wave2'],
                             'function': lambda wave1, wave2: wave2.low > wave1.low,
                             'message': 'End of Wave2 is lower than Start of Wave1.'},

                      'w2_2': {'waves': ['wave1', 'wave2'],
                             'function': lambda wave1, wave2: wave2.length >= 0.2 * wave1.length,
                             'message': 'Wave2 is shorten than 20% of Wave1.'},

                      'w2_3': {'waves': ['wave1', 'wave2'],
                             'function': lambda wave1, wave2: 9 * wave2.duration > wave1.duration,
                             'message': 'Wave2 is longer than 9x Wave1'},

                      # WAVE 3
                      'w3_1': {'waves': ['wave1', 'wave3', 'wave5'],
                             'function': lambda wave1, wave3, wave5: not (
                                       wave3.length < wave5.length and wave3.length < wave1.length),
                             'message': 'Wave3 is the shortest Wave.'},

                      'w3_2': {'waves': ['wave1', 'wave3'],
                             'function': lambda wave1, wave3: wave3.high > wave1.high,
                             'message': 'End of Wave3 is lower than End of Wave1'},

                      'w3_3': {'waves': ['wave1', 'wave3'],
                             'function': lambda wave1, wave3: wave3.length >= wave1.length / 3.,
                             'message': 'Wave3 is shorter than 1/3 of Wave1'},

                      'w3_4': {'waves': ['wave2', 'wave3'],
                             'function': lambda wave2, wave3: wave3.length > wave2.length,
                             'message': 'Wave3 shorter than Wave2'},

                      'w3_5': {'waves': ['wave1', 'wave3'],
                            'function': lambda wave1, wave3: 7 * wave3.duration > wave1.duration,
                            'message': 'Wave3 more than 7 times longer than Wave1.'},

                      # WAVE 4
                      'w4_1': {'waves': ['wave1', 'wave4'],
                             'function': lambda wave1, wave4: wave4.low > wave1.high,
                             'message': 'End of Wave4 is lower than End of Wave1'},

                      # WAVE 5
                      'w5_1': {'waves': ['wave3', 'wave5'],
                               'function': lambda wave3, wave5: wave3.high < wave5.high,
                               'message': 'End of Wave5 is lower than End of Wave3'},
                      }

        return conditions


class TDWave(WaveRule):
    def set_conditions(self):
        # conditon returns TRUE -> no exit
        conditions = {# WAVE 2
                      'w2_1': {'waves': ['wave1', 'wave2'],
                             'function': lambda wave1, wave2: wave2.length > wave1.length * 0.59,
                             'message': 'End of Wave2 corrected less  50% of Wave1.'},

                        'w2_2': {'waves': ['wave1', 'wave2'],
                         'function': lambda wave1, wave2: wave2.length < wave1.length * 0.64,
                         'message': 'End of Wave2 corrected more than 65% of Wave1.'},

                        'w2_3': {'waves': ['wave1', 'wave2'],
                         'function': lambda wave1, wave2: 9 * wave2.duration > wave1.duration,
                         'message': 'Wave2 is longer than 9x Wave1'},
        }

        return conditions


class WavePattern:
    def __init__(self, waves: list, verbose: bool = False):
        self.__waves = waves
        self.__verobse = verbose

        __waves_dict = dict()
        for i, wave in enumerate(self.__waves):
            #TODO if len waves = 3 -> map 1 - a etc

            key = f'wave{i+1}'
            __waves_dict.setdefault(key, wave)

        self.waves = __waves_dict

    def check_rule(self, waverule: WaveRule) -> bool:

        for rule, conditions in waverule.conditions.items():

            no_of_waves = len(conditions.get('waves'))
            function = conditions.get('function')
            message = conditions.get('message')

            if no_of_waves == 2:
                wave1 = self.waves.get(conditions.get('waves')[0])
                wave2 = self.waves.get(conditions.get('waves')[1])

                #
                # if rule == "w2_2":
                #     print("da", wave1.length, 0.2* wave1.length, wave2.length, function)

                if not function(wave1, wave2):
                    if self.__verobse:
                        print(f'Rule Violation of {waverule.name} for condition {rule}: {message}')
                    return False

            elif no_of_waves == 3:
                wave1 = self.waves.get(conditions.get('waves')[0])
                wave2 = self.waves.get(conditions.get('waves')[1])
                wave3 = self.waves.get(conditions.get('waves')[2])

                if not function(wave1, wave2, wave3):
                    if self.__verobse:
                        print(f'Rule Violation of {waverule.name} for condition {rule}: {message}')
                    return False
            else:
                raise NotImplementedError('other than 2 or 3 waves as argument not implemented')

        return True

    @property
    def dates(self):
        dates = list()
        for wave_no, wave in self.waves.items():
            dates.extend(wave.dates)

        return dates

    @property
    def values(self):
        values = list()
        for wave_no, wave in self.waves.items():
            if isinstance(wave, MonoWaveUp):
                values.extend([wave.low, wave.high])
            elif isinstance(wave, MonoWaveDown):
                values.extend([wave.high, wave.low])
            else:
                raise NotImplementedError()

        return values

    @property
    def labels(self):
        labels = list()
        reference_length = next(iter(self.waves.items()))[1].length

        for wave_no, wave in self.waves.items():
            #labels.extend([" ", f'{wave.label}({round(wave.length,0)})'])
            if wave.label in ['B', '2', '3']:
                labels.extend([" ", f'{wave.label} ({round(wave.length/reference_length, 3)})'])
            else:
                labels.extend([" ", f'{wave.label}'])
            length = wave.length
        return labels


class WaveOptions:
    def __init__(self, i: int, j: int = None, k: int = None, l: int = None, m: int = None):
        self.i = i
        self.j = j
        self.k = k
        self.l = l
        self.m = m

    @property
    def values(self):
        if self.k is not None:
            return [self.i, self.j, self.k, self.l, self.m]
        else:
            return [self.i, self.j]

    def __hash__(self):
        if self.k is not None:
            hash_str = f'{self.i}_{self.j}_{self.k}_{self.l}_{self.m}'
        else:
            hash_str = f'{self.i}_{self.j}'
        return hash(hash_str)

    def __eq__(self, other):
        if self.k is not None:
            if self.i == other.i and self.j == other.j and self.k == other.k and self.l == other.l and self.m == other.m:
                return True
            else:
                return False
        else:
            if self.i == other.i and self.j == other.j:
                return True
            else:
                return False
