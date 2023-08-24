from models.MonoWave import MonoWaveDown, MonoWaveUp
from models.helpers import plot_monowave
import numpy as np
import pandas as pd

df = pd.read_csv(r"data\btc-usd_1d.csv")
lows = np.array(list(df["Low"]))
highs = np.array(list(df["High"]))
dates = np.array(list(df["Date"]))

# find a monowave down starting from the low at the 3rd index
mw_up = MonoWaveUp(lows=lows, highs=highs, dates=dates, idx_start=3, skip=5)
plot_monowave(df, mw_up)

# find a monowave down from the end of the monowave up
mw_down = MonoWaveDown(
    lows=lows, highs=highs, dates=dates, idx_start=mw_up.idx_end, skip=0
)
plot_monowave(df, mw_down)
