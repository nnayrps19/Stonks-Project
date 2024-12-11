import pandas as pd
import json
import numpy as np
import logging
import matplotlib.pyplot as plt

# Configure logging to file and console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Create a file handler to save logs to 'macd_strategy.log'
file_handler = logging.FileHandler('macd_strategy.log')
file_handler.setLevel(logging.INFO)

# Create a console handler for console output
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Set format for both handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info("Starting MACD strategy implementation")

# Load and inspect the JSON data structure
try:
    logger.info("Loading data from history.json")
    with open('history.json') as f:
        data = json.load(f)
    logger.info("Data loaded successfully")

    # Inspect JSON structure and find 'Open' data
    def find_open_data(data):
        if isinstance(data, dict):
            if 'Open' in data and isinstance(data['Open'], dict):
                return data['Open']
            for key, value in data.items():
                if isinstance(value, dict):
                    result = find_open_data(value)
                    if result:
                        return result
        return None

    open_data = find_open_data(data)

    if open_data:
        logger.info("Successfully located 'Open' data with %d entries", len(open_data))
        # Convert 'Open' data to DataFrame
        df = pd.DataFrame(list(open_data.items()), columns=['Timestamp', 'Open'])
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
        df.set_index('Timestamp', inplace=True)
        df.sort_index(inplace=True)
        logger.info("Data converted to DataFrame successfully")
    else:
        logger.error("Unable to locate 'Open' data in JSON structure.")
        raise ValueError("Unexpected JSON format - 'Open' key missing or nested unexpectedly.")

except Exception as e:
    logger.error("Error processing JSON data: %s", e)
    raise

# MACD calculation
short_ema = 12  # Short period for MACD
long_ema = 26   # Long period for MACD
signal_ema = 9  # Signal line period
logger.info("Set MACD parameters: short EMA = %d, long EMA = %d, signal EMA = %d", short_ema, long_ema, signal_ema)

# Calculate MACD line and Signal line
logger.info("Calculating MACD line and Signal line")
df['12_EMA'] = df['Open'].ewm(span=short_ema, adjust=False).mean()
df['26_EMA'] = df['Open'].ewm(span=long_ema, adjust=False).mean()
df['MACD'] = df['12_EMA'] - df['26_EMA']
df['Signal'] = df['MACD'].ewm(span=signal_ema, adjust=False).mean()
logger.info("MACD and Signal line calculation complete")

# Generate buy/sell signals
logger.info("Generating buy/sell signals based on MACD crossover")
df['Position'] = 0
df['Position'] = np.where(df['MACD'] > df['Signal'], 1, 0)
df['Signal_Position'] = df['Position'].diff()

# Extract buy and sell signals for plotting
buy_signals = df[df['Signal_Position'] == 1]
sell_signals = df[df['Signal_Position'] == -1]
logger.info("Buy signals generated: %d", len(buy_signals))
logger.info("Sell signals generated: %d", len(sell_signals))

# Plot the MACD strategy
plt.figure(figsize=(14, 8))

# Plot the stock price
plt.subplot(2, 1, 1)
plt.plot(df['Open'], label='Price', color='blue', alpha=0.5)
plt.title("MACD Strategy with Price")

# Plot MACD and Signal lines
plt.subplot(2, 1, 2)
plt.plot(df['MACD'], label='MACD', color='green')
plt.plot(df['Signal'], label='Signal Line', color='red')
plt.scatter(buy_signals.index, buy_signals['MACD'], label='Buy Signal', marker='^', color='green', alpha=1)
plt.scatter(sell_signals.index, sell_signals['MACD'], label='Sell Signal', marker='v', color='red', alpha=1)

# Chart details
plt.title(f"MACD and Signal Line (Short EMA={short_ema}, Long EMA={long_ema}, Signal EMA={signal_ema})")
plt.xlabel('Date')
plt.ylabel('MACD')
plt.legend(loc='best')
plt.grid()

# Display the plot
logger.info("Displaying the MACD strategy plot")
plt.tight_layout()
plt.show()
