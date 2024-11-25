# For '/' page, data downloader functions
import pandas as pd
import json
from datetime import date

def get_filtered_data(symbol,start_date,end_date):
    with open('history.json', 'r') as file:
            data = json.load(file)

    df = pd.DataFrame.from_dict(data, orient='index')
    df.index = pd.to_datetime(df.index)
    
    column_name = f"('Adj Close', '{symbol}')"
    
    filtered_data = df[column_name].dropna()
    filtered_data = filtered_data.loc[start_date:end_date]
    return filtered_data
def calculate_prices(filtered_data):
    current_price = filtered_data.iloc[-1] if not filtered_data.empty else None
    prev_price = filtered_data.iloc[-2] if len(filtered_data) > 1 else current_price
    percent_change = ((current_price - prev_price) / prev_price * 100) if prev_price else 0

    return current_price, percent_change

