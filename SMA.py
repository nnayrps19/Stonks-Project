import pandas as pd
import json
import numpy as np
import logging
import matplotlib.pyplot as plt

# Configure logging to file and console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Create a file handler to save logs to 'sma_strategy.log'
file_handler = logging.FileHandler('sma_strategy.log')
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

logger.info("Starting SMA strategy implementation")

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

# Parameters for SMA
short_window = 20  # Short-term SMA period
long_window = 50   # Long-term SMA period
logger.info("Set short SMA window to %d and long SMA window to %d", short_window, long_window)

# Calculate SMAs
logger.info("Calculating short-term and long-term SMAs")
df['SMA_short'] = df['Open'].rolling(window=short_window, min_periods=1).mean()
df['SMA_long'] = df['Open'].rolling(window=long_window, min_periods=1).mean()
logger.info("SMA calculation complete")

# Generate signals
logger.info("Generating buy/sell signals")
df['Signal'] = 0
df['Signal'][short_window:] = np.where(df['SMA_short'][short_window:] > df['SMA_long'][short_window:], 1, 0)
df['Position'] = df['Signal'].diff()

# Identify buy/sell points for visualization
buy_signals = df[df['Position'] == 1]
sell_signals = df[df['Position'] == -1]
logger.info("Buy signals generated: %d", len(buy_signals))
logger.info("Sell signals generated: %d", len(sell_signals))

# Plot the SMA strategy
plt.figure(figsize=(14, 8))
plt.plot(df['Open'], label='Price', color='blue', alpha=0.5)
plt.plot(df['SMA_short'], label=f'SMA {short_window}', color='green')
plt.plot(df['SMA_long'], label=f'SMA {long_window}', color='red')

# Plot buy and sell signals
plt.scatter(buy_signals.index, buy_signals['Open'], label='Buy Signal', marker='^', color='green', alpha=1)
plt.scatter(sell_signals.index, sell_signals['Open'], label='Sell Signal', marker='v', color='red', alpha=1)

# Chart details
plt.title(f'SMA Strategy: Short Window = {short_window}, Long Window = {long_window}')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend(loc='best')
plt.grid()

# Display the plot
logger.info("Displaying the SMA strategy plot")
plt.show()
