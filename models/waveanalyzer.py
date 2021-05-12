from models.waves import MonoWaveUp, MonoWaveDown
import numpy as np
import pandas as pd


class WaveAnalyzer:
    """
    Find impulse or corrective waves for given dataframe
    """
    def __init__(self,
                 df: pd.DataFrame,
                 verbose: bool = False):

        self.df = df
        self.lows = np.array(list(self.df['Low']))
        self.highs = np.array(list(self.df['High']))
        self.dates = np.array(list(self.df['Date']))
        self.verbose = verbose

    def find_impulsive_wave(self,
                            idx_start: int,
                            wave_config: list = None):
        # first wave, start at first low in the data

        if wave_config is None:
            wave_config = [0, 0, 0, 0, 0]

        wave1 = MonoWaveUp(lows=self.lows, highs=self.highs, dates=self.dates, idx_start=idx_start, skip=wave_config[0])
        wave1.label = '1'
        wave1_end = wave1.idx_end
        if wave1_end is None:
            if self.verbose: print("Wave 1 has no End in Data")
            return False

        wave2 = MonoWaveDown(lows=self.lows, highs=self.highs, dates=self.dates, idx_start=wave1_end, skip=wave_config[1])
        wave2.label = '2'
        wave2_end = wave2.idx_end
        if wave2_end is None:
            if self.verbose: print("Wave 2 has no End in Data")
            return False

        wave3 = MonoWaveUp(lows=self.lows, highs=self.highs, dates=self.dates, idx_start=wave2_end, skip=wave_config[2])
        wave3.label = '3'
        wave3_end = wave3.idx_end
        if wave3_end is None:
            if self.verbose: print("Wave 3 has no End in Data")
            return False

        wave4 = MonoWaveDown(lows=self.lows, highs=self.highs, dates=self.dates, idx_start=wave3_end, skip=wave_config[3])
        wave4.label = '4'
        wave4_end = wave4.idx_end

        if wave4_end is None:
            if self.verbose: print("Wave 4 has no End in Data")
            return False

        wave5 = MonoWaveUp(lows=self.lows, highs=self.highs, dates=self.dates, idx_start=wave4_end, skip=wave_config[4])
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

        waveA = MonoWaveDown(lows=self.lows, highs=self.highs, dates=self.dates, idx_start=idx_start, skip=wave_config[0])
        waveA.label = 'A'
        waveA_end = waveA.idx_end
        if waveA_end is None:
            return False

        waveB = MonoWaveUp(lows=self.lows, highs=self.highs, dates=self.dates, idx_start=waveA_end, skip=wave_config[1])
        waveB.label = 'B'
        waveB_end = waveB.idx_end
        if waveB_end is None:
            return False

        waveC = MonoWaveDown(lows=self.lows, highs=self.highs, dates=self.dates, idx_start=waveB_end, skip=wave_config[2])
        waveC.label = 'C'
        waveC_end = waveC.idx_end
        if waveC_end is None:
            return False

        return [waveA, waveB, waveC]

    def find_td_wave(self, idx_start: int, wave_config: list = None):
        if wave_config is None:
            wave_config = [0, 0]

        wave1 = MonoWaveUp(self.df, idx_start=idx_start, skip=wave_config[0])
        wave1.label = '1'
        wave1_end = wave1.idx_end
        if wave1_end is None:
            if self.verbose: print("Wave 1 has no End in Data")
            return False

        wave2 = MonoWaveDown(self.df, idx_start=wave1_end, skip=wave_config[1])
        wave2.label = '2'
        wave2_end = wave2.idx_end
        if wave2_end is None:
            if self.verbose: print("Wave 2 has no End in Data")
            return False

        return [wave1, wave2]