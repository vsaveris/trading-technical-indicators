"""
Trading-Technical-Indicators (tti) python library

File name: run_all_examples.py
    Run example code for all the trading technical indicators.

Use as:
    python run_all_examples.py
"""

import time
import random
import inspect
import pandas as pd
import tti.indicators as ti


def execute_example_code(indicator_object, output_file=None, add_info=None,
                         figures_output_path=None, **kwargs):
    """
    Executes the tti API for all the indicators in the list for the input data.

    Parameters:
        indicator_object (tti.indicators object): The indicator object for
            which the tti API should be executed.

        output_file (file object, default is None): File object where the
            execution output is redirected. If None, output goes to console.

        add_info (str, default is None): Additional information for the running
            example, is used for information purposes in the printing functions
            and in the name of the produced graph.

        figures_output_path (str, default is None): Path for saving the
            indicator graph.

        **kwargs: Arguments to be passed in the indicator constructor.

    Raises:
        -

    Returns:
        -
    """

    start_time = time.time()

    indicator = indicator_object(**kwargs)

    print('\nExample code execution for technical indicator: ',
          type(indicator).__name__,
          (' (' + add_info + ')') if add_info is not None else '', sep='',
          file=output_file)

    print('\n- Indicator calculated in:', round(time.time() - start_time,
        2), 'seconds.', file=output_file)

    # Save graph for the calculated indicator
    graph_name_suffix = ('_' + add_info) if add_info is not None else ''
    output_file_name = figures_output_path + 'example_' + \
        type(indicator).__name__ + graph_name_suffix + '.png'

    fig = indicator.getTiGraph()
    fig.savefig(output_file_name)
    fig.close()

    print('\n- Graph', output_file_name, 'saved.', file=output_file)

    # Get indicator's calculated data
    print('\n- Technical Indicator data:\n', indicator.getTiData(),
          file=output_file)

    # Get indicator's value for a specific date (randomly chosen)
    date = indicator.getTiData().index[random.randint(0,
        len(indicator.getTiData().index) - 1)]
    print('\n- Technical Indicator value at ', date, ' : ',
        indicator.getTiValue(date), sep='', file=output_file)

    # Get the most recent indicator's value
    print('\n- Technical Indicator value at', indicator.getTiData().index[-1],
          ':', indicator.getTiValue(), file=output_file)

    # Get signal from indicator
    print('\n- Technical Indicator signal:', indicator.getTiSignal(),
          file=output_file)


if __name__ == '__main__':

    # Read data from csv file. Set the index to the correct column
    # (dates column)
    df = pd.read_csv('./data/sample_data.csv', parse_dates=True, index_col=0)

    # File object to redirect the output of the execution
    out_file = open('README.txt', 'w')
    print('Example code for the usage of the tti.indicators package ' +
          '(all indicators).', file=out_file)

    # Run example code for all the indicators implemented in the tti.indicators
    # package
    for x in inspect.getmembers(ti):

        if inspect.isclass(x[1]):

            # Moving Average includes five indicators
            if x[1] == ti.MovingAverage:
                execute_example_code(indicator_object=x[1],
                    output_file=out_file, add_info='simple',
                    figures_output_path='./figures/',
                    input_data=df[df.index >= '2012-01-01'],
                    ma_type='simple')

                execute_example_code(indicator_object=x[1],
                    output_file=out_file, add_info='exponential',
                    figures_output_path='./figures/',
                    input_data=df[df.index >= '2012-01-01'],
                     ma_type='exponential')

                execute_example_code(indicator_object=x[1],
                    output_file=out_file, add_info='time_series',
                    figures_output_path='./figures/',
                    input_data=df[df.index >= '2012-01-01'],
                    ma_type='time_series')

                execute_example_code(indicator_object=x[1],
                    output_file=out_file, add_info='triangular',
                    figures_output_path='./figures/',
                    input_data=df[df.index >= '2012-01-01'],
                    ma_type='triangular')

                execute_example_code(indicator_object=x[1],
                    output_file=out_file, add_info='variable',
                    figures_output_path='./figures/',
                    input_data=df[df.index >= '2012-01-01'],
                    ma_type='variable')

            # Stochastic Oscillator includes two indicators
            elif x[1] == ti.StochasticOscillator:
                execute_example_code(indicator_object=x[1],
                    output_file=out_file,
                    add_info='fast',
                    figures_output_path='./figures/',
                    input_data=df[df.index >= '2012-01-01'],
                    k_slowing_periods=1)

                execute_example_code(indicator_object=x[1],
                    output_file=out_file, add_info='slow',
                    figures_output_path='./figures/',
                    input_data=df[df.index >= '2012-01-01'],
                    k_slowing_periods=3)

            else:
                execute_example_code(indicator_object=x[1],
                    output_file=out_file, add_info=None,
                    figures_output_path='./figures/',
                    input_data=df[df.index >= '2012-01-01'])
