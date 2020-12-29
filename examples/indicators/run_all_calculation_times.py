"""
Trading-Technical-Indicators (tti) python library

File name: run_all_calculation_times.py
    Run example code for all the trading technical indicators and return
    calculation times. To be used as source for the optimization of indicators
    calculation.

Use as:
    python run_all_calculation_times.py
"""

import time
import inspect
import pandas as pd
import tti.indicators as ti


def calculate_ti(indicator_object, output_file=None, add_info=None, **kwargs):
    """
    Creates the indicator ``indicator_object`` and measures the calculation
    time.

    Parameters:
        indicator_object (tti.indicators object): The indicator object for
            which the tti API should be executed.

        output_file (file, default=None): File object where the calculation
            time is redirected. If None, output goes to console.

        add_info (str, default is None): Additional information for the running
            calculation, is used for information purposes in the printing
            functions.

        **kwargs: Arguments to be passed to the indicator constructor.
    """

    start_time = time.time()

    indicator = indicator_object(**kwargs)

    ti_name = str(type(indicator).__name__) + \
        (' (' + add_info + ')' if add_info is not None else '')

    print(ti_name, ',', round(time.time() - start_time,2), sep='',
          file=output_file)


if __name__ == '__main__':

    # Read data from csv file. Set the index to the correct column
    # (dates column)
    df = pd.read_csv('./data/sample_data.csv', parse_dates=True, index_col=0)

    # File object to redirect the output of the execution
    out_file = open('Calculation_times.csv', 'w')
    print('indicator,calculation_time_in_seconds', file=out_file)

    # Run all the indicators implemented in the tti.indicators package
    for x in inspect.getmembers(ti):

        if inspect.isclass(x[1]):

            # Moving Average includes five indicators
            if x[1] == ti.MovingAverage:
                calculate_ti(indicator_object=x[1],
                    output_file=out_file, add_info='simple',
                    input_data=df,
                    ma_type='simple')

                calculate_ti(indicator_object=x[1],
                    output_file=out_file, add_info='exponential',
                    input_data=df,
                     ma_type='exponential')

                calculate_ti(indicator_object=x[1],
                    output_file=out_file, add_info='time_series',
                    input_data=df,
                    ma_type='time_series')

                calculate_ti(indicator_object=x[1],
                    output_file=out_file, add_info='triangular',
                    input_data=df,
                    ma_type='triangular')

                calculate_ti(indicator_object=x[1],
                    output_file=out_file, add_info='variable',
                    input_data=df,
                    ma_type='variable')

            # Stochastic Oscillator includes two indicators
            elif x[1] == ti.StochasticOscillator:
                calculate_ti(indicator_object=x[1],
                    output_file=out_file,
                    add_info='fast',
                    input_data=df,
                    k_slowing_periods=1)

                calculate_ti(indicator_object=x[1],
                    output_file=out_file, add_info='slow',
                    input_data=df,
                    k_slowing_periods=3)

            else:
                calculate_ti(indicator_object=x[1],
                    output_file=out_file, add_info=None,
                    input_data=df)
