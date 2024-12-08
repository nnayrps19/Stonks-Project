# For '/' page, data downloader functions
import pandas as pd
import json
from datetime import date
import yfinance as yf
from abc import ABC, abstractmethod

# Abstract Component
class DH_Abstract(ABC):
    @abstractmethod
    def get_filtered_data(self, symbol, start_date, end_date):
        pass
    @abstractmethod
    def readable_download_new(self, tick, start='2021-1-1', end=None):
        pass
    @abstractmethod
    def calculate_prices(self, filtered_data):
        pass

# Concrete Component
class DataDownloader(DH_Abstract):
    def get_filtered_data(self, symbol,start_date,end_date):
        with open('history.json', 'r') as file:
                data = json.load(file)

        df = pd.DataFrame.from_dict(data, orient='index')
        df.index = pd.to_datetime(df.index)
        
        column_name = f"('Adj Close', '{symbol}')"
        
        filtered_data = df[column_name].dropna()
        filtered_data = filtered_data.loc[start_date:end_date]
        return filtered_data
    def readable_download_new(self, tick, start='2021-1-1', end=None):
        """Download function that createas a json that is easier to read"""
        data = yf.download(tick, start, end)
        data.index = data.index.strftime('%Y-%m-%d')
        data.to_json('history.json', orient='index', indent=1, index=True)
    def calculate_prices(self, filtered_data):
        current_price = filtered_data.iloc[-1] if not filtered_data.empty else None
        prev_price = filtered_data.iloc[-2] if len(filtered_data) > 1 else current_price
        percent_change = ((current_price - prev_price) / prev_price * 100) if prev_price else 0
        return current_price, percent_change

# Decorator Abstract Class
class DataDecorator(DH_Abstract, ABC): 
    def get_filtered_data(self, symbol, start_date, end_date):
        pass
    def readable_download_new(self, tick, start='2021-1-1', end=None):
        pass
    def calculate_prices(self, filtered_data):
        pass

# Concrete Decorator 
class DataCalculator(DataDecorator):
    def get_filtered_data(self, symbol, start_date, end_date):
        with open('history.json', 'r') as file:
                data = json.load(file)

        df = pd.DataFrame.from_dict(data, orient='index')
        df.index = pd.to_datetime(df.index)
        
        column_name = f"('Adj Close', '{symbol}')"
        
        filtered_data = df[column_name].dropna()
        filtered_data = filtered_data.loc[start_date:end_date]
        return filtered_data
    def readable_download_new(self, tick, start='2021-1-1', end=None):
        """Download function that createas a json that is easier to read"""
        data = yf.download(tick, start, end)
        data.index = data.index.strftime('%Y-%m-%d')
        data.to_json('history.json', orient='index', indent=1, index=True)
    def calculate_prices(self, filtered_data):
        current_price = filtered_data.iloc[-1] if not filtered_data.empty else None
        prev_price = filtered_data.iloc[-2] if len(filtered_data) > 1 else current_price
        percent_change = ((current_price - prev_price) / prev_price * 100) if prev_price else 0
        return current_price, percent_change


