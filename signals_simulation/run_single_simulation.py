"""
Trading-Technical-Indicators (tti) python library

File name: run_single_simulation.py
    Run trading simulation for a single trading technical indicators.

Use as:
    python run_single_simulation.py tti.indicators.<indicator_class_name>
        [**kwargs]
"""

import time
import sys
import pandas as pd
import matplotlib.pyplot as plt
import re
import tti.indicators


def execute_simulation(indicator_object, close_values, **kwargs):
    """
    Executes trading simulation for all the indicators in the list for the
    input data.

    Parameters:
        indicator_object (tti.indicators object): The indicator object for
            which the tti API should be executed.

        close_values (pandas.DataFrame): The close value of the stock, for the
            whole simulation period. Index is of type DateTimeIndex with same
            values as the input to the indicator data. It contains one column
            `close`.

        **kwargs: Arguments to be passed in the indicator constructor.

    Raises:
        -

    Returns:
        -
    """

    indicator = indicator_object(**kwargs)

    print('\nTrading Simulation for technical indicator: ',
          type(indicator).__name__)

    start_time = time.time()

    # Execute simulation
    simulation, statistics, graph = indicator.getTiSimulation(
        close_values=close_values)

    print('\n- Simulation executed in :', round(time.time() - start_time, 2),
          'seconds.')

    # Show graph for the calculated indicator
    #graph.show()
    graph.savefig('foo.png')

    # Get simulation statistics
    print('\n- Simulation Statistics:')
    for key, value in statistics.items():
        print('\t', key, ': ', value, sep='')


if __name__ == '__main__':

    # Read data from csv file. Set the index to the correct column
    # (dates column)
    df = pd.read_csv('./data/SCMN.SW.csv', parse_dates=True, index_col=0)

    indicator_class_name = None

    if len(sys.argv) > 1 and re.match('^tti\.indicators\.[A-Z,a-z]*$',
                                      sys.argv[1]):
        indicator_class_name = sys.argv[1]

    try:
        indicator = eval(indicator_class_name)
    except:
        print('Invalid technical indicator', indicator_class_name)
        exit()

    kwargs = {}

    for i in range(2, len(sys.argv)):

        input_arg = sys.argv[i].split('=')
        kwargs[input_arg[0]] = int(input_arg[1]) if re.match('^[0-9]*$',
            input_arg[1]) else (float(input_arg[1]) if
            re.match('^[0-9]*\.[0-9]]*$', input_arg[1]) else input_arg[1])

    print('Trading Simulation for the', indicator, 'with arguments', kwargs)

    # Run simulation
    execute_simulation(indicator_object=indicator,
                       close_values=df[['close']],
                       input_data=df,
                       **kwargs)
