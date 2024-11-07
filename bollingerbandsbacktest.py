import yfinance as yf
import ta
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

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

# Download data from yfinance
df = yf.download('FNGU', start='2021-01-01')

# Flatten MultiIndex
df.columns = df.columns.map(lambda x: x[0])

# Optionally reset index
df.reset_index(inplace=True)

# Run the backtest
bt = Backtest(df, BollingerBandsStrategy, cash=100000)
output = bt.run()
print(output)
bt.plot()
