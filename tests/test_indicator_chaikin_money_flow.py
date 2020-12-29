"""
Trading-Technical-Indicators (tti) python library

File name: test_indicator_chaikin_money_flow.py
    tti.indicators package, _chaikin_money_flow.py> module unit tests.
"""

import unittest
import tti.indicators
from test_indicators_common import TestIndicatorsCommon

import pandas as pd
import re


class TestChaikinMoneyFlow(unittest.TestCase, TestIndicatorsCommon):

    indicator = tti.indicators.ChaikinMoneyFlow

    ti_data_rows = [0, 2, 3]

    df = pd.read_csv('./data/sample_data.csv', parse_dates=True, index_col=0)

    indicator_input_arguments = {'period': 5}

    indicator_other_input_arguments = [{'period': 1}, {'period': 3169}]

    indicator_minimum_required_data = indicator_input_arguments['period']

    mandatory_arguments_missing_cases = []

    required_input_data_columns = ["high", "low", "close", "volume"]

    arguments_wrong_type = [
        {'input_data': 'No_DataFrame'},
        {'input_data': df, 'period': 'no_numeric'},
        {'input_data': df, 'fill_missing_values': 'no_boolean'}
    ]

    arguments_wrong_value = [
        {'input_data': df, 'period': -1},
        {'input_data': df, 'period': 0}
    ]

    graph_file_name = '_'.join(
        x.lower() for x in re.findall('[A-Z][^A-Z]*', str(
            indicator).split('.')[-1][:-2]))

    graph_file_name = './figures/test_' + graph_file_name + '.png'

    indicator_test_data_file_name = '_'.join(
        x.lower() for x in re.findall('[A-Z][^A-Z]*', str(
            indicator).split('.')[-1][:-2]))

    indicator_test_data_file_name = \
        './data/test_' + indicator_test_data_file_name + '_on_sample_data.csv'

    assertRaises = unittest.TestCase.assertRaises
    assertEqual = unittest.TestCase.assertEqual
    assertIn = unittest.TestCase.assertIn
    subTest = unittest.TestCase.subTest


if __name__ == '__main__':
    unittest.main()
