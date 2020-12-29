"""
Trading-Technical-Indicators (tti) python library

File name: test_indicator_stochastic_oscillator_fast.py
    tti.indicators package, _stochastic_oscillator.py module unit tests.

    Fast Stochastic Oscillator
"""

import unittest
import tti.indicators
from test_indicators_common import TestIndicatorsCommon

import pandas as pd
import re


class TestStochasticOscillator(unittest.TestCase, TestIndicatorsCommon):

    indicator = tti.indicators.StochasticOscillator

    ti_data_rows = [0, 1, 2]

    df = pd.read_csv('./data/sample_data.csv', parse_dates=True, index_col=0)

    indicator_input_arguments = {'k_periods': 14, 'k_slowing_periods': 1,
                                 'd_periods': 3, 'd_method': 'simple'}

    indicator_other_input_arguments = [{'k_periods': 1}, {'k_periods': 3169}]

    indicator_minimum_required_data = indicator_input_arguments['k_periods']

    mandatory_arguments_missing_cases = []

    required_input_data_columns = ["high", "low", "close"]

    arguments_wrong_type = [
        {'input_data': 'No_DataFrame'},
        {'input_data': df, 'k_periods': 'no_numeric'},
        {'input_data': df, 'k_slowing_periods': 'no_numeric'},
        {'input_data': df, 'd_periods': 'no_numeric'},
        {'input_data': df, 'd_method': 1},
        {'input_data': df, 'fill_missing_values': 'no_boolean'}
    ]

    arguments_wrong_value = [
        {'input_data': df, 'k_periods': -1},
        {'input_data': df, 'k_periods': 0},
        {'input_data': df, 'k_slowing_periods': 2},
        {'input_data': df, 'k_slowing_periods': 4},
        {'input_data': df, 'k_slowing_periods': 0},
        {'input_data': df, 'd_periods': -1},
        {'input_data': df, 'd_periods': 0},
        {'input_data': df, 'd_method': 'not_valid'}
    ]

    graph_file_name = '_'.join(
        x.lower() for x in re.findall('[A-Z][^A-Z]*', str(
            indicator).split('.')[-1][:-2]))

    graph_file_name = './figures/test_' + graph_file_name + '_fast.png'

    indicator_test_data_file_name = '_'.join(
        x.lower() for x in re.findall('[A-Z][^A-Z]*', str(
            indicator).split('.')[-1][:-2]))

    indicator_test_data_file_name = \
        './data/test_' + indicator_test_data_file_name + \
        '_fast_on_sample_data.csv'

    assertRaises = unittest.TestCase.assertRaises
    assertEqual = unittest.TestCase.assertEqual
    assertIn = unittest.TestCase.assertIn
    subTest = unittest.TestCase.subTest


if __name__ == '__main__':
    unittest.main()
