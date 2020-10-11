"""
Trading-Technical-Indicators (tti) python library

File name: test_indicator_ichimoku_cloud.py
    tti.indicators package, _ichimoku_cloud.py module unit tests.
"""

import unittest
import pandas as pd
import matplotlib.pyplot

from tti.indicators import IchimokuCloud
from tti.utils.exceptions import NotEnoughInputData, \
    WrongTypeForInputParameter, WrongValueForInputParameter


class TestIchimokuCloud(unittest.TestCase):

    # Validate input_data parameter

    def test_input_data_missing(self):
        with self.assertRaises(TypeError):
            IchimokuCloud()

    def test_input_data_wrong_type(self):
        with self.assertRaises(TypeError):
            IchimokuCloud('NO_DF')

    def test_input_data_wrong_index_type(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=1)

        with self.assertRaises(TypeError):
            IchimokuCloud(df)

    def test_input_data_required_column_close_missing(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(ValueError):
            IchimokuCloud(pd.DataFrame(df.drop(columns=['close'])))

    def test_input_data_required_high_close_missing(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(ValueError):
            IchimokuCloud(pd.DataFrame(df.drop(columns=['high'])))

    def test_input_data_required_column_low_missing(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(ValueError):
            IchimokuCloud(pd.DataFrame(df.drop(columns=['low'])))

    def test_input_data_empty(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(ValueError):
            IchimokuCloud(pd.DataFrame(df[df.index >= '2032-01-01']))

    def test_input_data_values_wrong_type(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df = df.astype('str')
        df['close'].iat[0] = 'no-numeric'

        with self.assertRaises(ValueError):
            IchimokuCloud(df)

    def test_fill_missing_values_parameter_wrong_type(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(WrongTypeForInputParameter):
            IchimokuCloud(df, fill_missing_values=1)

    # Validate fill_missing_values input argument

    def test_fill_missing_values_is_true(self):
        df = pd.read_csv('./data/missing_values_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv('./data/missing_values_filled.csv',
                                         parse_dates=True,
                                         index_col=0)[['high', 'low', 'close']]

        df_result = IchimokuCloud(df, fill_missing_values=True)._input_data

        pd.testing.assert_frame_equal(df_result, df_expected_result)

    def test_fill_missing_values_is_false(self):
        df = pd.read_csv('./data/missing_values_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/missing_values_data_sorted.csv', parse_dates=True,
            index_col=0)[['high', 'low', 'close']]

        df_result = IchimokuCloud(df, fill_missing_values=False)._input_data

        pd.testing.assert_frame_equal(df_result, df_expected_result)

    def test_fill_missing_values_is_default_true(self):
        df = pd.read_csv('./data/missing_values_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv('./data/missing_values_filled.csv',
                                         parse_dates=True,
                                         index_col=0)[['high', 'low', 'close']]

        df_result = IchimokuCloud(df)._input_data

        pd.testing.assert_frame_equal(df_result, df_expected_result)

    # Validate indicator creation

    def test_validate_indicator_full_data(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/test_ichimoku_cloud_on_sample_data.csv',
            parse_dates=True,
            index_col=0)

        df_result = IchimokuCloud(df)._ti_data

        pd.testing.assert_frame_equal(df_expected_result, df_result)

    # Validate API

    def test_getTiGraph(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        obv = IchimokuCloud(df)

        # Needs manual check of the produced graph
        self.assertEqual(obv.getTiGraph(), matplotlib.pyplot)

        obv.getTiGraph().savefig('./figures/test_moving_average.png')

    def test_getTiData(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/test_ichimoku_cloud_on_sample_data.csv',
            parse_dates=True,
            index_col=0)

        pd.testing.assert_frame_equal(df_expected_result.round(4),
                                      IchimokuCloud(df)
                                      .getTiData())

    def test_getTiValue_specific(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/test_ichimoku_cloud_on_sample_data.csv',
            parse_dates=True,
            index_col=0)

        self.assertEqual(list(df_expected_result.loc['2009-10-19', :]),
                         IchimokuCloud(df).
                         getTiValue('2009-10-19'))

    def test_getTiValue_latest(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/test_ichimoku_cloud_on_sample_data.csv',
            parse_dates=True,  index_col=0).round(4)

        self.assertEqual(list(df_expected_result.iloc[-1]),
                         IchimokuCloud(df).getTiValue())

    def test_getTiSignal(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        self.assertIn(IchimokuCloud(df).getTiSignal(),
                      [('buy', -1), ('hold', 0), ('sell', 1)])


if __name__ == '__main__':
    unittest.main()
