import json
import pandas as pd
import matplotlib.pyplot as plt

# Load the JSON data from a file
with open('history.json', 'r') as file:
    data = json.load(file)

# Convert the JSON data to a Pandas DataFrame
df = pd.DataFrame(data).T  # Transpose to have dates as index
df.index = pd.to_datetime(df.index)  # Convert index to datetime

# Function to extract data based on ETF symbol
def extract_etf_data(etf_symbol):
    columns = [col for col in df.columns if etf_symbol in col]
    return df[columns]

# User Input: ETF Symbol and Date Range
etf_symbol = input("Enter the ETF symbol (FNGU or FNGD): ").upper()
start_date = input("Enter start date (YYYY-MM-DD): ")
end_date = input("Enter end date (YYYY-MM-DD): ")

# Filter Data based on user inputs
etf_data = extract_etf_data(etf_symbol)
filtered_data = etf_data[start_date:end_date]

# Plotting the data
plt.figure(figsize=(10, 5))
plt.plot(filtered_data.index, filtered_data[('Adj Close', etf_symbol)], label='Adj Close')
plt.plot(filtered_data.index, filtered_data[('Open', etf_symbol)], label='Open', linestyle='--')
plt.plot(filtered_data.index, filtered_data[('Close', etf_symbol)], label='Close', linestyle='-.')
plt.plot(filtered_data.index, filtered_data[('High', etf_symbol)], label='High', linestyle=':')
plt.plot(filtered_data.index, filtered_data[('Low', etf_symbol)], label='Low', linestyle='-.')

# Adding labels and legend
plt.title(f"{etf_symbol} Historical Prices")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.show()
