import yfinance as yf
import ta
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from datetime import *

class BollingerBandsStrategy(Strategy):
    def init(self):
        close = self.data.Close
        # Middle Band: A 20-day (n) simple moving average (SMA)
        self.sma = self.I(ta.trend.sma_indicator, pd.Series(close), 20)
        # Upper Band: Middle Band + (2 x standard deviation of price)
        self.upper_band = self.sma + 2*(self.I(pd.Series(close).rolling(20).std))
        # Lower Band: Middle Band — (2 x standard deviation of price)
        self.lower_band = self.sma - 2*(self.I(pd.Series(close).rolling(20).std))

    def next(self):
        if crossover(self.data.Close, self.lower_band):
            self.buy()
        elif crossover(self.data.Close, self.upper_band):
            self.sell()

class MACDStrategy(Strategy):
    def init(self):
        close = self.data.Close
        # Calculate the MACD line and Signal line
        self.macd = self.I(ta.trend.macd, pd.Series(close), window_slow=26, window_fast=12)
        self.signal = self.I(ta.trend.macd_signal, pd.Series(close), window_slow=26, window_fast=12, window_sign=9)

    def next(self):
        # Buy when MACD crosses above the signal line
        if crossover(self.macd, self.signal):
            self.buy()
        # Sell when MACD crosses below the signal line
        elif crossover(self.signal, self.macd):
            self.sell()

def run_BBS_backtest(symbol):
    # Download data from yfinance
    df = yf.download(symbol, start='2021-01-01')

    # Flatten MultiIndex
    df.columns = df.columns.map(lambda x: x[0])

    # Optionally reset index
    df.reset_index(inplace=True)

    # Run the backtest
    bt = Backtest(df, BollingerBandsStrategy, cash=100000)
    output = bt.run()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_path = f'static/BB_backtest_plot_{timestamp}.png'
    bt.plot(filename=plot_path)

    return output, plot_path
def run_MACD_backtest(symbol):
    # Download data from yfinance
    df = yf.download(symbol, start='2021-01-01')

    # Flatten MultiIndex
    df.columns = df.columns.map(lambda x: x[0])

    # Optionally reset index
    df.reset_index(inplace=True)

    # Run the backtest
    bt = Backtest(df, MACDStrategy, cash=100000)
    output = bt.run()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_path = f'static/MACD_backtest_plot_{timestamp}.png'
    bt.plot(filename=plot_path)

    return output, plot_path

