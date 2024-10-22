import datasuite
import pandas as pd

# Create a simple moving average cross over function
def simple_average(long=200, short=50):
    """Returns a pandas dataframe with buy and sell signals for SMA cross over"""
    data = datasuite.read_data()
    data['sma_short'] = data['Close'].rolling(short).mean()
    data['sma_long'] = data['Close'].rolling(long).mean()
    data['Signal'] = 0
    data['Signal'] = data['sma_short'][short:] > data['sma_long'][short:]
    data['Trade'] = data['Signal'].diff()
    return data
