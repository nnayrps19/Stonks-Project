import yfinance as yf
import ta
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from datetime import *
from flask import url_for
from bokeh.io import output_file, save


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

def run_backtest(symbol, strategy, start_date, end_date):
    strat = ""
    initial_balance = 100000
    df = yf.download(symbol, start_date, end_date)

    # Flatten MultiIndex
    df.columns = df.columns.map(lambda x: x[0])

    # Optionally reset index
    df.reset_index(inplace=True)
    # Run the backtest
    bt = Backtest(df, strategy, cash=100000)
    if strategy == SMAcross:
        strat = "SMA"
    elif strategy == BollingerBandsStrategy:
        strat = "BB"
    elif strategy == MACDStrategy:
        strat = "MACD"
    output = bt.run()
    trades = output['_trades']
    trades['EntryDate'] = trades['EntryBar'].apply(lambda x: df['Date'].iloc[x])
    trades['ExitDate'] = trades['ExitBar'].apply(lambda x: df['Date'].iloc[x])
    trades['Symbol'] = symbol
    trades['TransactionType'] = trades['Size'].apply(lambda x: 'Buy' if x > 0 else 'Sell')
    trades['Shares'] = trades['Size'].abs()
    trades['TransactionAmount'] = trades['EntryPrice'] * trades['Shares']
    trades['Gain/Loss'] = trades['PnL']
    trades['Balance'] = initial_balance + trades['Gain/Loss'].cumsum()
    trades_filtered = trades[[
        'EntryDate', 'ExitDate', 'Symbol', 'TransactionType', 
        'Shares', 'TransactionAmount', 'Gain/Loss', 'Balance'
    ]]

    # Calculate summary metrics
    total_gain_loss = trades['Gain/Loss'].sum()
    total_return_pct = (trades['Balance'].iloc[-1] / initial_balance - 1) * 100
    annual_return_pct = ((1 + total_return_pct / 100) ** (1 / ((df['Date'].iloc[-1] - df['Date'].iloc[0]).days / 365)) - 1) * 100
    current_balance = trades['Balance'].iloc[-1]

    # Append summary row
    summary_row = pd.DataFrame({
        'EntryDate': [None],
        'ExitDate': [None],
        'Symbol': [symbol],
        'TransactionType': ['Summary'],
        'Shares': [None],
        'TransactionAmount': [None],
        'Gain/Loss': [total_gain_loss],
        'Balance': [current_balance]
    })
    trades_filtered = pd.concat([trades_filtered, summary_row], ignore_index=True)


    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_path = f'static/{strat}_backtest_plot_{timestamp}.html'
    trades_csv_path = f'static/{strat}_trades_{timestamp}.csv'
    
    bt.plot(filename=plot_path)
    trades_filtered.to_csv(trades_csv_path, index=False)
    plot_url = url_for('static', filename=plot_path.split('static/')[1])
    return output, plot_url, trades_csv_path
    
def run_backtest_option(backtest_option, symbol, start_date, end_date):
    if backtest_option == 'SMA':
        output, plot_path, trades_csv_path = run_backtest(symbol, SMAcross,start_date, end_date)
    elif backtest_option == 'BB':
        output, plot_path, trades_csv_path = run_backtest(symbol, BollingerBandsStrategy,start_date, end_date)
    elif backtest_option == 'MACD':
        output, plot_path, trades_csv_path = run_backtest(symbol, MACDStrategy,start_date, end_date)
    
    return output, plot_path, trades_csv_path
class Context():
    def __init__(self, symbol, btoption, start_date, end_date):
        self.Strategy = btoption
        self.Symbol = symbol
        self.Start_Date = start_date
        self.End_Date = end_date
    def run_backtest_option(self):
        output, plot_path, trades_csv_path = run_backtest(self.Symbol, self.Strategy ,self.Start_Date, self.End_Date)
        return output, plot_path, trades_csv_path

