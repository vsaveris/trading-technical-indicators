"""
Trading-Technical-Indicators (tti) python library

File name: test_indicator_simple_moving_average.py
    tti.indicators package, _simple_moving_average.py module unit tests.
"""

import unittest
import pandas as pd
import matplotlib.pyplot

from tti.indicators import SimpleMovingAverage


class TestSimpleMovingAverage(unittest.TestCase):

    # Validate input_data parameter

    def test_input_data_missing(self):
        with self.assertRaises(TypeError):
            SimpleMovingAverage()

    def test_input_data_wrong_type(self):
        with self.assertRaises(TypeError):
            SimpleMovingAverage('NO_DF')

    def test_input_data_wrong_index_type(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=1)

        with self.assertRaises(TypeError):
            SimpleMovingAverage(df)

    def test_input_data_required_column_close_missing(self):

        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(ValueError):
            SimpleMovingAverage(pd.DataFrame(df.drop(columns=['close'])))

    def test_input_data_required_column_volume_missing(self):
        df = pd.read_csv('./data/sample_data.csv',
                         parse_dates=True, index_col=0)

        with self.assertRaises(ValueError):
            SimpleMovingAverage(pd.DataFrame(df.drop(columns=['volume'])))

    def test_input_data_empty(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(ValueError):
            SimpleMovingAverage(pd.DataFrame(df[df.index >= '2032-01-01']))

    def test_input_data_values_wrong_type(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df = df.astype('str')
        df['close'].iat[0] = 'no-numeric'

        with self.assertRaises(ValueError):
            SimpleMovingAverage(df)

    # Validate fill_missing_values input argument

    def test_fill_missing_values_is_true(self):
        df = pd.read_csv('./data/missing_values_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv('./data/missing_values_filled.csv',
                                         parse_dates=True,
                                         index_col=0)[['close', 'volume']]

        df_result = SimpleMovingAverage(df, fill_missing_values=True)\
            ._input_data

        pd.testing.assert_frame_equal(df_result, df_expected_result)

    def test_fill_missing_values_is_false(self):
        df = pd.read_csv('./data/missing_values_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/missing_values_data_sorted.csv', parse_dates=True,
            index_col=0)[['close', 'volume']]

        df_result = SimpleMovingAverage(df, fill_missing_values=False)\
            ._input_data

        pd.testing.assert_frame_equal(df_result, df_expected_result)

    def test_fill_missing_values_is_default_true(self):
        df = pd.read_csv('./data/missing_values_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv('./data/missing_values_filled.csv',
                                         parse_dates=True,
                                         index_col=0)[['close', 'volume']]

        df_result = SimpleMovingAverage(df)._input_data

        pd.testing.assert_frame_equal(df_result, df_expected_result)

    # Validate indicator creation

    def test_validate_indicator_one_row(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/test_on_balance_volume_on_sample_data.csv',
            parse_dates=True,
            index_col=0)

        df_result = SimpleMovingAverage(df[df.index == '2000-02-01'])._ti_data

        pd.testing.assert_frame_equal(df_expected_result[df_expected_result.
                                      index == '2000-02-01'], df_result)

    def test_validate_indicator_full_data(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/test_on_balance_volume_on_sample_data.csv',
            parse_dates=True,
            index_col=0)

        df_result = SimpleMovingAverage(df)._ti_data

        pd.testing.assert_frame_equal(df_expected_result, df_result)

    # Validate API

    def test_getTiGraph(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        obv = SimpleMovingAverage(df)

        # Needs manual check of the produced graph
        self.assertEqual(obv.getTiGraph(), matplotlib.pyplot)

        obv.getTiGraph().savefig('./figures/test_on_balance_volume.png')

    def test_getTiData(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/test_on_balance_volume_on_sample_data.csv',
            parse_dates=True,
            index_col=0)

        pd.testing.assert_frame_equal(df_expected_result,
                                      SimpleMovingAverage(df).getTiData())

    def test_getTiValue_specific(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/test_on_balance_volume_on_sample_data.csv',
            parse_dates=True,
            index_col=0)

        self.assertEqual(df_expected_result.loc['2000-04-25', 'OBV'],
                         SimpleMovingAverage(df).getTiValue('2000-04-25'))

    def test_getTiValue_latest(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/test_on_balance_volume_on_sample_data.csv',
            parse_dates=True,
            index_col=0)

        self.assertEqual(df_expected_result.iloc[-1, 0],
                         SimpleMovingAverage(df).getTiValue())

    def test_getTiSignal(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        self.assertIn(SimpleMovingAverage(df).getTiSignal(),
                      [('buy', -1), ('hold', 0), ('sell', 1)])


if __name__ == '__main__':
    unittest.main()
