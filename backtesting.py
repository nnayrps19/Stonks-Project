import pandas as pd
import json
from downloader import *

def calculateSMAs():
    data = read_data()
    df = pd.DataFrame(data)

    df['SMA_3'] = df['price'].rolling(window=3).mean()

    print(df)