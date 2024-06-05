import yfinance as yf

from models.helpers import convert_yf_data

df = yf.download(tickers='AAPL',
                 interval="1d",
                 start="2022-12-01")

convert_yf_data(df).to_csv(r'data\aapl_1d_2020.csv', sep=",", index=False)
