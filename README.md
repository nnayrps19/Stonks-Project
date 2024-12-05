# Automated Trading System for FNGU and FNGD ETFs

## Project Overview
This project is an automated trading system designed to trade two highly volatile leveraged ETFs: **FNGU** and **FNGD**. The system leverages technical analysis to generate buy/sell signals based on market data and aims to automate the trading process for users with the goal of achieving at least a 10% annual return.

The system utilizes historical market data from Yahoo Finance and provides a user interface to interact with the data, select trading strategies, and backtest them.

## Features

### 1. Data Management
- **Data Download**: The system downloads historical market data for **FNGU** and **FNGD** from Yahoo Finance, covering the period from 01/01/2020 to the latest market close.
- **Data Storage**: The downloaded data is stored in a local `history.json` file in JSON format, which includes:
  - Date
  - Open price
  - High price
  - Low price
  - Closing price
  - Volume

### 2. User Interface
The system provides a user interface with the following functionality:
- **Select ETF**: Choose between **FNGU** and **FNGD**.
- **Download Data**: Download the selected ETF's historical data to a local JSON file.
- **Market Data Display**: View the latest market date, price, and percentage price change compared to the previous day.
- **Historical Price Graph**: View a graph displaying the historical price for the selected date range.
- **Trading Strategy Selection**: Choose from various trading strategies based on technical indicators.

### 3. Technical Indicators
The system implements three common technical indicators to assist in generating trading signals:
- **Simple Moving Average (SMA)**: Used for trend-following strategies. The system buys when the short-term moving average crosses above the long-term moving average and sells when the opposite occurs.
- **Bollinger Bands (BB)**: Identifies overbought and oversold conditions based on the price relative to the moving average.
- **MACD (Moving Average Convergence Divergence)**: Measures the momentum and trend of the market.

These indicators help automate the decision-making process for trading based on predefined strategies.

### 4. Backtesting
The system includes a **backtesting** feature to evaluate the effectiveness of trading strategies:
- **Initial Account Balance**: Set at $100,000.
- **No Trading Fees**: Assumed no trading fees for simplicity.
- **Backtesting Metrics**: The system tracks and displays key performance metrics, including:
  - Profit/Loss per trade
  - Total profit/loss
  - Return percentage compared to the initial balance
  - Trade log in `trade_log.json`, including:
    - Date of transaction
    - Trade type (buy/sell)
    - Number of shares traded
    - Amount spent on the trade
    - Account balance after the trade

### 5. Logging and Data Persistence
All trades and relevant metrics are logged in a JSON file (`trade_log.json`) for future analysis. The log includes detailed information about each transaction, which can be used for performance evaluation or auditing.

## Technology Stack
- **Programming Language**: Python
- **Libraries**: `pandas`, `matplotlib`, `Flask` (for web interface), `yfinance` (for data retrieval)
- **Data Storage**: JSON file (for simplicity)
- **Technical Indicators**: Implemented using Python libraries and custom logic.

## How to Use

### Prerequisites
- Python 3.9 or higher.
- Required Python libraries listed in `requirements.txt`.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/nnayrps19/Stonks-Project.git
