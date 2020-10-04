"""
Trading-Technical-Indicators (tti) python library

File name: test_indicator_stochastic_oscillator.py
    tti.indicators package, _stochastic_oscillator.py module unit tests.
"""

import unittest
import pandas as pd
import matplotlib.pyplot

from tti.indicators import StochasticOscillator
from tti.utils.exceptions import NotEnoughInputData, \
    WrongTypeForInputParameter, WrongValueForInputParameter


class TestFastStochasticOscillator(unittest.TestCase):

    # Validate input_data parameter

    def test_input_data_missing(self):
        with self.assertRaises(TypeError):
            StochasticOscillator()

    def test_input_data_wrong_type(self):
        with self.assertRaises(TypeError):
            StochasticOscillator('NO_DF')

    def test_input_data_wrong_index_type(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=1)

        with self.assertRaises(TypeError):
            StochasticOscillator(df)

    def test_input_data_required_column_close_missing(self):

        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(ValueError):
            StochasticOscillator(pd.DataFrame(df.drop(columns=['close'])))

    def test_input_data_required_column_high_missing(self):
        df = pd.read_csv('./data/sample_data.csv',
                         parse_dates=True, index_col=0)

        with self.assertRaises(ValueError):
            StochasticOscillator(pd.DataFrame(df.drop(columns=['high'])))

    def test_input_data_required_column_low_missing(self):
        df = pd.read_csv('./data/sample_data.csv',
                         parse_dates=True, index_col=0)

        with self.assertRaises(ValueError):
            StochasticOscillator(pd.DataFrame(df.drop(columns=['low'])))

    def test_input_data_empty(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(ValueError):
            StochasticOscillator(pd.DataFrame(df[df.index >= '2032-01-01']))

    def test_input_data_values_wrong_type(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df = df.astype('str')
        df['close'].iat[0] = 'no-numeric'

        with self.assertRaises(ValueError):
            StochasticOscillator(df)

    def test_k_periods_parameter_wrong_type(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(WrongTypeForInputParameter):
            StochasticOscillator(df, k_periods='1', k_slowing_periods=3,
                                 d_periods=3, d_method='simple')

    def test_k_periods_parameter_wrong_value(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(WrongValueForInputParameter):
            StochasticOscillator(df, k_periods=0, k_slowing_periods=3,
                                 d_periods=3, d_method='simple')

    def test_k_slowing_periods_parameter_wrong_type(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(WrongTypeForInputParameter):
            StochasticOscillator(df, k_periods=14, k_slowing_periods='3',
                                 d_periods=3, d_method='simple')

    def test_k_slowing_periods_parameter_wrong_value(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(WrongValueForInputParameter):
            StochasticOscillator(df, k_periods=14, k_slowing_periods=2,
                                 d_periods=3, d_method='simple')

    def test_d_periods_parameter_wrong_type(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(WrongTypeForInputParameter):
            StochasticOscillator(df, k_periods=14, k_slowing_periods=3,
                                 d_periods='3', d_method='simple')

    def test_d_periods_parameter_wrong_value(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(WrongValueForInputParameter):
            StochasticOscillator(df, k_periods=14, k_slowing_periods=3,
                                 d_periods=0, d_method='simple')

    def test_d_method_parameter_wrong_type(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(WrongTypeForInputParameter):
            StochasticOscillator(df, k_periods=14, k_slowing_periods=3,
                                 d_periods=3, d_method=1)

    def test_d_method_parameter_wrong_value(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(WrongValueForInputParameter):
            StochasticOscillator(df, k_periods=14, k_slowing_periods=3,
                                 d_periods=3, d_method='something')

    def test_fill_missing_values_parameter_wrong_type(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(WrongTypeForInputParameter):
            StochasticOscillator(df, k_periods=14, k_slowing_periods=3,
                                 d_periods=3, d_method='simple',
                                 fill_missing_values=1)

    # Validate fill_missing_values input argument

    def test_fill_missing_values_is_true(self):
        df = pd.read_csv('./data/missing_values_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv('./data/missing_values_filled.csv',
                                         parse_dates=True,
                                         index_col=0)[['high', 'low', 'close']]

        df_result = StochasticOscillator(df, fill_missing_values=True)\
            ._input_data

        pd.testing.assert_frame_equal(df_result, df_expected_result)

    def test_fill_missing_values_is_false(self):
        df = pd.read_csv('./data/missing_values_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/missing_values_data_sorted.csv', parse_dates=True,
            index_col=0)[['high', 'low', 'close']]

        df_result = StochasticOscillator(df, fill_missing_values=False)\
            ._input_data

        pd.testing.assert_frame_equal(df_result, df_expected_result)

    def test_fill_missing_values_is_default_true(self):
        df = pd.read_csv('./data/missing_values_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv('./data/missing_values_filled.csv',
                                         parse_dates=True,
                                         index_col=0)[['high', 'low', 'close']]

        df_result = StochasticOscillator(df)._input_data

        pd.testing.assert_frame_equal(df_result, df_expected_result)

    # Validate indicator creation

    def test_validate_indicator_less_than_required_data(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(NotEnoughInputData):
            StochasticOscillator(df.iloc[0:13], k_periods=14,
                                 k_slowing_periods=3,
                                 d_periods=3, d_method='simple',
                                 fill_missing_values=True)

    def test_validate_indicator_fast_full_data(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/test_stochastic_oscillator_fast_on_sample_data.csv',
            parse_dates=True,
            index_col=0)

        df_result = StochasticOscillator(df)._ti_data

        pd.testing.assert_frame_equal(df_expected_result, df_result)

    def test_validate_indicator_slow_full_data(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/test_stochastic_oscillator_slow_on_sample_data.csv',
            parse_dates=True,
            index_col=0)

        df_result = StochasticOscillator(df, k_slowing_periods=3)._ti_data

        pd.testing.assert_frame_equal(df_expected_result, df_result)

    # Validate API

    def test_getTiGraph(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        obv = StochasticOscillator(df)

        # Needs manual check of the produced graph
        self.assertEqual(obv.getTiGraph(), matplotlib.pyplot)

        obv.getTiGraph().savefig('./figures/test_stochastic_oscillator.png')

    def test_getTiData(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/test_stochastic_oscillator_fast_on_sample_data.csv',
            parse_dates=True,
            index_col=0)

        pd.testing.assert_frame_equal(df_expected_result,
                                      StochasticOscillator(df).getTiData())

    def test_getTiValue_specific(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/test_stochastic_oscillator_fast_on_sample_data.csv',
            parse_dates=True,
            index_col=0)

        self.assertEqual(list(df_expected_result.loc['2000-04-25', :]),
                         StochasticOscillator(df).getTiValue('2000-04-25'))

    def test_getTiValue_latest(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/test_stochastic_oscillator_fast_on_sample_data.csv',
            parse_dates=True,
            index_col=0)

        self.assertEqual(list(df_expected_result.iloc[-1]),
                         StochasticOscillator(df).getTiValue())

    def test_getTiSignal(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        self.assertIn(StochasticOscillator(df).getTiSignal(),
                      [('buy', -1), ('hold', 0), ('sell', 1)])


if __name__ == '__main__':
    unittest.main()
