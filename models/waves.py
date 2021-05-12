import numpy as np
from numba.experimental import jitclass
from models.waverules import WaveRule
from models.functions import hi, lo, next_hi, next_lo

class MonoWave:
    def __init__(self,
                 lows: np.array,
                 highs: np.array,
                 dates: np.array,
                 idx_start: int,
                 skip: int = 0):

        self.lows_arr = lows
        self.highs_arr = highs
        self.dates_arr = dates
        self.skip_n = skip
        self.idx_start = idx_start
        self.idx_end = int

        self.count = int  # the count of the monowave, e.g. 1, 2, A, B, etc
        self.degree = int  # 1 = lowest timeframe level, 2 as soon as a e.g. 12345 is found etc.

        self.date_start = str
        self.date_end = str

        self.low = float
        self.high = float
        self.low_idx = int
        self.high_idx = int

    def find_end(self):
        pass

    def next_hi_legacy(self, idx_start: int = 0, prev_high: float = 0):
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

    def next_lo_legacy(self, idx_start, prev_low):
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
    def length(self) -> float:
        return abs(self.high - self.low)

    @property
    def duration(self) -> int:
        return self.idx_end - self.idx_start


class MonoWaveUp(MonoWave):
    """
    Describes a upwards movement, which can have [skip_n] smaller downtrends
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.high, self.high_idx = self.find_end()
        self.low = self.lows_arr[self.idx_start]
        self.low_idx = self.idx_start
        self.idx_end = self.high_idx
        self.date_start = self.dates_arr[self.idx_start]
        self.date_end = self.dates_arr[self.high_idx]

    def find_end(self):
        """
        Finds the end of this MonoWave

        :param idx_start:
        :return:
        """
        high, high_idx = hi(self.lows_arr, self.highs_arr, self.idx_start)
        low_at_start = self.lows_arr[self.idx_start]

        if high is None:
            return None, None

        for _ in range(self.skip_n):

            act_high, act_high_idx = next_hi(self.lows_arr, self.highs_arr, high_idx, high)
            if act_high is None:
                return None, None

            if act_high > high:
                high = act_high
                high_idx = act_high_idx
                if np.min(self.lows_arr[self.idx_start:act_high_idx] < low_at_start):
                    return None, None

        return high, high_idx

    @property
    def dates(self) -> list:
        return [self.date_start, self.date_end]

    @property
    def points(self):
        return self.low, self.high


class MonoWaveDown(MonoWave):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.low, self.low_idx = self.find_end()
        self.high = self.highs_arr[self.idx_start]
        self.high_idx = self.idx_start

        self.date_start = self.dates_arr[self.idx_start]
        if self.low is not None:
            self.date_end = self.dates_arr[self.low_idx]
            self.idx_end = self.low_idx
        else:
            self.date_end = None
            self.idx_end = None

    @property
    def dates(self) -> list:
        return [self.date_start, self.date_end]

    @property
    def points(self):
        return self.high, self.low

    def find_end(self):
        """
        Finds the end of this MonoWave (downwards)

        :return:
        """

        low, low_idx = lo(self.lows_arr, self.highs_arr, self.idx_start)
        high_at_start = self.highs_arr[self.idx_start]
        if low is None:
            return None, None

        for _ in range(self.skip_n):
            act_low, act_low_idx = next_lo(self.lows_arr, self.highs_arr, low_idx, low)
            # print(_, 'act_low:', act_low, 'low:', low, 'low_idx:', low_idx)
            if act_low is None:
                return None, None

            if act_low < low:
                low = act_low
                low_idx = act_low_idx
                if np.max(self.highs_arr[self.idx_start:act_low_idx]) > high_at_start:
                    return None, None

            # TODO what to do if no more minima can be found?
            # if act_low > low:
            #    return None, None

        return low, low_idx

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
            if wave.label in ['B', '2', '3']:
                labels.extend([" ", f'{wave.label} ({round(wave.length/reference_length, 3)})'])
            else:
                labels.extend([" ", f'{wave.label}'])
        return labels
