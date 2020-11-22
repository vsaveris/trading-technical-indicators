"""
Trading-Technical-Indicators (tti) python library

File name: test_utils_data_validation.py
    tti.utils package, data_validation.py module unit tests.
"""

import unittest
import pandas as pd

from tti.utils import data_validation as dv
from tti.utils.exceptions import WrongTypeForInputParameter


class TestValidateInputData(unittest.TestCase):

    def test_input_data_parameter_missing(self):
        with self.assertRaises(TypeError):
            dv.validateInputData(required_columns=['C1'], indicator_name='I')

    def test_required_columns_parameter_missing(self):
        df = pd.DataFrame(index=range(10), columns=['A'], data=None,
                          dtype=float)

        with self.assertRaises(TypeError):
            dv.validateInputData(input_data=df, indicator_name='I')

    def test_indicator_name_parameter_missing(self):
        df = pd.DataFrame(index=range(10), columns=['A'], data=None,
                          dtype=float)

        with self.assertRaises(TypeError):
            dv.validateInputData(input_data=df, required_columns=['C1'])

    def test_input_data_is_not_dataframe(self):

        with self.assertRaises(WrongTypeForInputParameter):
            dv.validateInputData(input_data='No_DF', required_columns=['C1'],
                                 indicator_name='I')

    def test_input_data_index_is_not_date(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=1)

        with self.assertRaises(TypeError):
            dv.validateInputData(input_data=df, required_columns=['close'],
                                 indicator_name='I')

    def test_input_data_dataframe_is_empty(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(ValueError):
            dv.validateInputData(input_data=df[df.index >= '2032-01-01'],
                                 required_columns=['close'],
                                 indicator_name='I')

    def test_input_data_no_numeric_columns(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df = df.astype('str')
        df['close'].iat[0] = 'no-numeric'

        with self.assertRaises(ValueError):
            dv.validateInputData(input_data=df, required_columns=['close'],
                                 indicator_name='I')

    def test_input_data_missing_required_columns(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(ValueError):
            dv.validateInputData(input_data=df, required_columns=['not_exist'],
                                 indicator_name='I')

    def test_input_data_not_required_columns_removed(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_result = dv.validateInputData(input_data=df,
                                         required_columns=['close'],
                                         indicator_name='I')

        self.assertListEqual(['close'], list(df_result.columns))

    def test_input_data_already_sorted(self):
        df = pd.read_csv('./data/sample_data_sorted.csv', parse_dates=True,
                         index_col=0)

        pd.testing.assert_frame_equal(
            dv.validateInputData(input_data=df, required_columns=['close'],
                                 indicator_name='I'), df[['close']])

    def test_input_data_not_sorted(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv('./data/sample_data_sorted.csv',
                                         parse_dates=True,
                                         index_col=0)

        df_result = dv.validateInputData(input_data=df,
                                         required_columns=['open', 'high',
                                                           'low', 'close',
                                                           'volume',
                                                           'adj_close'],
                                         indicator_name='I')

        pd.testing.assert_frame_equal(df_result, df_expected_result)

    def test_fill_missing_values_is_true(self):
        df = pd.read_csv('./data/missing_values_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv('./data/missing_values_filled.csv',
                                         parse_dates=True,
                                         index_col=0)

        df_result = dv.validateInputData(input_data=df,
                                         required_columns=['open', 'high',
                                                           'low', 'close',
                                                           'volume',
                                                           'adj_close'],
                                         indicator_name='I',
                                         fill_missing_values=True)

        pd.testing.assert_frame_equal(df_result, df_expected_result)

    def test_fill_missing_values_is_false(self):
        df = pd.read_csv('./data/missing_values_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/missing_values_data_sorted.csv', parse_dates=True,
            index_col=0)

        df_result = dv.validateInputData(input_data=df,
                                         required_columns=['open', 'high',
                                                           'low', 'close',
                                                           'volume',
                                                           'adj_close'],
                                         indicator_name='I',
                                         fill_missing_values=False)

        pd.testing.assert_frame_equal(df_result, df_expected_result)

    def test_fill_missing_values_is_default_true(self):
        df = pd.read_csv('./data/missing_values_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv('./data/missing_values_filled.csv',
                                         parse_dates=True,
                                         index_col=0)

        df_result = dv.validateInputData(input_data=df,
                                         required_columns=['open', 'high',
                                                           'low', 'close',
                                                           'volume',
                                                           'adj_close'],
                                         indicator_name='I')

        pd.testing.assert_frame_equal(df_result, df_expected_result)


if __name__ == '__main__':
    unittest.main()
