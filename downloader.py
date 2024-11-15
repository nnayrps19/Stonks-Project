import yfinance as yf
import pandas as pd
import json
import matplotlib.pyplot as plt
from datetime import datetime

#Default Download Function
def download(tick, start='2021-1-1', end=None):
    """Default download function, accepts ticker symbol, keyword start and end parameters that default to 2021-1-1 and todays date"""
    data = yf.download(tick, start, end)
    data.to_json('history.json')

#Readable Download Function
def readable_download(tick, start='2021-1-1', end=None):
    """Download function that createas a json that is easier to read"""
    data = yf.download(tick, start=start, end=end)
    data.index = data.index.strftime('%Y-%m-%d')

    # Load existing data if it exists
    try:
        with open('history.json', 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = {}

    # Append new data for the ticker
    for date, row in data.iterrows():
        if date not in existing_data:
            existing_data[date] = {}
        
        for column, value in row.items():
            existing_data[date][(column, tick)] = value

    # Save the updated data back to JSON in readable format
    with open('history.json', 'w') as file:
        json.dump(existing_data, file, indent=1)
def delete_data():
    with open('readable.json', 'r') as file:
        json.dump({}, file)

#Read data from history.json returns a pandas dataframe
def read_data():
    """Reads data from history.json, returns a pandas dataframe"""
    data = pd.read_json('history.json', precise_float=True)
    flattened_data = data.applymap(lambda x: pd.Series(x).stack()).unstack().T
    flattened_data.index = pd.to_datetime(flattened_data.index)

    return data

#Convert data to list
def data_list():
    """Converts data to a list"""
    data = read_data()
    return data.values.tolist()

def load_data(symbol, start_date, end_date):
    try:
        with open('history.json', 'r') as f:
            data = json.load(f)

        df = pd.DataFrame.from_dict(data, orient='index')
        df.index = pd.to_datetime(df.index)
        df = df[(df.index >= start_date) & (df.index <= end_date)]

        return df
    except FileNotFoundError:
        return None

def readable_download_new(tick, start='2021-1-1', end=None):
    """Download function that createas a json that is easier to read"""
    data = yf.download(tick, start, end)
    data.index = data.index.strftime('%Y-%m-%d')
    data.to_json('history.json', orient='index', indent=1, index=True)
