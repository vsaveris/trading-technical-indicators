"""
Trading-Technical-Indicators (tti) python library

File name: run_all_simulation.py
    Run trading simulation for all the trading technical indicators.

Use as:
    python run_all_simulation.py
"""

import time
import inspect
import pandas as pd
import tti.indicators as ti


def execute_simulation(indicator_object, close_values, output_file=None,
                       add_info=None, figures_output_path=None, **kwargs):
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

    indicator = indicator_object(**kwargs)

    print('\nTrading Simulation for technical indicator: ',
          type(indicator).__name__,
          (' (' + add_info + ')') if add_info is not None else '', sep='',
          file=output_file)

    start_time = time.time()

    # Execute simulation
    simulation, statistics, graph = indicator.getTiSimulation(
        close_values=close_values)

    print('\n- Simulation executed in :', round(time.time() - start_time, 2),
          'seconds.', file=output_file)

    # Save graph for the calculated indicator
    graph_name_suffix = ('_' + add_info) if add_info is not None else ''
    output_file_name = figures_output_path + 'simulation_' + \
        type(indicator).__name__ + graph_name_suffix + '.png'

    graph.savefig(output_file_name)
    graph.close()

    print('\n- Graph', output_file_name, 'saved.', file=output_file)

    # Get simulation statistics
    print('\n- Simulation Statistics:', file=output_file)
    for key, value in statistics.items():
        print('\t', key, ': ', value, sep='', file=output_file)


if __name__ == '__main__':

    # Read data from csv file. Set the index to the correct column
    # (dates column)
    df = pd.read_csv('./data/SCMN.SW.csv', parse_dates=True, index_col=0)

    # File object to redirect the output of the execution
    out_file = open('README.txt', 'w')
    print('Trading Simulation for the tti.indicators package ' +
          '(all indicators).', file=out_file)

    # Run simulation for all the indicators implemented in the tti.indicators
    # package
    for x in inspect.getmembers(ti):

        if inspect.isclass(x[1]):

            # Moving Average includes five indicators
            if x[1] == ti.MovingAverage:
                execute_simulation(indicator_object=x[1],
                    close_values=df[['close']],
                    output_file=out_file, add_info='simple',
                    figures_output_path='./figures/',
                    input_data=df,
                    ma_type='simple')

                execute_simulation(indicator_object=x[1],
                    close_values=df[['close']],
                    output_file=out_file, add_info='exponential',
                    figures_output_path='./figures/',
                    input_data=df,
                     ma_type='exponential')

                execute_simulation(indicator_object=x[1],
                    close_values=df[['close']],
                    output_file=out_file, add_info='time_series',
                    figures_output_path='./figures/',
                    input_data=df,
                    ma_type='time_series')

                execute_simulation(indicator_object=x[1],
                    close_values=df[['close']],
                    output_file=out_file, add_info='triangular',
                    figures_output_path='./figures/',
                    input_data=df,
                    ma_type='triangular')

                execute_simulation(indicator_object=x[1],
                    close_values=df[['close']],
                    output_file=out_file, add_info='variable',
                    figures_output_path='./figures/',
                    input_data=df,
                    ma_type='variable')

            # Stochastic Oscillator includes two indicators
            elif x[1] == ti.StochasticOscillator:
                execute_simulation(indicator_object=x[1],
                    close_values=df[['close']],
                    output_file=out_file,
                    add_info='fast',
                    figures_output_path='./figures/',
                    input_data=df,
                    k_slowing_periods=1)

                execute_simulation(indicator_object=x[1],
                    close_values=df[['close']],
                    output_file=out_file, add_info='slow',
                    figures_output_path='./figures/',
                    input_data=df,
                    k_slowing_periods=3)

            else:
                execute_simulation(indicator_object=x[1],
                    close_values=df[['close']],
                    output_file=out_file, add_info=None,
                    figures_output_path='./figures/',
                    input_data=df)
