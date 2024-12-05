import yfinance as yf
import ta
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from datetime import *
from flask import url_for

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
class SMAcross(Strategy):
    n1 = 50
    n2 = 100

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(ta.trend.sma_indicator, pd.Series(close), self.n1)
        self.sma2 = self.I(ta.trend.sma_indicator, pd.Series(close), self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()

def run_backtest(symbol):
    
    df = yf.download(symbol, start='2021-01-01')

    # Flatten MultiIndex
    df.columns = df.columns.map(lambda x: x[0])

    # Optionally reset index
    df.reset_index(inplace=True)

    # Run the backtest
    bt = Backtest(df, SMAcross, cash=100000)
    output = bt.run()
    trades = output['_trades']
    trades['EntryDate'] = trades['EntryBar'].apply(lambda x: df['Date'].iloc[x])
    trades['ExitDate'] = trades['ExitBar'].apply(lambda x: df['Date'].iloc[x])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_path = f'static/SMA_backtest_plot_{timestamp}.html'
    trades_csv_path = f'static/SMA_trades_{timestamp}.csv'
    
    bt.plot(filename=plot_path)
    trades.to_csv(trades_csv_path, index=False)
    plot_url = url_for('static', filename=plot_path.split('static/')[1])
    return output, plot_url, trades_csv_path

def run_BBS_backtest(symbol):
    df = yf.download(symbol, start='2021-01-01')
    df.columns = df.columns.map(lambda x: x[0])

    df.reset_index(inplace=True)
    bt = Backtest(df, BollingerBandsStrategy, cash=100000)
    output = bt.run()
    trades = output['_trades']

    trades['EntryDate'] = trades['EntryBar'].apply(lambda x:df['Date'].iloc[x])
    trades['ExitDate'] = trades['ExitBar'].apply(lambda x:df['Date'].iloc[x])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_path = f'static/BB_backtest_plot_{timestamp}.html'
    trades_csv_path = f'static/BBS_trades_{timestamp}.csv'
    bt.plot(filename=plot_path)
    trades.to_csv(trades_csv_path, index=False)
    plot_url = url_for('static', filename=plot_path.split('static/'[1]))

    return output, plot_url, trades_csv_path
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
    trades = output['_trades']

    trades['EntryDate'] = trades['EntryBar'].apply(lambda x:df['Date'].iloc[x])
    trades['ExitDate'] = trades['ExitBar'].apply(lambda x:df['Date'].iloc[x])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_path = f'static/MACD_backtest_plot_{timestamp}.html'
    trades_csv_path = f'static/MACD_trades_{timestamp}.csv'
    bt.plot(filename=plot_path)
    trades.to_csv(trades_csv_path, index=False)
    plot_url = url_for('static/',filename=plot_path.split('static/'[1]))

    return output, plot_url, trades_csv_path
def run_backtest_option(backtest_option, symbol):
    if backtest_option == 'SMA':
        output, plot_path, trades_csv_path = run_backtest(symbol)
    elif backtest_option == 'BB':
        output, plot_path, trades_csv_path = run_BBS_backtest(symbol)
    elif backtest_option == 'MACD':
        output, plot_path, trades_csv_path = run_MACD_backtest(symbol)
    
    return output, plot_path, trades_csv_path

