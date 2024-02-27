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

# Plotting moving averages
ax.plot(daily_data.index, daily_data['MA50'], color='blue', label='50-Day MA')
ax.plot(daily_data.index, daily_data['MA200'], color='red', label='200-Day MA')

# Marking when the 50-day crosses above or below the 200-day
crossings = []
for i in range(1, len(daily_data)):
    if daily_data['MA50'][i] > daily_data['MA200'][i] and daily_data['MA50'][i - 1] <= daily_data['MA200'][i - 1]:
        crossings.append((daily_data.index[i], daily_data['MA50'][i], 'golden'))
    elif daily_data['MA50'][i] < daily_data['MA200'][i] and daily_data['MA50'][i - 1] >= daily_data['MA200'][i - 1]:
        crossings.append((daily_data.index[i], daily_data['MA50'][i], 'death'))

for date, price, marker in crossings:
    ax.annotate(marker, xy=(date, price), xytext=(-10, 10), textcoords='offset points', arrowprops=dict(arrowstyle='->', color='black'))

# Adding labels and title
ax.set_xlabel('Date')
ax.set_ylabel('Price')
ax.set_title('Microsoft Stock Prices')

# Adding legend
ax.legend()

# Rotating dates for better readability
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
