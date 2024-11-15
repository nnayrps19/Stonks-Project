from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import json
from datetime import *
from downloader import *
from stonksbacktest import *
from bollingerbandsbacktest import *
import matplotlib.pyplot as plt


app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def index():
    max_date = date.today().strftime("%Y-%m-%d")
    
    if request.method == "POST":
        today = date.today()
        symbol = request.form["symbol"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        readable_download_new(symbol, '2021-01-01', today)
        with open('history.json', 'r') as file:
            data = json.load(file)

        df = pd.DataFrame.from_dict(data, orient='index')
        df.index = pd.to_datetime(df.index)
        
        

        
        column_name = f"('Adj Close', '{symbol}')"
        
        filtered_data = df[column_name].dropna()
        # Calculates current price, percent change
        current_price = filtered_data.iloc[-1] if not filtered_data.empty else None
        prev_price = filtered_data.iloc[-2] if len(filtered_data) > 1 else current_price
        percent_change = ((current_price - prev_price) / prev_price * 100) if prev_price else 0


        dates = filtered_data.index.strftime('%Y-%m-%d').tolist()
        prices = filtered_data.values.tolist()
        
        return jsonify(dates=dates, prices=prices, current_price=current_price, percent_change=percent_change)
    return render_template('index.html', max_date=max_date)


@app.route('/backtestresults', methods=['GET', 'POST'])
def backtesting():
    
    if request.method == 'POST':
        backtest_option = request.form["backtest_option"]
        symbol = request.form["symbol"]
        if backtest_option == 'SMA':
            output, plot_path = run_backtest(symbol)
        elif backtest_option == 'BB':
            output, plot_path = run_BBS_backtest(symbol)
        elif backtest_option == 'MACD':
            output, plot_path = run_MACD_backtest(symbol)

        results = output.to_dict()
        
        
        return render_template('backtestresults.html', plot_url=plot_path, results=results)
    return render_template('backtestresults.html')


if __name__ == "__main__":
    app.run(debug=True)