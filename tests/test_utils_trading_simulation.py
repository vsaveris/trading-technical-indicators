"""
Trading-Technical-Indicators (tti) python library

File name: test_utils_trading_simulation.py
    tti.utils package, trading_simulation.py module unit tests.
"""

import unittest
import pandas as pd

from tti.utils.trading_simulation import TradingSimulation
from tti.utils.exceptions import WrongTypeForInputParameter, \
    NotValidInputDataForSimulation, WrongValueForInputParameter
from tti.utils.constants import TRADE_SIGNALS

class TestTradingSimulation(unittest.TestCase):

    # Missing input argument test cases

    def test_input_data_index_missing(self):

        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)[['close']]

        with self.assertRaises(TypeError):
            TradingSimulation(close_values=cv_df,
                              max_items_per_transaction=1,
                              max_investment=None)

    def test_close_values_missing(self):

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(TypeError):
            TradingSimulation(input_data_index=id_df.index,
                              max_items_per_transaction=1,
                              max_investment=None)

    def test_max_items_per_transaction_missing(self):

        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_investment=None)

        self.assertEqual(ts._max_items_per_transaction, 1)

    def test_max_investment_missing(self):

        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1)

        self.assertEqual(ts._max_investment, None)

    # Wrong type for input arguments test cases

    def test_input_data_index_wrong_type(self):

        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=1)

        with self.assertRaises(NotValidInputDataForSimulation):
            TradingSimulation(input_data_index=id_df,
                              close_values=cv_df,
                              max_items_per_transaction=1,
                              max_investment=None)

    def test_close_values_index_wrong_type(self):

        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=1)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(NotValidInputDataForSimulation):
            TradingSimulation(input_data_index=id_df,
                              close_values=cv_df,
                              max_items_per_transaction=1,
                              max_investment=None)

    def test_close_values_wrong_type(self):
        # close values DataFrame
        cv_df = 'No-DF'

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(NotValidInputDataForSimulation):
            TradingSimulation(input_data_index=id_df.index,
                              close_values=cv_df,
                              max_items_per_transaction=1,
                              max_investment=None)

    def test_max_items_per_transaction_wrong_type(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(WrongTypeForInputParameter):
            TradingSimulation(input_data_index=id_df.index,
                              close_values=cv_df,
                              max_items_per_transaction='1',
                              max_investment=None)

    def test_max_investment_wrong_type(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(WrongTypeForInputParameter):
            TradingSimulation(input_data_index=id_df.index,
                              close_values=cv_df,
                              max_items_per_transaction=1,
                              max_investment='10000.0')

    # Wrong value for input arguments test cases

    def test_close_values_missing_column(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0).drop(columns=['close'], axis=1)

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(NotValidInputDataForSimulation):
            TradingSimulation(input_data_index=id_df.index,
                              close_values=cv_df,
                              max_items_per_transaction=1,
                              max_investment=None)

    def test_close_values_wrong_index(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=False,
                            index_col=0)

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=1)

        with self.assertRaises(NotValidInputDataForSimulation):
            TradingSimulation(input_data_index=id_df.index,
                              close_values=cv_df,
                              max_items_per_transaction=1,
                              max_investment=None)

    def test_close_values_missing_index_values(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(NotValidInputDataForSimulation):
            TradingSimulation(input_data_index=id_df.index,
                              close_values=cv_df.iloc[1:],
                              max_items_per_transaction=1,
                              max_investment=None)

    def test_max_items_per_transaction_zero(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(WrongValueForInputParameter):
            TradingSimulation(input_data_index=id_df.index,
                              close_values=cv_df,
                              max_items_per_transaction=0,
                              max_investment=None)

    def test_max_items_per_transaction_negative(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(WrongValueForInputParameter):
            TradingSimulation(input_data_index=id_df.index,
                              close_values=cv_df,
                              max_items_per_transaction=-1,
                              max_investment=None)

    def test_max_investment_zero(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(WrongValueForInputParameter):
            TradingSimulation(input_data_index=id_df.index,
                              close_values=cv_df,
                              max_items_per_transaction=1,
                              max_investment=0)

    def test_max_investment_negative(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(WrongValueForInputParameter):
            TradingSimulation(input_data_index=id_df.index,
                              close_values=cv_df,
                              max_items_per_transaction=1,
                              max_investment=-100000)

    # Other than default values in input arguments test cases

    def test_max_items_per_transaction_no_default(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1000,
                               max_investment=None)

        self.assertEqual(ts._max_items_per_transaction, 1000)

    def test_max_investment_no_default(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=10000)

        self.assertEqual(ts._max_investment, 10000)

    # Test _calculateSimulationStatistics

    def test_calculate_simulation_statistics_no_simulation_data(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        statistics_expected_result = {
            'number_of_trading_days': 0,
            'number_of_buy_signals': 0,
            'number_of_ignored_buy_signals': 0,
            'number_of_sell_signals': 0,
            'number_of_ignored_sell_signals': 0,
            'balance': 0.0,
            'total_stocks_in_long': 0,
            'total_stocks_in_short': 0,
            'stock_value': 0.0,
            'total_value': 0.0}

        simulation_data_expected_result = pd.DataFrame(
            index=id_df.index,
            columns=['signal',
                     'open_trading_action',
                     'stocks_in_open_transaction',
                     'close_long_trading_actions',
                     'stocks_in_close_long_transactions',
                     'close_short_trading_actions',
                     'stocks_in_close_short_transactions',
                     'balance',
                     'stock_value',
                     'total_value'],
            data=None).sort_index(ascending=True)

        ts._calculateSimulationStatistics()

        pd.testing.assert_frame_equal(ts._simulation_data,
                                      simulation_data_expected_result)

        self.assertDictEqual(ts._statistics, statistics_expected_result)

    def test_calculate_simulation_statistics_no_trading_actions(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        statistics_expected_result = {
            'number_of_trading_days': 22,
            'number_of_buy_signals': 9,
            'number_of_ignored_buy_signals': 9,
            'number_of_sell_signals': 8,
            'number_of_ignored_sell_signals': 8,
            'balance': 0.0,
            'total_stocks_in_long': 0,
            'total_stocks_in_short': 0,
            'stock_value': 19.09,
            'total_value': 0.0}

        simulation_data_expected_result = pd.read_csv(
            './data/simulation_data_full_without_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_without_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._calculateSimulationStatistics()

        pd.testing.assert_frame_equal(ts._simulation_data,
                                      simulation_data_expected_result)

        self.assertDictEqual(ts._statistics, statistics_expected_result)

    def test_calculate_simulation_statistics_with_trading_actions(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        statistics_expected_result = {
            'number_of_trading_days': 23,
            'number_of_buy_signals': 9,
            'number_of_ignored_buy_signals': 4,
            'number_of_sell_signals': 10,
            'number_of_ignored_sell_signals': 5,
            'balance': 31.0,
            'total_stocks_in_long': 4,
            'total_stocks_in_short': 6,
            'stock_value': 19.45,
            'total_value': 122.0}

        simulation_data_expected_result = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full.csv',
            parse_dates=True,
            index_col=0)

        ts._calculateSimulationStatistics()

        pd.testing.assert_frame_equal(ts._simulation_data,
                                      simulation_data_expected_result)

        self.assertDictEqual(ts._statistics, statistics_expected_result)

    # Test _closeOpenPositions

    def test_close_open_positions_invalid_price(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full_close_none.csv',
            parse_dates=True,
            index_col=0)

        with self.assertRaises(WrongValueForInputParameter):
            value, cli, csi = ts._closeOpenPositions(
                price=0.0, force_all=False, write=True)

    def test_close_open_positions_none(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full_close_none.csv',
            parse_dates=True,
            index_col=0)

        value, cli, csi = ts._closeOpenPositions(
            price=20.0, force_all=False, write=True)

        portfolio_expected_results = pd.read_csv(
            './data/portfolio_simulation_data_full_close_none.csv',
            parse_dates=True,
            index_col=0)

        pd.testing.assert_frame_equal(ts._portfolio,
                                      portfolio_expected_results)

        self.assertEqual(value, cli * 20.0 - csi * 20.0)

        self.assertEqual(cli, 0)

        self.assertEqual(csi, 0)

    def test_close_open_positions_only_long(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full_close_long.csv',
            parse_dates=True,
            index_col=0)

        value, cli, csi = ts._closeOpenPositions(
            price=40.0, force_all=False, write=True)

        portfolio_expected_results = pd.read_csv(
            './data/portfolio_simulation_data_full_close_long.csv',
            parse_dates=True,
            index_col=0)

        portfolio_expected_results['status'].iat[0] = 'close'

        pd.testing.assert_frame_equal(ts._portfolio,
                                      portfolio_expected_results)

        self.assertEqual(value, cli * 40.0 - csi * 40.0)

        self.assertEqual(cli, 1)

        self.assertEqual(csi, 0)

    def test_close_open_positions_only_short(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full_close_short.csv',
            parse_dates=True,
            index_col=0)

        value, cli, csi = ts._closeOpenPositions(
            price=25.0, force_all=False, write=True)

        portfolio_expected_results = pd.read_csv(
            './data/portfolio_simulation_data_full_close_short.csv',
            parse_dates=True,
            index_col=0)

        portfolio_expected_results['status'].iat[3] = 'close'

        pd.testing.assert_frame_equal(ts._portfolio,
                                      portfolio_expected_results)

        self.assertEqual(value, cli * 25.0 - csi * 25.0)

        self.assertEqual(cli, 0)

        self.assertEqual(csi, 4)

    def test_close_open_positions_both_long_and_short(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full_close_both.csv',
            parse_dates=True,
            index_col=0)

        value, cli, csi = ts._closeOpenPositions(
            price=22.0, force_all=False, write=True)

        portfolio_expected_results = pd.read_csv(
            './data/portfolio_simulation_data_full_close_both.csv',
            parse_dates=True,
            index_col=0)

        portfolio_expected_results['status'].iat[0] = 'close'
        portfolio_expected_results['status'].iat[3] = 'close'

        pd.testing.assert_frame_equal(ts._portfolio,
                                      portfolio_expected_results)

        self.assertEqual(value, 1 * 22.0 - 4 * 22.0)

        self.assertEqual(cli, 1)

        self.assertEqual(csi, 4)

    def test_close_open_positions_force_all_no_write(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full.csv',
            parse_dates=True,
            index_col=0)

        value, cli, csi = ts._closeOpenPositions(price=10, force_all=True,
                                                 write=False)

        portfolio_expected_results = pd.read_csv(
            './data/portfolio_simulation_data_full.csv',
            parse_dates=True,
            index_col=0)

        pd.testing.assert_frame_equal(ts._portfolio,
                                      portfolio_expected_results)

        self.assertEqual(value, 4 * 10.0 - 6 * 10.0)

        self.assertEqual(cli, 0)

        self.assertEqual(csi, 0)

    def test_close_open_positions_force_False_no_write(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full_close_both.csv',
            parse_dates=True,
            index_col=0)

        value, cli, csi = ts._closeOpenPositions(price=22.0, force_all=False,
                                       write=False)

        portfolio_expected_results = pd.read_csv(
            './data/portfolio_simulation_data_full_close_both.csv',
            parse_dates=True,
            index_col=0)

        pd.testing.assert_frame_equal(ts._portfolio,
                                      portfolio_expected_results)

        self.assertEqual(value, 1 * 22.0 - 4 * 22.0)

        self.assertEqual(cli, 0)

        self.assertEqual(csi, 0)

    def test_close_open_positions_force_all_write(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full.csv',
            parse_dates=True,
            index_col=0)

        value, cli, csi = ts._closeOpenPositions(price=10, force_all=True,
                                                 write=True)

        portfolio_expected_results = pd.read_csv(
            './data/portfolio_simulation_data_full.csv',
            parse_dates=True,
            index_col=0)

        portfolio_expected_results['status'].iat[0] = 'close'
        portfolio_expected_results['status'].iat[1] = 'close'
        portfolio_expected_results['status'].iat[2] = 'close'
        portfolio_expected_results['status'].iat[3] = 'close'

        pd.testing.assert_frame_equal(ts._portfolio,
                                      portfolio_expected_results)

        self.assertEqual(value, 4 * 10.0 - 6 * 10.0)

        self.assertEqual(cli, 4)

        self.assertEqual(csi, 6)

    def test_close_open_positions_price_force_true(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full.csv',
            parse_dates=True,
            index_col=0)

        value, cli, csi = ts._closeOpenPositions(
            price=10000, force_all=True, write=True)

        portfolio_expected_results = pd.read_csv(
            './data/portfolio_simulation_data_full.csv',
            parse_dates=True,
            index_col=0)

        portfolio_expected_results['status'].iat[0] = 'close'
        portfolio_expected_results['status'].iat[1] = 'close'
        portfolio_expected_results['status'].iat[2] = 'close'
        portfolio_expected_results['status'].iat[3] = 'close'

        pd.testing.assert_frame_equal(ts._portfolio,
                                      portfolio_expected_results)

        self.assertEqual(value, cli * 10000 - csi * 10000)

        self.assertEqual(cli, 4)

        self.assertEqual(csi, 6)

    # Test _processHoldSignal

    def test_process_hold_signal_positions_closed(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full_close_both.csv',
            parse_dates=True,
            index_col=0)

        ts._close_values['close'].iat[23] = 22.0

        ts._processHoldSignal(i_index=23)

        value = ts._closeOpenPositions(
            price=22, force_all=True, write=False)[0]

        self.assertListEqual(ts._portfolio.iloc[23, :].to_list(),
                             ['none', 0, 0.0, 'none'])

        self.assertListEqual(ts._simulation_data.iloc[23, :].to_list(), [
            'hold', 'none', 0, False, 0, False, 0,
            ts._simulation_data['balance'].iat[22],
            ts._close_values['close'].iat[23],
            ts._simulation_data['balance'].iat[22] + value])

    def test_process_hold_signal_no_positions_closed(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full_close_none.csv',
            parse_dates=True,
            index_col=0)

        ts._close_values['close'].iat[23] = 20.0

        ts._processHoldSignal(i_index=23)

        value = ts._closeOpenPositions(
            price=20, force_all=True, write=False)[0]

        self.assertListEqual(ts._portfolio.iloc[23, :].to_list(),
                             ['none', 0, 0.0, 'none'])

        self.assertListEqual(ts._simulation_data.iloc[23, :].to_list(), [
            'hold', 'none', 0, False, 0, False, 0,
            ts._simulation_data['balance'].iat[22],
            ts._close_values['close'].iat[23],
            ts._simulation_data['balance'].iat[22] + value])

    # Test _processBuySignal

    def test_process_buy_signal_not_enough_balance(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=0.1)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full_close_both.csv',
            parse_dates=True,
            index_col=0)

        ts._simulation_data['balance'].iat[22] = 1

        ts._processBuySignal(i_index=23)

        value = ts._closeOpenPositions(
            price=34.5, force_all=True, write=False)[0]

        self.assertListEqual(ts._portfolio.iloc[23, :].to_list(),
                             ['none', 0, 0.0, 'none'])

        self.assertListEqual(ts._simulation_data.iloc[23, :].to_list(), [
            'buy', 'none', 0, False, 0, False, 0,
            ts._simulation_data['balance'].iat[22],
            ts._close_values['close'].iat[23],
            ts._simulation_data['balance'].iat[22] + value])

    def test_process_buy_signal_position_open_positions_closed(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=100000)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full_close_both.csv',
            parse_dates=True,
            index_col=0)

        ts._close_values['close'].iat[23] = 22.0

        ts._processBuySignal(i_index=23)

        value = ts._closeOpenPositions(
            price=22, force_all=True, write=False)[0]

        self.assertListEqual(ts._portfolio.iloc[23, :].to_list(),
                             ['long', 1, ts._close_values['close'].iat[23],
                              'open'])

        self.assertListEqual(ts._simulation_data.iloc[23, :].to_list(), [
            'buy', 'long', 1, False, 0, False, 0,
            ts._simulation_data['balance'].iat[22] -
            ts._close_values['close'].iat[23],
            ts._close_values['close'].iat[23],
            ts._simulation_data['balance'].iat[22] -
            ts._close_values['close'].iat[23] + value])

    def test_process_buy_signal_less_items_than_max(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=10000000,
                               max_investment=100000)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full_close_both.csv',
            parse_dates=True,
            index_col=0)

        ts._processBuySignal(i_index=23)

        value = ts._closeOpenPositions(
            price=ts._close_values['close'].iat[23], force_all=True,
            write=False)[0]

        self.assertListEqual(ts._portfolio.iloc[23, :].to_list(),
                             ['long', 2899, ts._close_values['close'].iat[23],
                              'open'])

        self.assertListEqual(ts._simulation_data.iloc[23, :].to_list(), [
            'buy', 'long', 2899, False, 0, False, 0,
            ts._simulation_data['balance'].iat[22] -
            2899 * ts._close_values['close'].iat[23],
            ts._close_values['close'].iat[23],
            ts._simulation_data['balance'].iat[22] -
            2899 * ts._close_values['close'].iat[23] + value])

    def test_process_buy_signal_no_position_open_positions_closed(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full_close_both.csv',
            parse_dates=True,
            index_col=0)

        ts._close_values['close'].iat[23] = 22.0

        ts._processBuySignal(i_index=23)

        value = ts._closeOpenPositions(
            price=22, force_all=True, write=False)[0]

        self.assertListEqual(ts._portfolio.iloc[23, :].to_list(),
                             ['long', 1, ts._close_values['close'].iat[23],
                              'open'])

        self.assertListEqual(ts._simulation_data.iloc[23, :].to_list(), [
            'buy', 'long', 1, False, 0, False, 0,
            ts._simulation_data['balance'].iat[22] -
            ts._close_values['close'].iat[23],
            ts._close_values['close'].iat[23],
            ts._simulation_data['balance'].iat[22] -
            ts._close_values['close'].iat[23] + value])

    def test_process_buy_signal_position_open_no_positions_closed(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full_close_none.csv',
            parse_dates=True,
            index_col=0)

        ts._close_values['close'].iat[23] = 20.0

        ts._processBuySignal(i_index=23)

        value = ts._closeOpenPositions(
            price=20, force_all=True, write=False)[0]

        self.assertListEqual(ts._portfolio.iloc[23, :].to_list(),
                             ['long', 1, ts._close_values['close'].iat[23],
                              'open'])

        self.assertListEqual(ts._simulation_data.iloc[23, :].to_list(), [
            'buy', 'long', 1, False, 0, False, 0,
            ts._simulation_data['balance'].iat[22] -
            ts._close_values['close'].iat[23],
            ts._close_values['close'].iat[23],
            ts._simulation_data['balance'].iat[22] -
            ts._close_values['close'].iat[23] + value])

    def test_process_buy_signal_no_position_open_no_positions_closed(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full_close_none.csv',
            parse_dates=True,
            index_col=0)

        ts._close_values['close'].iat[23] = 20.0

        ts._processBuySignal(i_index=23)

        value = ts._closeOpenPositions(
            price=20, force_all=True, write=False)[0]

        self.assertListEqual(ts._portfolio.iloc[23, :].to_list(),
                             ['long', 1,ts._close_values['close'].iat[23],
                              'open'])

        self.assertListEqual(ts._simulation_data.iloc[23, :].to_list(), [
            'buy', 'long', 1, False, 0, False, 0,
            ts._simulation_data['balance'].iat[22] -
            ts._close_values['close'].iat[23],
            ts._close_values['close'].iat[23],
            ts._simulation_data['balance'].iat[22] -
            ts._close_values['close'].iat[23] + value])

    # Test _processSellSignal

    def test_process_sell_signal_not_enough_balance(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=0.1)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full_close_both.csv',
            parse_dates=True,
            index_col=0)

        ts._simulation_data['balance'].iat[22] = 1

        ts._processSellSignal(i_index=23)

        value = ts._closeOpenPositions(
            price=34.5, force_all=True, write=False)[0]

        self.assertListEqual(ts._portfolio.iloc[23, :].to_list(),
                             ['none', 0, 0.0, 'none'])

        self.assertListEqual(ts._simulation_data.iloc[23, :].to_list(), [
            'sell', 'none', 0, False, 0, False, 0,
            ts._simulation_data['balance'].iat[22],
            ts._close_values['close'].iat[23],
            ts._simulation_data['balance'].iat[22] + value])

    def test_process_sell_signal_less_items_than_max(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=10000000,
                               max_investment=100000)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full_close_both.csv',
            parse_dates=True,
            index_col=0)

        ts._processSellSignal(i_index=23)

        value = ts._closeOpenPositions(
            price=ts._close_values['close'].iat[23], force_all=True,
            write=False)[0]

        self.assertListEqual(ts._portfolio.iloc[23, :].to_list(),
                             ['short', 2899, ts._close_values['close'].iat[23],
                              'open'])

        self.assertListEqual(ts._simulation_data.iloc[23, :].to_list(), [
            'sell', 'short', 2899, False, 0, False, 0,
            ts._simulation_data['balance'].iat[22] +
            2899 * ts._close_values['close'].iat[23],
            ts._close_values['close'].iat[23],
            ts._simulation_data['balance'].iat[22] +
            2899 * ts._close_values['close'].iat[23] + value])

    def test_process_sell_signal_position_open_positions_closed(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=10000)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full_close_both.csv',
            parse_dates=True,
            index_col=0)

        ts._close_values['close'].iat[23] = 22.0

        ts._processSellSignal(i_index=23)

        value = ts._closeOpenPositions(
            price=22, force_all=True, write=False)[0]

        self.assertListEqual(ts._portfolio.iloc[23, :].to_list(),
                             ['short', 1, ts._close_values['close'].iat[23],
                              'open'])

        self.assertListEqual(ts._simulation_data.iloc[23, :].to_list(), [
            'sell', 'short', 1, False, 0, False, 0,
            ts._simulation_data['balance'].iat[22] +
            ts._close_values['close'].iat[23],
            ts._close_values['close'].iat[23],
            ts._simulation_data['balance'].iat[22] +
            ts._close_values['close'].iat[23] + value])

    def test_process_sell_signal_no_position_open_positions_closed(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full_close_both.csv',
            parse_dates=True,
            index_col=0)

        ts._close_values['close'].iat[23] = 22.0

        ts._processSellSignal(i_index=23)

        value = ts._closeOpenPositions(
            price=22, force_all=True, write=False)[0]

        self.assertListEqual(ts._portfolio.iloc[23, :].to_list(),
                             ['short', 1, ts._close_values['close'].iat[23],
                              'open'])

        self.assertListEqual(ts._simulation_data.iloc[23, :].to_list(), [
            'sell', 'short', 1, False, 0, False, 0,
            ts._simulation_data['balance'].iat[22] +
            ts._close_values['close'].iat[23],
            ts._close_values['close'].iat[23],
            ts._simulation_data['balance'].iat[22] +
            ts._close_values['close'].iat[23] + value])

    def test_process_sell_signal_position_open_no_positions_closed(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full_close_none.csv',
            parse_dates=True,
            index_col=0)

        ts._close_values['close'].iat[23] = 20.0

        ts._processSellSignal(i_index=23)

        value = ts._closeOpenPositions(
            price=20, force_all=True, write=False)[0]

        self.assertListEqual(ts._portfolio.iloc[23, :].to_list(),
                             ['short', 1, ts._close_values['close'].iat[23],
                              'open'])

        self.assertListEqual(ts._simulation_data.iloc[23, :].to_list(), [
            'sell', 'short', 1, False, 0, False, 0,
            ts._simulation_data['balance'].iat[22] +
            ts._close_values['close'].iat[23],
            ts._close_values['close'].iat[23],
            ts._simulation_data['balance'].iat[22] +
            ts._close_values['close'].iat[23] + value])

    def test_process_sell_signal_no_position_open_no_positions_closed(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full_close_none.csv',
            parse_dates=True,
            index_col=0)

        ts._close_values['close'].iat[23] = 20.0

        ts._processSellSignal(i_index=23)

        value = ts._closeOpenPositions(
            price=20, force_all=True, write=False)[0]

        self.assertListEqual(ts._portfolio.iloc[23, :].to_list(),
                             ['short', 1, ts._close_values['close'].iat[23],
                              'open'])

        self.assertListEqual(ts._simulation_data.iloc[23, :].to_list(), [
            'sell', 'short', 1, False, 0, False, 0,
            ts._simulation_data['balance'].iat[22] +
            ts._close_values['close'].iat[23],
            ts._close_values['close'].iat[23],
            ts._simulation_data['balance'].iat[22] +
            ts._close_values['close'].iat[23] + value])

    # Test runSimulationRound

    def test_run_simulation_round_first_round_sell(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        cv_df['close'].iat[0] = 100.0

        ts.runSimulationRound(i_index=0, signal=TRADE_SIGNALS['sell'])

        self.assertListEqual(ts._portfolio.iloc[0, :].to_list(),
                             ['none', 0, 0.0, 'none'])

        self.assertListEqual(ts._simulation_data.iloc[0, :].to_list(), [
            'sell', 'none', 0, False, 0, False, 0, 0.0, 34.5, 0.0])

    def test_run_simulation_round_first_round_buy(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        cv_df['close'].iat[0] = 100.0

        ts.runSimulationRound(i_index=0, signal=TRADE_SIGNALS['buy'])

        self.assertListEqual(ts._portfolio.iloc[0, :].to_list(),
                             ['none', 0, 0.0, 'none'])

        self.assertListEqual(ts._simulation_data.iloc[0, :].to_list(), [
            'buy', 'none', 0, False, 0, False, 0, 0.0, 34.5, 0.0])

    def test_run_simulation_round_first_round_hold(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        cv_df['close'].iat[0] = 100.0

        ts.runSimulationRound(i_index=0, signal=TRADE_SIGNALS['hold'])

        self.assertListEqual(ts._portfolio.iloc[0, :].to_list(),
                             ['none', 0, 0.0, 'none'])

        self.assertListEqual(ts._simulation_data.iloc[0, :].to_list(), [
            'hold', 'none', 0, False, 0, False, 0, 0.0, 34.5, 0.0])

    def test_run_simulation_round_no_first_round_sell(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full_close_both.csv',
            parse_dates=True,
            index_col=0)

        value = ts._closeOpenPositions(
            price=34.5, force_all=True, write=False)[0]

        ts.runSimulationRound(i_index=23, signal=TRADE_SIGNALS['sell'])

        self.assertListEqual(ts._portfolio.iloc[23, :].to_list(),
                             ['short', 1, 34.5, 'open'])

        self.assertListEqual(ts._simulation_data.iloc[23, :].to_list(), [
            'sell', 'short', 1, False, 0, False, 0,
            ts._simulation_data['balance'].iat[22] + 34.5, 34.5,
            ts._simulation_data['balance'].iat[22] + value])

    def test_run_simulation_round_no_first_round_buy(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full_close_both.csv',
            parse_dates=True,
            index_col=0)

        value = ts._closeOpenPositions(
            price=34.5, force_all=True, write=False)[0]

        ts.runSimulationRound(i_index=23, signal=TRADE_SIGNALS['buy'])

        self.assertListEqual(ts._portfolio.iloc[23, :].to_list(),
                             ['long', 1, 34.5, 'open'])

        self.assertListEqual(ts._simulation_data.iloc[23, :].to_list(), [
            'buy', 'long', 1, False, 0, False, 0,
            ts._simulation_data['balance'].iat[22] - 34.5, 34.5,
            ts._simulation_data['balance'].iat[22] + value])

    def test_run_simulation_round_no_first_round_hold(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full_close_both.csv',
            parse_dates=True,
            index_col=0)

        value = ts._closeOpenPositions(
            price=34.5, force_all=True, write=False)[0]

        ts.runSimulationRound(i_index=23, signal=TRADE_SIGNALS['hold'])

        self.assertListEqual(ts._portfolio.iloc[23, :].to_list(),
                             ['none', 0, 0.0, 'none'])

        self.assertListEqual(ts._simulation_data.iloc[23, :].to_list(), [
            'hold', 'none', 0, False, 0, False, 0,
            ts._simulation_data['balance'].iat[22], 34.5,
            ts._simulation_data['balance'].iat[22] + value])

    # Test closeSimulation

    def test_close_simulation_round_not_started(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        statistics_expected_result = {
            'number_of_trading_days': 0,
            'number_of_buy_signals': 0,
            'number_of_ignored_buy_signals': 0,
            'number_of_sell_signals': 0,
            'number_of_ignored_sell_signals': 0,
            'balance': 0.0,
            'total_stocks_in_long': 0,
            'total_stocks_in_short': 0,
            'stock_value': 0.0,
            'total_value': 0.0}

        simulation_data_expected_result = pd.DataFrame(
            index=id_df.index,
            columns=['signal',
                     'open_trading_action',
                     'stocks_in_open_transaction',
                     'close_long_trading_actions',
                     'stocks_in_close_long_transactions',
                     'close_short_trading_actions',
                     'stocks_in_close_short_transactions',
                     'balance',
                     'stock_value',
                     'total_value'],
            data=None).sort_index(ascending=True)

        simulation_data, statistics = ts.closeSimulation()

        pd.testing.assert_frame_equal(simulation_data,
                                      simulation_data_expected_result)

        self.assertDictEqual(statistics, statistics_expected_result)

    def test_close_simulation_round_no_trading_actions(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        statistics_expected_result = {
            'number_of_trading_days': 22,
            'number_of_buy_signals': 9,
            'number_of_ignored_buy_signals': 9,
            'number_of_sell_signals': 8,
            'number_of_ignored_sell_signals': 8,
            'balance': 0.0,
            'total_stocks_in_long': 0,
            'total_stocks_in_short': 0,
            'stock_value': 19.09,
            'total_value': 0.0}

        simulation_data_expected_result = pd.read_csv(
            './data/simulation_data_full_without_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_without_actions.csv',
            parse_dates=True,
            index_col=0)

        simulation_data, statistics = ts.closeSimulation()

        pd.testing.assert_frame_equal(simulation_data,
                                      simulation_data_expected_result)

        self.assertDictEqual(statistics, statistics_expected_result)

    def test_close_simulation_round_withTrading_actions(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_items_per_transaction=1,
                               max_investment=None)

        statistics_expected_result = {
            'number_of_trading_days': 23,
            'number_of_buy_signals': 9,
            'number_of_ignored_buy_signals': 4,
            'number_of_sell_signals': 10,
            'number_of_ignored_sell_signals': 5,
            'balance': 31.0,
            'total_stocks_in_long': 4,
            'total_stocks_in_short': 6,
            'stock_value': 19.45,
            'total_value': 122.0}

        simulation_data_expected_result = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True,
            index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full.csv',
            parse_dates=True,
            index_col=0)

        ts._calculateSimulationStatistics()

        pd.testing.assert_frame_equal(ts._simulation_data,
                                      simulation_data_expected_result)

        self.assertDictEqual(ts._statistics, statistics_expected_result)

    # Full simulation test cases

