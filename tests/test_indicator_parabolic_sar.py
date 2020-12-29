"""
Trading-Technical-Indicators (tti) python library

File name: test_indicator_parabolic_sar.py
    tti.indicators package, _parabolic_sar.py module unit tests.
"""

import unittest
import tti.indicators
from test_indicators_common import TestIndicatorsCommon

import pandas as pd
import re


class TestParabolicSAR(unittest.TestCase, TestIndicatorsCommon):

    indicator = tti.indicators.ParabolicSAR

    ti_data_rows = [0, 1, 2]

    df = pd.read_csv('./data/sample_data.csv', parse_dates=True, index_col=0)

    indicator_input_arguments = {}

    indicator_other_input_arguments = []

    indicator_minimum_required_data = 2

    mandatory_arguments_missing_cases = []

    required_input_data_columns = ["high", "low", "close"]

    arguments_wrong_type = [
        {'input_data': 'No_DataFrame'},
        {'input_data': df, 'fill_missing_values': 'no_boolean'}
    ]

    arguments_wrong_value = []

    graph_file_name = './figures/test_parabolic_sar.png'

    indicator_test_data_file_name = \
        './data/test_parabolic_sar_on_sample_data.csv'

    assertRaises = unittest.TestCase.assertRaises
    assertEqual = unittest.TestCase.assertEqual
    assertIn = unittest.TestCase.assertIn
    subTest = unittest.TestCase.subTest


if __name__ == '__main__':
    unittest.main()
