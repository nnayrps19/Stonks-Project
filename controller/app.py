from flask import Flask, render_template, request, jsonify, redirect, url_for, Response
import pandas as pd
import json
from datetime import *
import matplotlib.pyplot as plt
from model.publisher_subscriber_pattern import *
from model.tradingstrategies import *
from model.data_downloader import *

def create_app():
    app = Flask(__name__, template_folder='../view/templates', static_folder='../view/static')

    @app.route('/', methods=['GET', 'POST'])
    def index():
        max_date = date.today().strftime("%Y-%m-%d")

        if request.method == "POST":
            DH = DataDownloader()
            DataCalc = DataCalculator(DH)

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
            BacktestObject = Context(
                request.form["symbol"],
                request.form["backtest_option"],
                request.form["start_date"],
                request.form["end_date"]
            )
            output, plot_url, trades_csv_path = BacktestObject.run_backtest_option()

            trades_df = pd.read_csv(trades_csv_path)
            trades_html = trades_df.to_html(classes="table table-striped", index=False)

            results = output.to_dict()
            return render_template('backtestresults.html', plot_url=plot_url, results=results, trades_table=trades_html)
        return render_template('backtestresults.html')

    return app