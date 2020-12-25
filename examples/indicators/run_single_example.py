"""
Trading-Technical-Indicators (tti) python library

File name: run_single_example.py
    Example code for the trading technical indicators.

Use as:
    python run_single_example.py tti.indicators.<indicator_class_name>
        [**kwargs]
"""

import re
import sys
import time
import random
import pandas as pd
import tti.indicators


if __name__ == '__main__':

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
            input_arg[1]) else (float(input_arg[1]) if re.match(
            '^[0-9]*\.[0-9]]*$', input_arg[1]) else input_arg[1])

    print('Trading Example for the', indicator, 'with arguments', kwargs)

    # Read data from csv file. Set the index to the correct column
    # (dates column)
    df = pd.read_csv('./data/sample_data.csv', parse_dates=True, index_col=0)

    start_time = time.time()

    # Create the indicator for a part of the input file
    ti = indicator(input_data=df, **kwargs)

    print('\nIndicator created in :', round(time.time() - start_time, 2),
          'seconds.')

    # Show the Graph for the calculated Technical Indicator
    ti.getTiGraph().show()

    # Get indicator's calculated data
    print('\nTechnical Indicator data:\n', ti.getTiData())

    # Get indicator's value for a specific date
    print('\nTechnical Indicator value at random date:', ti.getTiValue(
        ti.getTiData().index[random.randint(0, len(ti.getTiData().index) - 1)])
          )

    # Get the most recent indicator's value
    print('\nTechnical Indicator value at', ti.getTiData().index[-1], ':',
        ti.getTiValue())

    # Get signal from indicator
    print('\nTechnical Indicator signal:', ti.getTiSignal())
