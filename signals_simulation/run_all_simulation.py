"""
Trading-Technical-Indicators (tti) python library

File name: run_all_simulation.py
    Run trading simulation for all the trading technical indicators or for
    a single indicator given.

Use as:
    python run_all_simulation.py [indicator_class_name [**kwargs]]
"""

import sys
import json
import time
import inspect
import pandas as pd
import tti.indicators as ti
import matplotlib.pyplot as plt


def getSimulationGraph(simulation, close_values, title):
    """
    Returns a matplotlib.pyplot graph with simulation data.

    Parameters:
        simulation (pandas.DataFrame): Simulation data returned from the
            runSimulation method of the tti.indicators package.

        close_values (pandas.DataFrame): The close value of the stock, for the
            whole simulation period. Index is of type DateTimeIndex with same
            values as the input to the indicator data. It contains one column
            `close`.

        title (str): Title of the graph.

    Returns:
        (matplotlib.pyplot): The produced graph.
    """

    plt.figure(figsize=(7, 5))

    plt.subplot(3, 1, 1)
    plt.plot(list(range(1, len(close_values['close']) + 1)),
        close_values['close'], label='close_price', color='limegreen')
    plt.legend(loc=0)
    plt.grid(which='major', axis='y', alpha=0.5)
    plt.title(title, fontsize=11, fontweight='bold')
    plt.gca().axes.get_xaxis().set_visible(False)

    plt.subplot(3, 1, 2)
    plt.plot(list(range(1, len(simulation['stocks_in_possession']) + 1)),
        simulation['stocks_in_possession'], label='stocks_in_possession',
        color='tomato')
    plt.legend(loc=0)
    plt.grid(which='major', axis='y', alpha=0.5)
    plt.gca().axes.get_xaxis().set_visible(False)

    plt.subplot(3, 1, 3)
    plt.plot(list(range(1, len(simulation['total_value']) + 1)),
        simulation['total_value'], label='total_value', color='cornflowerblue')
    plt.legend(loc=0)
    plt.grid(which='major', axis='y', alpha=0.5)

    plt.xlabel('Transactions', fontsize=11, fontweight='bold')
    plt.gcf().text(0.04, 0.5, 'Total Value | Stocks | Price', fontsize=11,
        fontweight='bold', va='center', rotation='vertical')

    return plt


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

        output_file (file, default=None): File object where the execution
            output is redirected. If None, output goes to console.

        add_info (str, default=None): Additional information for the running
            example, is used for information purposes in the printing functions
            and in the name of the produced graph.

        figures_output_path (str, default=None): Path for saving the
            indicator graph. If None, the graph is just shown.

        **kwargs: Arguments to be passed in the indicator constructor.
    """

    indicator = indicator_object(**kwargs)

    print('\nTrading Simulation for technical indicator: ',
          type(indicator).__name__,
          (' (' + add_info + ')') if add_info is not None else '', sep='',
          file=output_file)

    start_time = time.time()

    # Execute simulation
    simulation, statistics = indicator.runSimulation(close_values=close_values)

    print('\n- Simulation executed in :', round(time.time() - start_time, 2),
          'seconds.', file=output_file)

    # Save graph for the calculated indicator
    graph_name_suffix = ('_' + add_info) if add_info is not None else ''
    output_file_name = figures_output_path + 'simulation_' + \
        type(indicator).__name__ + graph_name_suffix + '.png'

    graph_title_suffix = (' (' + add_info + ')') if add_info is not None else \
        ''
    fig = getSimulationGraph(simulation, close_values,
        'Trading Simulation for ' + type(indicator).__name__ +
        graph_title_suffix)

    # Show or save the graph
    if figures_output_path is None:
        fig.show()
    else:
        fig.savefig(output_file_name)
        fig.close()

    print('\n- Graph', output_file_name, 'saved.', file=output_file)

    # Get simulation statistics
    print('\n- Simulation Statistics:\n', file=output_file)
    for key, value in statistics.items():
        print('-- ', key, ': ', value, sep='', file=output_file)


if __name__ == '__main__':

    # Read data from csv file. Set the index to the correct column
    # (dates column)
    df = pd.read_csv('./data/sample_data.csv', parse_dates=True, index_col=0)

    # Run simulation for the given indicator, if any
    if len(sys.argv) > 1:

        indicator = None

        try:
            indicator = eval(sys.argv[1])
        except:
            print('Error: Not valid indicator class name', sys.argv[1])
            exit()

        # Read the input kwargs (dictionary)
        if len(sys.argv) > 2:
            kwargs_dict = json.loads(sys.argv[2])
        else:
            kwargs_dict = None

        print('Trading Simulation for the', sys.argv[1], 'with arguments',
              kwargs_dict)

        execute_simulation(kwargs_dict,
                           indicator_object=indicator,
                           close_values=df[['close']],
                           output_file=None, add_info=None,
                           figures_output_path=None,
                           input_data=df)

    # Run simulation for all the indicators implemented in the tti.indicators
    # package
    else:
        # File object to redirect the output of the execution
        out_file = open('README.txt', 'w')
        print('Trading Simulation for the tti.indicators package ' +
              '(all indicators).', file=out_file)

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
                        ma_type='time_serie         s')

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
