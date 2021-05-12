from __future__ import annotations
from models.waves import WavePattern
from models.waverules import Impulse, TDWave
from models.waveanalyzer import WaveAnalyzer
from models.helpers import WaveOptionsGenerator2, WaveOptionsGenerator5
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import random
import time

df = pd.read_csv(r'data\btc-eur_h.csv')
df = pd.read_csv(r'data\btc-usd_1d.csv')
df = pd.read_csv(r'data\eth-usd_60m.csv')

df = df
idx_start = np.argmin(np.array(list(df['Low'])))

wa = WaveAnalyzer(df=df, verbose=True)

cntr = 0
found_wave_cntr = 0
checked = set()
start = time.perf_counter()

# TODO find number of skippable max / min for a given start point
# TODO MonoWaveUp/Down .from_wavepattern() -> to generate a larger wave from a found 12345 / ABC Structure
wave_options = WaveOptionsGenerator5(10)
#wave_options = WaveOptionsGenerator2(150)


valid_pattern = False
impulse = Impulse('impulse')
tdwave = TDWave('tdwave')


class WaveCount:
    def __init__(self):
        self.wavecycles = list

    def waves_by_degree(self, degree: int):
        pass

    def add(self, wavecycle: WaveCycle):
        self.wavecycles.append(wavecycle)

class WaveCycle:
    """
    One Cycle of 12345 -> ABC
    """
    def __init__(self, wavepattern_up: WavePattern, wavepattern_down: WavePattern):
        self.wp_up = wavepattern_up
        self.wp_down = wavepattern_down

    @property
    def low(self):
        pass

    @property
    def high(self):
        pass

print(f"will run {wave_options.number} combinations.")
random_starts = set()
while True:#not valid_pattern:
    try:
        new_options = next(wave_options)
    except StopIteration:
        print('end of options')
        break


    waves = wa.find_impulsive_wave(idx_start=idx_start, wave_config=new_options.values)
    #waves = wa.find_td_wave(idx_start=idx_start, wave_config=new_options.values)
    waves = wa.find_corrective_wave(idx_start=idx_start, wave_config=[0, 0, 0])
    if waves:

        wave_pattern = WavePattern(waves, verbose=False)

        valid_pattern = wave_pattern.check_rule(impulse)
        #valid_pattern = wave_pattern.check_rule(tdwave)
        if valid_pattern:
            print('WAVE FOUND!!!', new_options.values)


            data = go.Ohlc(x=df['Date'],
                           open=df['Open'],
                           high=df['High'],
                           low=df['Low'],
                           close=df['Close'])

            monowaves = go.Scatter(x=wave_pattern.dates,
                                   y=wave_pattern.values,
                                   text=wave_pattern.labels,
                                   mode='lines+markers+text',
                                   textposition='middle right',
                                   textfont=dict(size=15, color='#2c3035'),
                                   line=dict(
                                       color=('rgb(111, 126, 130)'),
                                       width=3),
                                   )

            fig = go.Figure(data=[data, monowaves])
            fig.update(layout_xaxis_rangeslider_visible=False)

            fig.show()
end = time.perf_counter()

print(f"took: {-start + end}")