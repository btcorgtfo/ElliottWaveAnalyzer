import yfinance as yf

from models.helpers import convert_yf_data

df = yf.download(tickers='BTC-USD',
                 interval="1d",
                 start="2017-12-01")

convert_yf_data(df).to_csv(r'data\btc-usd_1d_2017.csv', sep=",", index=False)
