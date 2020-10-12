"""
Trading-Technical-Indicators (tti) python library

File name: example_technical_indicator.py
    Example code for the trading technical indicators.

Use as:
    python example_technical_indicator.py tti.indicators.<Indicator_Class_name> [<indicator_param> ...]
"""

import re
import sys
import pandas as pd
import tti.indicators


def readArguments(input_args):
    """
    Reads and validates the input arguments.

    Parameters:
        input_args (list): The input arguments (sys.argv).

    Raises:
        -

    Returns:
        (tti.indicators class name): The requested indicator class name.

        (str): The graph file name.
    """

    # Get trading technical indicator argument
    if len(input_args) < 2:
        print('Indicator argument is missing. Run as: python ' +
              'example_technical_indicator.py tti.indicators.<indicator_' +
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

    graph_file = \
        '_'.join(x.lower() for x in re.findall('[A-Z][^A-Z]*',
                                               input_args[1].split('.')[-1]))

    graph_file = './figures/example_' + graph_file + '.png'

    return indicator, graph_file


def createIndicator(indicator_name, data, input_args):
    """
    Creates the indicator based on the input arguments.

    Parameters:
        indicator_name (tti.indicators class name): The requested indicator
        class name.

        data (pandas.DataFrame): The input data.

        input_args (list): The input arguments (sys.argv).

    Raises:
        -

    Returns:
        (tti.indicators object: The created indicator object.
    """

    if len(input_args) == 3:
        return indicator_name(
            data[data.index >= '2012-01-01'],
            int(input_args[2]) if '.' not in input_args[2] else
            float(input_args[2]))

    elif len(input_args) == 4:
        return indicator_name(
            data[data.index >= '2012-01-01'],
            int(input_args[2]) if '.' not in input_args[2] else
            float(input_args[2]),
            int(input_args[3]) if '.' not in input_args[3] else
            float(input_args[3]))
    else:
        return indicator_name(data[data.index >= '2012-01-01'])


if __name__ == '__main__':

    ti_name, gf_name = readArguments(sys.argv)

    # Read data from csv file. Set the index to the correct column
    # (dates column)
    df = pd.read_csv('./data/sample_data.csv', parse_dates=True, index_col=0)

    # Create the indicator for a part of the input file
    ti = createIndicator(ti_name, df, sys.argv)

    # Show the Graph for the calculated Technical Indicator
    ti.getTiGraph().show()

    ti.getTiGraph().savefig(gf_name)
    print('- Graph ' + gf_name + ' saved.')

    # Get indicator's calculated data
    print('\nTechnical Indicator data:\n', ti.getTiData())

    # Get indicator's value for a specific date
    print('\nTechnical Indicator value at 2012-09-06:',
          ti.getTiValue('2012-09-06'))

    # Get the most recent indicator's value
    print('\nTechnical Indicator value at', ti.getTiData().index[-1], ':',
          ti.getTiValue())

    # Get signal from indicator
    print('\nTechnical Indicator signal:', ti.getTiSignal())
