import duka.app.app as import_ticks_method
from duka.core.utils import TimeFrame
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os.path
import mplfinance as mpf
from mplfinance.original_flavor import candlestick_ohlc


# Start date params
start_year = 2019
start_month = 1
start_day = 1

# End date params
end_year = 2019
end_month = 2
end_day = 1


start_date = datetime.date(start_year,start_month,start_day)
end_date = datetime.date(end_year,end_month,end_day)

Assets = ['EURUSD']

replaced_start = str(start_date).replace('-', '_')
replaced_end = end_date

list_group = [start_month, start_day, end_month, end_day]

if  len(str(start_month)) <= 1:
    start_month = str(start_month)
    start_month = f"0{start_month}"

if  len(str(start_day)) <= 1:
    start_day = str(start_day)
    start_day = f"0{start_day}"

if  len(str(end_month)) <= 1:
    end_month = str(end_month)
    end_month = f"0{end_month}"

if  len(str(end_day)) <= 1:
    end_day = str(end_day)
    end_day = f"0{end_day}"

file_csv = f"{Assets[0]}/{Assets[0]}-{start_year}_{start_month}_{start_day}-{end_year}_{end_month}_{end_day}.csv"

def convert_tick_to_ohlc(df,df_column,timeframe):
    data_frame = df[df_column].resample(timeframe).ohlc()
    return data_frame

def plot_candle(data):
    fig = plt.figure(figsize=(8,5))
    ax1 = plt.subplot2grid((1,1), (0,0))

    candle_counter = range(len(data['open'])-1)
    ohlc = []

    for candle in candle_counter:
        append_me = candle_counter[candle], \
            data['open'][candle], \
            data['high'][candle], \
            data['low'][candle], \
            data['close'][candle]
        ohlc.append(append_me)

    candlestick_ohlc(ax1, ohlc, width=0.2, colorup='#075105', colordown='#AF141A')

    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)

    ax1.xaxis.set_major_locator(mticker.MaxNLocator(15))
    ax1.grid(True)
    plt.xlabel('Candle Counter')
    plt.ylabel('Price')
    plt.title(f"{Assets[0]} trades from {start_year}-{start_month}-{start_day} to {end_year}-{end_month}-{end_day}")
    plt.grid(False)
    plt.show()

if os.path.exists(file_csv) == False:
    if  os.path.exists(Assets[0]) == False:
        # Makea directory to hold data for this pair
        os.makedirs(Assets[0])

    # Download financial data
    import_ticks_method(Assets, start_date, end_date, 1, TimeFrame.TICK, Assets[0] + "/", True)

    # Read CSV using pandas
    tick_data = pd.read_csv(file_csv,
                            index_col = ["time"],
                            usecols = ["time", "ask", "bid"],
                            parse_dates = ["time"])
    tick_data.head()
    data_ask = convert_tick_to_ohlc(tick_data, "ask", "240Min")
    data_ask.head()
    print(data_ask)
    plot_candle(data_ask)
else:
    
    tick_data = pd.read_csv(file_csv,
                            index_col = ["time"],
                            usecols = ["time", "ask", "bid"],
                            parse_dates = ["time"])
    tick_data.head()
    data_ask = convert_tick_to_ohlc(tick_data, "ask", "240Min")
    data_ask.head()
    # print(data_ask)
    plot_candle(data_ask)