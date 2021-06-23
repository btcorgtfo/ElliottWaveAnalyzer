from __future__ import annotations
from models.WavePattern import WavePattern
from models.WaveRules import Impulse, LeadingDiagonal
from models.WaveAnalyzer import WaveAnalyzer
from models.WaveOptions import WaveOptionsGenerator5
from models.helpers import plot_pattern
import pandas as pd
import numpy as np

df = pd.read_csv(r'data\btc-usd_1d.csv')
idx_start = np.argmin(np.array(list(df['Low'])))

wa = WaveAnalyzer(df=df, verbose=False)

wave_options_impulse = WaveOptionsGenerator5(up_to=15)

impulse = Impulse('impulse')
leading_diagonal = LeadingDiagonal('leading diagonal')
rules_to_check = [impulse, leading_diagonal]

print(f'Start at idx: {idx_start}')
print(f"will run up to {wave_options_impulse.number / 1e6}M combinations.")

wavepatterns_up = set()

for new_option_impulse in wave_options_impulse.options_sorted:

    waves_up = wa.find_impulsive_wave(idx_start=idx_start, wave_config=new_option_impulse.values)

    if waves_up:
        wavepattern_up = WavePattern(waves_up, verbose=False)

        for rule in rules_to_check:

            if wavepattern_up.check_rule(rule):
                if wavepattern_up in wavepatterns_up:
                    continue
                else:
                    wavepatterns_up.add(wavepattern_up)
                    print(f'{rule.name} found: {new_option_impulse.values}')
                    plot_pattern(df=df, wave_pattern=wavepattern_up)
