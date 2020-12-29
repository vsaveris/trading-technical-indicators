"""
Trading-Technical-Indicators (tti) python library

File name: test_indicator_moving_average_simple.py
    tti.indicators package, _moving_average.py module unit tests.
    Time Series Moving Average
"""

import unittest
import tti.indicators
from test_indicators_common import TestIndicatorsCommon

import pandas as pd
import re


class TestSimpleMovingAverage(unittest.TestCase, TestIndicatorsCommon):

    indicator = tti.indicators.MovingAverage

    ti_data_rows = [0, 1]

    df = pd.read_csv('./data/sample_data.csv', parse_dates=True, index_col=0)

    indicator_input_arguments = {'period': 20, 'ma_type': 'time_series'}

    indicator_other_input_arguments = [
        {'period': 2, 'ma_type': 'time_series'},
        {'period': 3169, 'ma_type': 'time_series'}
    ]

    indicator_minimum_required_data = indicator_input_arguments['period']

    mandatory_arguments_missing_cases = []

    required_input_data_columns = ['close']

    # Tested already with the Simple Moving Average
    arguments_wrong_type = []

    # Tested already with the Simple Moving Average
    arguments_wrong_value = []

    graph_file_name = '_'.join(
        x.lower() for x in re.findall('[A-Z][^A-Z]*', str(
            indicator).split('.')[-1][:-2]))

    graph_file_name = './figures/test_' + graph_file_name + '_time_series.png'

    indicator_test_data_file_name = '_'.join(
        x.lower() for x in re.findall('[A-Z][^A-Z]*', str(
            indicator).split('.')[-1][:-2]))

    indicator_test_data_file_name = \
        './data/test_' + indicator_test_data_file_name + \
        '_time_series_on_sample_data.csv'

    assertRaises = unittest.TestCase.assertRaises
    assertEqual = unittest.TestCase.assertEqual
    assertIn = unittest.TestCase.assertIn
    subTest = unittest.TestCase.subTest


if __name__ == '__main__':
    unittest.main()
