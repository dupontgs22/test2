import yfinance as yf
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd

# Fetching Microsoft stock data for the past 10 years
msft = yf.Ticker("MSFT")
hist = msft.history(period="10y")

# Resampling data to get the daily data
daily_data = hist.resample('D').ffill()

# Calculating 50-day and 200-day moving averages
daily_data['MA50'] = daily_data['Close'].rolling(window=50).mean()
daily_data['MA200'] = daily_data['Close'].rolling(window=200).mean()

# Generating Candlestick data
candlestick_data = daily_data[['Open', 'High', 'Low', 'Close']]
candlestick_data.reset_index(inplace=True)
candlestick_data['Date'] = candlestick_data['Date'].map(mdates.date2num)

# Plotting
fig, ax = plt.subplots()
ax.xaxis_date()

# Plotting candlestick chart
candlestick_ohlc(ax, candlestick_data.values, width=0.6, colorup='g', colordown='r')

# Plott

# Adding legend
ax.legend()

# Rotating dates for better readability
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
