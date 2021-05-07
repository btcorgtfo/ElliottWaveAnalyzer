from __future__ import annotations
from models.models import WavePattern, WaveAnalyzer, Impulse
from models.helpers import WaveOptionsGenerator
import pandas as pd
import plotly.graph_objects as go
import random
import time

idx_start = 4
df = pd.read_csv(r'data\eth-usd_90m.csv')
df = df

wa = WaveAnalyzer(df=df)

cntr = 0
found_wave_cntr = 0
checked = set()
start = time.perf_counter()


wave_options = WaveOptionsGenerator(8)
valid_pattern = False
impulse = Impulse('impulse')

print(f"will run {wave_options.number} combinations.")

while not valid_pattern:
    try:
        new_options = next(wave_options)
    except StopIteration:
        break

    waves = wa.find_impulsive_wave(idx_start=idx_start, wave_config=new_options.values)

    #waves = wa.find_corrective_wave(idx_start=idx_start, wave_config=[0, 0, 0])
    if waves:
        wave_pattern = WavePattern(waves, verbose=False)
        valid_pattern = wave_pattern.check_rule(impulse)
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