"""
Trading-Technical-Indicators (tti) python library

File name: test_indicator_accumulation_distribution_line.py
    tti.indicators package, _accumulation_distribution_line.py module unit 
    tests.
"""

import unittest
import pandas as pd
import matplotlib.pyplot as plt

from tti.indicators import AccumulationDistributionLine
from tti.utils.exceptions import WrongTypeForInputParameter


class TestAccumulationDistributionLine(unittest.TestCase):

    # Validate input_data parameter

    def test_input_data_missing(self):
        with self.assertRaises(TypeError):
            AccumulationDistributionLine()

    def test_input_data_wrong_type(self):
        with self.assertRaises(TypeError):
            AccumulationDistributionLine('NO_DF')

    def test_input_data_wrong_index_type(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=1)

        with self.assertRaises(TypeError):
            AccumulationDistributionLine(df)

    def test_input_data_required_column_close_missing(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(ValueError):
            AccumulationDistributionLine(pd.DataFrame(
                df.drop(columns=['close'])))

    def test_input_data_required_column_high_missing(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(ValueError):
            AccumulationDistributionLine(pd.DataFrame(
                df.drop(columns=['high'])))

    def test_input_data_required_column_low_missing(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(ValueError):
            AccumulationDistributionLine(pd.DataFrame(
                df.drop(columns=['low'])))

    def test_input_data_required_column_volume_missing(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(ValueError):
            AccumulationDistributionLine(pd.DataFrame(
                df.drop(columns=['volume'])))

    def test_input_data_empty(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(ValueError):
            AccumulationDistributionLine(pd.DataFrame(
                df[df.index >= '2032-01-01']))

    def test_input_data_values_wrong_type(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df = df.astype('str')
        df['close'].iat[0] = 'no-numeric'

        with self.assertRaises(ValueError):
            AccumulationDistributionLine(df)

    def test_fill_missing_values_parameter_wrong_type(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(WrongTypeForInputParameter):
            AccumulationDistributionLine(df, fill_missing_values=1)

    # Validate fill_missing_values input argument

    def test_fill_missing_values_is_true(self):
        df = pd.read_csv('./data/missing_values_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/missing_values_filled.csv', parse_dates=True,
            index_col=0)[['high', 'low', 'close', 'volume']]

        df_result = AccumulationDistributionLine(
            df, fill_missing_values=True)._input_data

        pd.testing.assert_frame_equal(df_result, df_expected_result)

    def test_fill_missing_values_is_false(self):
        df = pd.read_csv('./data/missing_values_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/missing_values_data_sorted.csv', parse_dates=True,
            index_col=0)[['high', 'low', 'close', 'volume']]

        df_result = AccumulationDistributionLine(
            df, fill_missing_values=False)._input_data

        pd.testing.assert_frame_equal(df_result, df_expected_result)

    def test_fill_missing_values_is_default_true(self):
        df = pd.read_csv('./data/missing_values_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/missing_values_filled.csv', parse_dates=True,
            index_col=0)[['high', 'low', 'close', 'volume']]

        df_result = AccumulationDistributionLine(df)._input_data

        pd.testing.assert_frame_equal(df_result, df_expected_result)

    # Validate indicator creation

    def test_validate_indicator_one_row(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/test_accumulation_distribution_line_on_sample_data.csv',
            parse_dates=True,
            index_col=0)

        df_result = AccumulationDistributionLine(
            df[df.index == '2000-02-01'])._ti_data

        pd.testing.assert_frame_equal(
            df_expected_result[df_expected_result.index == '2000-02-01'],
            df_result)

    def test_validate_indicator_full_data(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/test_accumulation_distribution_line_on_sample_data.csv',
            parse_dates=True,
            index_col=0)

        df_result = AccumulationDistributionLine(df)._ti_data

        pd.testing.assert_frame_equal(df_expected_result, df_result)

    # Validate API

    def test_getTiGraph(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        obv = AccumulationDistributionLine(df)

        # Needs manual check of the produced graph
        self.assertEqual(obv.getTiGraph(), plt)

        obv.getTiGraph().savefig(
            './figures/test_accumulation_distribution_line.png')
        plt.close('all')

    def test_getTiData(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/test_accumulation_distribution_line_on_sample_data.csv',
            parse_dates=True,
            index_col=0)

        pd.testing.assert_frame_equal(
            df_expected_result,
            AccumulationDistributionLine(df).getTiData())

    def test_getTiValue_specific(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/test_accumulation_distribution_line_on_sample_data.csv',
            parse_dates=True,
            index_col=0)

        self.assertEqual(
            list(df_expected_result.loc['2009-10-19', :]),
            AccumulationDistributionLine(df).getTiValue('2009-10-19'))

    def test_getTiValue_latest(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/test_accumulation_distribution_line_on_sample_data.csv',
            parse_dates=True,
            index_col=0)

        self.assertEqual(list(df_expected_result.iloc[-1]),
                         AccumulationDistributionLine(df).getTiValue())

    def test_getTiSignal(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        self.assertIn(AccumulationDistributionLine(df).getTiSignal(),
                      [('buy', -1), ('hold', 0), ('sell', 1)])


if __name__ == '__main__':
    unittest.main()
