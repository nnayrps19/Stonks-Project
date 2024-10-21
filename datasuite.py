import yfinance as yf
import pandas as pd

#Default Download Function
def download(tick, start='2021-1-1', end=None):
    """Default download function, accepts ticker symbol, keyword start and end parameters that default to 2021-1-1 and todays date"""
    data = yf.download(tick, start, end)
    data.to_json('history.json')

#Readable Download Function
def readable_download(tick, start='2021-1-1', end=None):
    """Download function that createas a json that is easier to read"""
    data = yf.download(tick, start, end)
    data.index = data.index.strftime('%Y-%m-%d')
    data.to_json('readable.json', orient='index', indent=1, index=True)

#Read data from history.json returns a pandas dataframe
def read_data():
    """Reads data from history.json, returns a pandas dataframe"""
    data = pd.read_json('history.json', precise_float=True)
    return data

#Convert data to list
def data_list():
    """Converts data to a list"""
    data = read_data()
    return data.values.tolist()