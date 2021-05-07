import yfinance as yf
import pandas as pd
from models.helpers import convert_yf_data

df = yf.download(tickers='ETH-USD',
                 interval="90m",
                 start="2021-04-18")

convert_yf_data(df).to_csv('data/eth-usd_90m.csv', sep=",", index=False)

#print(df.info())