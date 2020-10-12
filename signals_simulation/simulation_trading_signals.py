"""
Trading-Technical-Indicators (tti) python library

File name: simulation_trading_signals.py
    Trading simulation code for evaluating the Trading Signals implemented
    for each trading technical indicator.

Use as:
    python simulation_trading_signals.py tti.indicators.<Indicator_Class_name> [<indicator_param> ...]
"""

import re
import sys
import pandas as pd
from trading_simulator import TradingSimulator

import tti.indicators
from tti.utils import fillMissingValues
from tti.utils.exceptions import NotEnoughInputData


def readArguments(input_args):
    """
    Reads and validates the input arguments.

    Parameters:
        input_args (list): The input arguments (sys.argv).

    Raises:
        -

    Returns:
        (tti.indicators class name): The requested indicator class name.

        (str): Indicator's name, to be used as a part of the graph title.

        (str): The graph file name.
    """

    # Get trading technical indicator argument
    if len(input_args) < 2:
        print('Indicator argument is missing. Run simulator as: python ' +
              'simulation_trading_signals.py tti.indicators.<indicator_' +
              'class_name> [<indicator_param> ...]')
        exit(-1)

    if 'tti.indicators.' not in input_args[1]:
        print('Invalid indicator argument, it should be in the format: ' +
              'tti.indicators.<indicator_class_name>')
        exit(-1)

    try:
        indicator = eval(input_args[1])
    except:
        print('Indicator `' + input_args[1] + '` is not supported.')
        exit(-1)

    indicator_name = \
        ' '.join(x for x in re.findall('[A-Z][^A-Z]*',
                                       input_args[1].split('.')[-1]))

    graph_file = \
        '_'.join(x.lower() for x in re.findall('[A-Z][^A-Z]*',
                                               input_args[1].split('.')[-1]))

    graph_file = './figures/simulation_' + graph_file + '.png'

    return indicator, indicator_name, graph_file


def getIndicatorSignal(indicator_name, data, date, input_args):
    """
    Creates the indicator based on the input arguments.

    Parameters:
        indicator_name (tti.indicators class name): The requested indicator
        class name.

        data (pandas.DataFrame): The input data.

        date (str): Date in format YYYY-MM-DD. data.index <= date are
        considered.

        input_args (list): The input arguments (sys.argv).

    Raises:
        -

    Returns:
        (TRADE_SIGNALS): The trading signal returned by the indicator.
    """

    if len(input_args) == 3:
        return indicator_name(
            data[data.index <= date],
            int(input_args[2]) if '.' not in input_args[2] else
            float(input_args[2])).getTiSignal()

    elif len(input_args) == 4:
        return indicator_name(
            data[data.index <= date],
            int(input_args[2]) if '.' not in input_args[2] else
            float(input_args[2]),
            int(input_args[3]) if '.' not in input_args[3] else
            float(input_args[3])).getTiSignal()
    else:
        return indicator_name(data[data.index <= date]).getTiSignal()


# Read data from csv file. Set the index to the correct column (dates column)

df = pd.read_csv('./data/sample_data.csv', parse_dates=True, index_col=0)

# Fill missing values (it sorts also on index ascending)
df = fillMissingValues(df)

ti_class, ti_name, gf_name = readArguments(sys.argv)

# Trading simulation based on the indicator's trading signals
ts = TradingSimulator(ti_name)

for current_date in df.index:

    # Get trading signal
    # Supports up to two passing arguments (int or float)
    try:
        signal = getIndicatorSignal(ti_class, df, current_date, sys.argv)

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

print(ti_name + ' trading signal simulation statistics')
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

history_graph.savefig(gf_name)
