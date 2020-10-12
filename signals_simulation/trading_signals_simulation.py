"""
Trading-Technical-Indicators (tti) python library

File name: trading_signals_simulation.py
    Trading simulation code for evaluating the Trading Signals implemented
    for each trading technical indicator.
"""

import re
import sys
import pandas as pd
from trading_simulator import TradingSimulator

import tti.indicators
from tti.utils import fillMissingValues
from tti.utils.exceptions import NotEnoughInputData

# Get trading technical indicator argument
if len(sys.argv) < 2:
    print('Indicator argument is missing. Run simulator as: python ' +
          'trading_signals_simulation.py tti.indicators.<indicator_' +
          'class_name>')
    exit(-1)

if 'tti.indicators.' not in sys.argv[1]:
    print('Invalid indicator argument, it should be in the format: ' +
          'tti.indicators.<indicator_class_name>')
    exit(-1)

try:
    indicator = eval(sys.argv[1])
except:
    print('Indicator `' + sys.argv[1] + '` is not supported.')
    exit(-1)

indicator_name = ' '.join(x for x in re.findall('[A-Z][^A-Z]*',
                                                sys.argv[1].split('.')[-1]))

indicator_graph_name = \
    '_'.join(x.lower() for x in re.findall('[A-Z][^A-Z]*',
                                           sys.argv[1].split('.')[-1]))
indicator_graph_name = \
    './figures/simulation_' + indicator_graph_name.lower()  + '.png'

# Read data from csv file. Set the index to the correct column (dates column)
df = pd.read_csv('./data/sample_data.csv', parse_dates=True, index_col=0)

# Fill missing values (it sorts also on index ascending)
df = fillMissingValues(df)

# Trading simulation based on the indicator's trading signals
ts = TradingSimulator(indicator_name)

for current_date in df.index:

    # Get trading signal
    # Supports up to two passing arguments (int or float)
    try:
        if len(sys.argv) == 3:
            signal = indicator(
                df[df.index <= current_date],
                int(sys.argv[2]) if '.' not in sys.argv[2] else
                float(sys.argv[2])).getTiSignal()
        elif len(sys.argv) == 4:
            signal = indicator(
                df[df.index <= current_date],
                int(sys.argv[2]) if '.' not in sys.argv[2] else
                float(sys.argv[2]),
                int(sys.argv[3]) if '.' not in sys.argv[3] else
                float(sys.argv[3])).getTiSignal()
        else:
            signal = indicator(df[df.index <= current_date]).getTiSignal()

    except NotEnoughInputData as e:
        print('Error: ', e, ' Skipping this simulation round.', sep='')
        continue

    # If `buy` signal, then buy one stock at `close` price
    if signal[0] == 'buy':
        ts.buyStocks(price=df.at[current_date, 'close'])

    # If `sell` signal, then sell all stocks at `close` price
    elif signal[0] == 'sell':
        ts.sellStocks(price=df.at[current_date, 'close'])

portfolio_data = ts.getPortfolioInfo(df['close'].iat[-1])
transactions_data = ts.getTransactionsInfo()
history_graph = ts.getHistoryGraph()

print(indicator_name + ' trading signal simulation statistics')
print('- Trading Statistics')
print('\t- trading days        :', len(df.index))
print('\t- buy signals         :', transactions_data['executed_buy_orders'])
print('\t- sell signals        :', transactions_data['executed_sell_orders'])
print('\t- ignored buy signals :', transactions_data['ignored_buy_orders'])
print('\t- ignored sell signals:', transactions_data['ignored_sell_orders'])
print('- Portfolio Information')
print('\t- balance             :', round(portfolio_data['balance'], 2))
print('\t- stocks              :', portfolio_data['stocks'])
print('\t- stocks latest price :', df['close'].iat[-1])
print('\t- total value         :', round(portfolio_data['total_value'], 2))

history_graph.savefig(indicator_graph_name)
