from __future__ import annotations

import numpy as np

from models.functions import hi, lo, next_hi, next_lo


class MonoWave:
    """
    A class representing a monowave pattern in financial time series data.

    Attributes:
    - lows_arr (numpy.array): An array containing the lows of the monowave pattern.
    - highs_arr (numpy.array): An array containing the highs of the monowave pattern.
    - dates_arr (numpy.array): An array containing the dates corresponding to the monowave pattern.
    - idx_start (int): The index of the starting point of the monowave pattern.
    - skip_n (int, optional): The number of elements to skip during pattern analysis (default is 0).
    - idx_end (int): The index of the ending point of the monowave pattern.
    - count (int): The count of the monowave (e.g., 1, 2, A, B, etc.).
    - degree (int): The degree of the monowave (1 = lowest timeframe level, 2 as soon as a pattern like 12345 is found,
    etc.).
    - date_start (str): The start date of the monowave pattern.
    - date_end (str): The end date of the monowave pattern.
    - low (float): The lowest value in the monowave pattern.
    - high (float): The highest value in the monowave pattern.
    - low_idx (int): The index of the lowest value in the monowave pattern.
    - high_idx (int): The index of the highest value in the monowave pattern.

    Properties:
    - labels (str): A property that returns the count of the monowave as a string.
    - length (float): A property that returns the absolute difference between high and low values.
    - duration (int): A property that returns the duration (index difference) of the monowave.

    Methods:
    - from_wavepattern(cls, wave_pattern): A class method to create a MonoWave object from a given wave pattern.

    Note:
    - This class is designed for analyzing financial time series data and identifying monowave patterns.
    """

    def __init__(self,
                 lows: np.array,
                 highs: np.array,
                 dates: np.array,
                 idx_start: int,
                 skip: int = 0):

        # Constructor initializes the attributes
        self.lows_arr = lows
        self.highs_arr = highs
        self.dates_arr = dates
        self.skip_n = skip
        self.idx_start = idx_start
        self.idx_end = int

        self.count = int
        self.degree = 1

        self.date_start = str
        self.date_end = str

        self.low = float
        self.high = float
        self.low_idx = int
        self.high_idx = int

    def __sub__(self, other):
        """
        Subtracts the length of another MonoWave object from the length of the current object.

        Args:
        - other (MonoWave): Another MonoWave object to subtract.

        Returns:
        float: The difference in length between the two MonoWave objects.
        """
        return self.length - other.length

    @property
    def labels(self) -> str:
        """
        Property that returns the count of the monowave as a string.

        Returns:
        str: The count of the monowave.
        """
        return str(self.count)

    @property
    def length(self) -> float:
        """
        Property that returns the absolute difference between the high and low values.

        Returns:
        float: The length of the monowave.
        """
        return abs(self.high - self.low)

    @property
    def duration(self) -> int:
        """
        Property that returns the duration (index difference) of the monowave.

        Returns:
        int: The duration of the monowave.
        """
        return self.idx_end - self.idx_start

    @classmethod
    def from_wavepattern(cls, wave_pattern):
        """
        Class method tocreate a MonoWave object from a given wave pattern.

        Args:
        - wave_pattern (WavePattern): The wave pattern object to create the MonoWave from.

        Returns:
        MonoWave: The created MonoWave object.

        Raises:
        ValueError: If the wave pattern has a number of waves other than 3 or 5.

        Note:
        - This method is used to convert a WavePattern object into a MonoWave object for further analysis.
        """
        lows = highs = dates = np.zeros(10)  # dummy arrays to initialize the class

        if len(wave_pattern.waves.keys()) == 5:
            low = wave_pattern.waves.get('wave1').low
            low_idx = wave_pattern.waves.get('wave1').low_idx
            high = wave_pattern.waves.get('wave5').high
            high_idx = wave_pattern.waves.get('wave5').high_idx
            date_start = wave_pattern.waves.get('wave1').date_start
            date_end = wave_pattern.waves.get('wave5').date_end

            monowave_up = cls(lows, highs, dates, 0)

            monowave_up.low, monowave_up.low_idx, monowave_up.high, monowave_up.high_idx = low, low_idx, high, high_idx
            monowave_up.date_start, monowave_up.date_end = date_start, date_end

            monowave_up.degree = wave_pattern.waves.get('wave1').degree + 1
            return monowave_up

        elif len(wave_pattern.waves.keys()) == 3:
            low = wave_pattern.waves.get('wave3').low
            low_idx = wave_pattern.waves.get('wave3').low_idx
            high = wave_pattern.waves.get('wave1').high
            high_idx = wave_pattern.waves.get('wave1').high_idx
            date_start = wave_pattern.waves.get('wave1').date_start
            date_end = wave_pattern.waves.get('wave3').date_end

            monowave_down = cls(lows, highs, dates, 0)
            monowave_down.low, monowave_down.low_idx, monowave_down.high, monowave_down.high_idx = low, low_idx, high, high_idx
            monowave_down.date_start, monowave_down.date_end = date_start, date_end

            monowave_down.degree = wave_pattern.waves.get('wave1').degree + 1

            return monowave_down

        else:
            raise ValueError('WavePattern other than 3 or 5 waves not implemented, yet.')


class MonoWaveUp(MonoWave):
    """
    A subclass of MonoWave representing an upward monowave pattern.

    Attributes:
    - Inherits all attributes from the parent class MonoWave.

    Methods:
    - __init__(*args, **kwargs): Initializes the MonoWaveUp object.
    - find_end(): Finds the end of the MonoWaveUp pattern.

    Properties:
    - dates (list): Returns the start and end dates of the MonoWaveUp pattern.
    - points: Returns the low and high values of the MonoWaveUp pattern.

    Note:
    - This class extends the functionality of the MonoWave class specifically for upward monowave patterns.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the MonoWaveUp object.

        Args:
        - *args: Variable length argument list.
        - **kwargs: Arbitrary keyword arguments.

        Note:
        - This constructor calls the constructor of the parent class (MonoWave) using super().
        - It also sets additional attributes specific to MonoWaveUp.
        """
        super().__init__(*args, **kwargs)

        self.high, self.high_idx = self.find_end()
        self.low = self.lows_arr[self.idx_start]
        self.low_idx = self.idx_start
        self.idx_end = self.high_idx
        self.date_start = self.dates_arr[self.idx_start]
        self.date_end = self.dates_arr[self.high_idx]

    def find_end(self):
        """
        Finds the end of this MonoWaveUp pattern.

        Returns:
        tuple: The high value and its index that marks the end of the MonoWaveUp pattern.

        Note:
        - This method searches for the end of the upward pattern based on the lows and highs arrays.
        - It considers the skip_n attribute to skip a certain number of elements during the search.
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
                # if np.min(self.lows_arr[self.idx_start:act_high_idx] < low_at_start):
                #     return None, None
                if self.idx_start <= act_high_idx and np.min(self.lows_arr[self.idx_start:act_high_idx]) < low_at_start:
                    return None, None
        return high, high_idx

    @property
    def dates(self) -> list:
        """
        Property that returns the start and end dates of the MonoWaveUp pattern.

        Returns:
        list: The start and end dates of the MonoWaveUp pattern.
        """
        return [self.date_start, self.date_end]

    @property
    def points(self):
        """
        Property that returns the low and high values of the MonoWaveUp pattern.

        Returns:
        tuple: The low and high values of the MonoWaveUp pattern.
        """
        return self.low, self.high


class MonoWaveDown(MonoWave):
    """
    A subclass of MonoWave representing a downward monowave pattern.

    Attributes:
    - Inherits all attributes from the parent class MonoWave.

    Methods:
    - __init__(*args, **kwargs): Initializes the MonoWaveDown object.
    - find_end(): Finds the end of the MonoWaveDown pattern.

    Properties:
    - dates (list): Returns the start and end dates of the MonoWaveDown pattern.
    - points: Returns the high and low values of the MonoWaveDown pattern.

    Note:
    - This class extends the functionality of the MonoWave class specifically for downward monowave patterns.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the MonoWaveDown object.

        Args:
        - *args: Variable length argument list.
        - **kwargs: Arbitrary keyword arguments.

        Note:
        - This constructor calls the constructor of the parent class (MonoWave) using super().
        - It also sets additional attributes specific to MonoWaveDown.
        """
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
        """
        Property that returns the start and end dates of the MonoWaveDown pattern.

        Returns:
        list: The start and end dates of the MonoWaveDown pattern.
        """
        return [self.date_start, self.date_end]

    @property
    def points(self):
        """
        Property that returns the high and low values of the MonoWaveDown pattern.

        Returns:
        tuple: The high and low values of the MonoWaveDown pattern.
        """
        return self.high, self.low

    def find_end(self):
        """
        Finds the end of this MonoWaveDown pattern.

        Returns:
        tuple: The low value and its index that marks the end of the MonoWaveDown pattern.

        Note:
        - This method searches for the end of the downward pattern based on the lows and highs arrays.
        - It considers the skip_n attribute to skip a certain number of elements during the search.
        """
        low, low_idx = lo(self.lows_arr, self.highs_arr, self.idx_start)
        high_at_start = self.highs_arr[self.idx_start]
        if low is None:
            return None, None

        for _ in range(self.skip_n):
            act_low, act_low_idx = next_lo(self.lows_arr, self.highs_arr, low_idx, low)
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
        # if low > np.min(self.lows_arr[low_idx:]):
        #    return None, None
        # else:
        return low, low_idx
