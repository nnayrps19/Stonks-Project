from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import json
from datetime import *
from downloader import *
from stonksbacktest import *
import matplotlib.pyplot as plt


app = Flask(__name__)

with open('history.json', 'r') as file:
    data = json.load(file)

df = pd.DataFrame.from_dict(data, orient='index')
df.index = pd.to_datetime(df.index)

@app.route('/', methods=['GET', 'POST'])
def index():
    max_date = date.today().strftime("%Y-%m-%d")
    
    if request.method == "POST":
        today = date.today()
        symbol = request.form["symbol"]
        readable_download_new(symbol, '2021-01-01', today)
        
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        

        column_name = f"('Adj Close', '{symbol}')"
        filtered_data = df.loc[start_date:end_date, column_name]
        
        dates = filtered_data.index.strftime('%Y-%m-%d').tolist()
        prices = filtered_data.values.tolist()
        
        return jsonify(dates=dates, prices=prices)
    return render_template('index.html', max_date=max_date)

@app.route('/download', methods=['GET','POST'])
def download():
    

    return render_template('download.html')

@app.route('/backtestresults', methods=['GET', 'POST'])
def backtesting():
    
    if request.method == 'POST':
        output, plot_path = run_backtest()

        results = output.to_dict()
        
        
        return render_template('backtestresults.html', plot_url=plot_path, results=results)
    return render_template('backtestresults.html')


if __name__ == "__main__":
    app.run(debug=True)
