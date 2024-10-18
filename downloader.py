import yfinance as yf
import datetime

#Default Download Function
def download(tick, start='2021-1-1', end=datetime.date.today()):
    """Default download function, accepts ticker symbol, keyword start and end parameters that default to 2021-1-1 and todays date"""
    data = yf.download(tick, start, end)
    data.index = data.index.strftime('%Y-%m-%d')
    data.to_json('history.json', orient='index', indent=4)



