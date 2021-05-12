from models.models import WaveOptions
import pandas as pd
from abc import ABC, abstractmethod
import time

def timeit(func):
    def wrapper(*arg, **kw):

        t1 = time.perf_counter_ns()
        res = func(*arg, **kw)
        t2 = time.perf_counter_ns()
        print("took:", t2-t1, 'ns')
        return res
    return wrapper


class WaveOptionsGenerator(ABC):
    def __init__(self, up_to: int):
        self.__up_to = up_to
        self.options = self.populate_set()

    @property
    def up_to(self):
        return self.__up_to

    @property
    def number(self):
        return len(self.options)

    @abstractmethod
    def populate_set(self):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.options.pop()
        except KeyError:
            raise StopIteration


class WaveOptionsGenerator5(WaveOptionsGenerator):
    def populate_set(self):
        checked = set()

        for i in range(0, self.up_to):
            for j in range(0, self.up_to):
                for k in range(0, self.up_to):
                    for l in range(0, self.up_to):
                        for m in range(0, self.up_to):

                            if i == 0:
                                j = k = l = m = 0
                            if j == 0:
                                k = l = m = 0
                            if k == 0:
                                l = m = 0
                            if l == 0:
                                m = 0
                            wave_options = WaveOptions(i, j, k, l, m)
                            checked.add(wave_options)
        return checked


class WaveOptionsGenerator2(WaveOptionsGenerator):
    def populate_set(self):
        checked = set()

        for i in range(0, self.up_to):
            for j in range(0, self.up_to):
                if i == 0:
                    j = 0

                wave_options = WaveOptions(i, j, None, None, None)
                checked.add(wave_options)
        return checked


def convert_yf_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts a yahoo finance OHLC DataFrame to column name(s) used in this project

    old_names = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    new_names = ['Date', 'Open', 'High', 'Low', 'Close']

    :param df:
    :return:
    """
    df_output = pd.DataFrame()

    df_output['Date'] = list(df.index)
    df_output['Date'] = pd.to_datetime(df_output['Date'], format="%Y-%m-%d %H:%M:%S")

    df_output['Open'] = df['Open'].to_list()
    df_output['High'] = df['High'].to_list()
    df_output['Low'] = df['Low'].to_list()
    df_output['Close'] = df['Close'].to_list()

    return df_output
