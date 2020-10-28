"""
Trading-Technical-Indicators (tti) python library

File name: test_indicator_forecast_oscillator.py
    tti.indicators package, _forecast_oscillator.py module unit tests.
"""

import unittest
import pandas as pd
import matplotlib.pyplot as plt

from tti.indicators import ForecastOscillator
from tti.utils.exceptions import NotEnoughInputData, \
    WrongTypeForInputParameter, WrongValueForInputParameter


class TestForecastOscillator(unittest.TestCase):

    # Validate input_data parameter

    def test_input_data_missing(self):
        with self.assertRaises(TypeError):
            ForecastOscillator()

    def test_input_data_wrong_type(self):
        with self.assertRaises(TypeError):
            ForecastOscillator('NO_DF')

    def test_input_data_wrong_index_type(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=1)

        with self.assertRaises(TypeError):
            ForecastOscillator(df)

    def test_input_data_required_column_close_missing(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(ValueError):
            ForecastOscillator(pd.DataFrame(df.drop(columns=['close'])))

    def test_input_data_empty(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(ValueError):
            ForecastOscillator(pd.DataFrame(df[df.index >= '2032-01-01']))

    def test_input_data_values_wrong_type(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df = df.astype('str')
        df['close'].iat[0] = 'no-numeric'

        with self.assertRaises(ValueError):
            ForecastOscillator(df)

    def test_period_parameter_wrong_type(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(WrongTypeForInputParameter):
            ForecastOscillator(df, period='30')

    def test_period_parameter_wrong_value(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(WrongValueForInputParameter):
            ForecastOscillator(df, period=0)

    def test_fill_missing_values_parameter_wrong_type(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(WrongTypeForInputParameter):
            ForecastOscillator(df, period=200, fill_missing_values=1)

    # Validate fill_missing_values input argument

    def test_fill_missing_values_is_true(self):
        df = pd.read_csv('./data/missing_values_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv('./data/missing_values_filled.csv',
                                         parse_dates=True,
                                         index_col=0)[['close']]

        df_result = ForecastOscillator(df, fill_missing_values=True)._input_data

        pd.testing.assert_frame_equal(df_result, df_expected_result)

    def test_fill_missing_values_is_false(self):
        df = pd.read_csv('./data/missing_values_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/missing_values_data_sorted.csv', parse_dates=True,
            index_col=0)[['close']]

        df_result = ForecastOscillator(df, fill_missing_values=False)\
            ._input_data

        pd.testing.assert_frame_equal(df_result, df_expected_result)

    def test_fill_missing_values_is_default_true(self):
        df = pd.read_csv('./data/missing_values_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv('./data/missing_values_filled.csv',
                                         parse_dates=True,
                                         index_col=0)[['close']]

        df_result = ForecastOscillator(df)._input_data

        pd.testing.assert_frame_equal(df_result, df_expected_result)

    # Validate indicator creation

    def test_validate_indicator_one_row(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(NotEnoughInputData):
            ForecastOscillator(df[df.index == '2000-02-01'])

    def test_validate_indicator_less_than_required_data(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(NotEnoughInputData):
            ForecastOscillator(df.iloc[:13], period=14)

    def test_validate_indicator_full_data(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/test_forecast_oscillator_on_sample_data.csv',
            parse_dates=True,
            index_col=0).round(4)

        df_result = ForecastOscillator(df)._ti_data

        pd.testing.assert_frame_equal(df_expected_result, df_result)

    # Validate API

    def test_getTiGraph(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        obv = ForecastOscillator(df)

        # Needs manual check of the produced graph
        self.assertEqual(obv.getTiGraph(), plt)

        obv.getTiGraph().savefig('./figures/test_forecast_oscillator.png')
        plt.close('all')

    def test_getTiData(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/test_forecast_oscillator_on_sample_data.csv',
            parse_dates=True,
            index_col=0)

        pd.testing.assert_frame_equal(df_expected_result.round(4),
                                      ForecastOscillator(df)
                                      .getTiData())

    def test_getTiValue_specific(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/test_forecast_oscillator_on_sample_data.csv',
            parse_dates=True,
            index_col=0).round(4)

        self.assertEqual(list(df_expected_result.loc['2009-10-19', :]),
                         ForecastOscillator(df).
                         getTiValue('2009-10-19'))

    def test_getTiValue_latest(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/test_forecast_oscillator_on_sample_data.csv',
            parse_dates=True,
            index_col=0).round(4)

        self.assertEqual(list(df_expected_result.iloc[-1]),
                         ForecastOscillator(df).getTiValue())

    def test_getTiSignal(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        self.assertIn(ForecastOscillator(df).getTiSignal(),
                      [('buy', -1), ('hold', 0), ('sell', 1)])


if __name__ == '__main__':
    unittest.main()
