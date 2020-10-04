"""
Trading-Technical-Indicators (tti) python library

File name: simulation_exponential_moving_average.py
    Trading signals simulation code for the Exponential Moving Average
    technical indicator.
"""

import pandas as pd

from tti.indicators import ExponentialMovingAverage
from tti.utils import fillMissingValues

# Read data from csv file. Set the index to the correct column (dates column)
df = pd.read_csv('./data/sample_data.csv', parse_dates=True, index_col=0)

# Fill missing values (it sorts also on index ascending)
df = fillMissingValues(df)

# Trading simulation based on the indicator's trading signals
balance = 0.0
number_of_stocks = 0
number_of_buy_signals = 0
number_of_sell_signals = 0
number_of_ignored_sell_signals = 0
lowest_balance = 0.0
highest_balance = 0.0
highest_number_of_stocks = 0

for current_date in df.index:
    # Get trading signal
    ts = ExponentialMovingAverage(df[df.index <= current_date]).getTiSignal()

    # If `buy` signal, then buy one stock at `close` price
    if ts[0] == 'buy':
        number_of_buy_signals += 1
        balance -= df.at[current_date, 'close']
        number_of_stocks += 1
        lowest_balance = min(lowest_balance, balance)

    # If `sell` signal, then sell all stocks at `close` price
    elif ts[0] == 'sell':
        number_of_sell_signals += 1

        if number_of_stocks == 0:
            number_of_ignored_sell_signals += 1

        highest_number_of_stocks = max(highest_number_of_stocks,
                                       number_of_stocks)
        balance += number_of_stocks*df.at[current_date, 'close']
        number_of_stocks = 0
        highest_balance = max(highest_balance, balance)

print('Exponential Moving Average trading signal simulation statistics')
print('- number of trading days          :', len(df.index))
print('- number of `buy` signals         :', number_of_buy_signals)
print('- number of `sell` signals        :', number_of_sell_signals)
print('- number of ignored `sell` signals:', number_of_ignored_sell_signals)
print('- lowest balance                  :', lowest_balance)
print('- highest balance                 :', highest_balance)
print('- highest number of stocks        :', highest_number_of_stocks)
print('- initial balance                 : 0.0')
print('- final balance                   :', balance)
print('- final number of stocks          :', number_of_stocks)
print('- final number of stocks (value)  :', number_of_stocks*df.
      at[current_date, 'close'])
