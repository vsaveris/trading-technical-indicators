"""
Trading-Technical-Indicators (tti) python library

File name: test_indicator_stochastic_oscillator_fast.py
    tti.indicators package, _stochastic_oscillator.py module unit tests.
    Slow Stochastic Oscillator
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

    indicator_input_arguments = {'k_periods': 14, 'k_slowing_periods': 3,
                                 'd_periods': 3, 'd_method': 'simple'}

    indicator_other_input_arguments = [{'k_periods': 1}, {'k_periods': 3169}]

    indicator_minimum_required_data = indicator_input_arguments['k_periods']

    mandatory_arguments_missing_cases = []

    required_input_data_columns = ["high", "low", "close"]

    # Tested already with the Fast Stochastic Oscillator
    arguments_wrong_type = []

    # Tested already with the Fast Stochastic Oscillator
    arguments_wrong_value = []

    graph_file_name = '_'.join(
        x.lower() for x in re.findall('[A-Z][^A-Z]*', str(
            indicator).split('.')[-1][:-2]))

    graph_file_name = './figures/test_' + graph_file_name + '_slow.png'

    indicator_test_data_file_name = '_'.join(
        x.lower() for x in re.findall('[A-Z][^A-Z]*', str(
            indicator).split('.')[-1][:-2]))

    indicator_test_data_file_name = \
        './data/test_' + indicator_test_data_file_name + \
        '_slow_on_sample_data.csv'

    assertRaises = unittest.TestCase.assertRaises
    assertEqual = unittest.TestCase.assertEqual
    assertIn = unittest.TestCase.assertIn
    subTest = unittest.TestCase.subTest


if __name__ == '__main__':
    unittest.main()
