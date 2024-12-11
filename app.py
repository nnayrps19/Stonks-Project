from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import json
from datetime import *
from tradingstrategies import *
from data_downloader import *
import matplotlib.pyplot as plt


app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def index():
    max_date = date.today().strftime("%Y-%m-%d")
    
    if request.method == "POST":
        #Use of new adapter for data access
        yahoo_finance_data_access = YahooFinanceDataAccess()
        DataClac = YahooFinanceAdapter(yahoo_finance_data_access)
        DataCalc = DataCalculator(DataCalc)

        today = date.today()
        symbol = request.form["symbol"]
        start_date = request.form["start_date"]
        DataCalc.readable_download_new(symbol, '2021-01-01', today)
        end_date = request.form["end_date"]
        
        
        filtered_data = DataCalc.get_filtered_data(symbol,start_date,end_date)
        # Calculates current price, percent change
        current_price, percent_change = DataCalc.calculate_prices(filtered_data)

        dates = filtered_data.index.strftime('%Y-%m-%d').tolist()
        prices = filtered_data.values.tolist()
        
        return jsonify(dates=dates, prices=prices, current_price=current_price, percent_change=percent_change)
    return render_template('index.html', max_date=max_date)


@app.route('/backtestresults', methods=['GET', 'POST'])
def backtesting(): 
    if request.method == 'POST':
        BacktestObject = Context.__init__("BTObject", request.form["symbol"], request.form["backtest_option"], request.form["start_date"], request.form["end_date"])
        output, plot_url, trades_csv_path = BacktestObject.run_backtest_option()

        trades_df = pd.read_csv(trades_csv_path)
        trades_html = trades_df.to_html(classes="table table-striped", index=False)
        
        results = output.to_dict()
        return render_template('backtestresults.html', plot_url=plot_url, results=results, trades_table=trades_html)
    return render_template('backtestresults.html')


if __name__ == "__main__":
    app.run(debug=True) 