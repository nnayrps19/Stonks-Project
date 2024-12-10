import yfinance as yf
import ta
import pandas as pd
# "Strategy" is an interface that complies with 'Strategy' pattern & applies to different backtest strategies
from backtesting import Backtest, Strategy 
from backtesting.lib import crossover
from datetime import *
from flask import url_for

class BollingerBandsStrategy(Strategy):
    def init(self):
        close = self.data.Close
        self.sma = self.I(ta.trend.sma_indicator, pd.Series(close), 20)
        self.upper_band = self.sma + 2*(self.I(pd.Series(close).rolling(20).std))
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

def run_backtest(symbol, strategy, start_date, end_date):
    strat = ""
    df = yf.download(symbol, start_date, end_date)
    df.columns = df.columns.map(lambda x: x[0])
    df.reset_index(inplace=True)
    BacktestStrategyOperation = None
    if strategy == 'SMA':
        BacktestStrategyOperation = SMAcross
    elif strategy == 'BB':
        BacktestStrategyOperation = BollingerBandsStrategy
    elif strategy == 'MACD':
        BacktestStrategyOperation = MACDStrategy
    bt = Backtest(df, BacktestStrategyOperation, cash=100000)
    output = bt.run()
    trades = output['_trades']
    trades['EntryDate'] = trades['EntryBar'].apply(lambda x: df['Date'].iloc[x])
    trades['ExitDate'] = trades['ExitBar'].apply(lambda x: df['Date'].iloc[x])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_path = f'static/{strategy}_backtest_plot_{timestamp}.html'
    trades_csv_path = f'static/{strategy}_trades_{timestamp}.csv'
    bt.plot(filename=plot_path)
    trades.to_csv(trades_csv_path, index=False)
    plot_url = url_for('static', filename=plot_path.split('static/')[1])
    return output, plot_url, trades_csv_path

# Context class for the "Strategy" pattern of software engineering
class Context():
    def __init__(self, symbol, btoption, start_date, end_date):
        self.Strategy = btoption
        self.Symbol = symbol
        self.Start_Date = start_date
        self.End_Date = end_date
    def run_backtest_option(self):
        output, plot_path, trades_csv_path = run_backtest(self.Symbol, self.Strategy ,self.Start_Date, self.End_Date)
        return output, plot_path, trades_csv_path