"""
Trading-Technical-Indicators (tti) python library

File name: test_utils_trading_simulation.py
    tti.utils package, trading_simulation.py module unit tests.
"""

import unittest
import pandas as pd
import numpy as np

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
                              max_exposure=None,
                              short_exposure_factor=1.5)

    def test_close_values_missing(self):

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(TypeError):
            TradingSimulation(input_data_index=id_df.index,
                              max_exposure=None,
                              short_exposure_factor=1.5)

    def test_max_exposure_missing(self):

        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               short_exposure_factor=1.5)

        self.assertEqual(ts._max_exposure, None)

    def test_short_exposure_factor_missing(self):

        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_exposure=None)

        self.assertEqual(ts._short_exposure_factor, 1.5)

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
                              max_exposure=None,
                              short_exposure_factor=1.5)

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
                              max_exposure=None,
                              short_exposure_factor=1.5)

    def test_close_values_wrong_type(self):
        # close values DataFrame
        cv_df = 'No-DF'

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(NotValidInputDataForSimulation):
            TradingSimulation(input_data_index=id_df.index,
                              close_values=cv_df,
                              max_exposure=None,
                              short_exposure_factor=1.5)

    def test_max_exposure_wrong_type(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(WrongTypeForInputParameter):
            TradingSimulation(input_data_index=id_df.index,
                              close_values=cv_df,
                              max_exposure='10000',
                              short_exposure_factor=1.5)

    def test_short_exposure_factor_wrong_type(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(WrongTypeForInputParameter):
            TradingSimulation(input_data_index=id_df.index,
                              close_values=cv_df,
                              max_exposure=None,
                              short_exposure_factor='1.5')

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
                              max_exposure=None,
                              short_exposure_factor=1.5)

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
                              max_exposure=None,
                              short_exposure_factor=1.5)

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
                              max_exposure=None,
                              short_exposure_factor=1.5)

    def test_max_exposure_zero(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(WrongValueForInputParameter):
            TradingSimulation(input_data_index=id_df.index,
                              close_values=cv_df,
                              max_exposure=0.0,
                              short_exposure_factor=1.5)

    def test_max_exposure_negative(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(WrongValueForInputParameter):
            TradingSimulation(input_data_index=id_df.index,
                              close_values=cv_df,
                              max_exposure=-10000,
                              short_exposure_factor=1.5)

    def test_short_exposure_factor_below_one(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(WrongValueForInputParameter):
            TradingSimulation(input_data_index=id_df.index,
                              close_values=cv_df,
                              max_exposure=None,
                              short_exposure_factor=0.99)

    # Other than default values in input arguments test cases

    def test_max_exposure_no_default(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_exposure=10000,
                               short_exposure_factor=1.5)

        self.assertEqual(ts._max_exposure, 10000)

    def test_short_exposure_factor_no_default(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_exposure=None,
                               short_exposure_factor=1.0)

        self.assertEqual(ts._short_exposure_factor, 1.0)

    # Test _calculateSimulationStatistics

    def test_calculate_simulation_statistics_none_simulation_round(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_exposure=None,
                               short_exposure_factor=1.5)

        statistics_expected_result = {
            'number_of_trading_days': 0,
            'number_of_buy_signals': 0,
            'number_of_ignored_buy_signals': 0,
            'number_of_sell_signals': 0,
            'number_of_ignored_sell_signals': 0,
            'last_stock_value': 0.0,
            'last_exposure': 0.0,
            'last_open_long_positions': 0,
            'last_open_short_positions': 0,
            'last_portfolio_value': 0.0,
            'last_earnings': 0.0,
            'final_balance': 0.0}

        ts._simulation_data = pd.read_csv('./data/simulation_data_empty.csv',
                                          parse_dates=True, index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_empty.csv', parse_dates=True,
            index_col=0).to_numpy(dtype=np.float64, copy=True)

        ts._calculateSimulationStatistics()

        self.assertDictEqual(ts._statistics, statistics_expected_result)

    def test_calculate_simulation_statistics_ten_simulation_rounds(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_exposure=None,
                               short_exposure_factor=1.5)

        statistics_expected_result = {
            'number_of_trading_days': 10,
            'number_of_buy_signals': 4,
            'number_of_ignored_buy_signals': 1,
            'number_of_sell_signals': 3,
            'number_of_ignored_sell_signals': 2,
            'last_stock_value': 34.37,
            'last_exposure': 109.0,
            'last_open_long_positions': 2,
            'last_open_short_positions': 3,
            'last_portfolio_value': 209.0,
            'last_earnings': 309.0,
            'final_balance': 409.0}

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_with_actions_ten_rounds.csv',
            parse_dates=True, index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_ten_rounds.csv',
            parse_dates=True, index_col=0).to_numpy(dtype=np.float64,
                                                    copy=True)

        ts._calculateSimulationStatistics()

        self.assertDictEqual(ts._statistics, statistics_expected_result)

    def test_calculate_simulation_statistics_all_simulation_rounds(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_exposure=None,
                               short_exposure_factor=1.5)

        self.maxDiff = None

        statistics_expected_result = {
            'number_of_trading_days': 3169,
            'number_of_buy_signals': 1297,
            'number_of_ignored_buy_signals': 1029,
            'number_of_sell_signals': 1152,
            'number_of_ignored_sell_signals': 741,
            'last_stock_value': 140.41,
            'last_exposure': 3268.0,
            'last_open_long_positions': 397,
            'last_open_short_positions': 396,
            'last_portfolio_value': 3368.0,
            'last_earnings': 3468.0,
            'final_balance': 3568.0}

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True, index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full.csv',
            parse_dates=True, index_col=0).to_numpy(dtype=np.float64,
                                                    copy=True)

        ts._calculateSimulationStatistics()

        self.assertDictEqual(ts._statistics, statistics_expected_result)

    def test_calculate_simulation_statistics_no_opened_positions(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_exposure=None,
                               short_exposure_factor=1.5)

        self.maxDiff = None

        statistics_expected_result = {
            'number_of_trading_days': 3169,
            'number_of_buy_signals': 1297,
            'number_of_ignored_buy_signals': 1297,
            'number_of_sell_signals': 1152,
            'number_of_ignored_sell_signals': 1152,
            'last_stock_value': 140.41,
            'last_exposure': 0.0,
            'last_open_long_positions': 0,
            'last_open_short_positions': 0,
            'last_portfolio_value': 0.0,
            'last_earnings': 0.0,
            'final_balance': 0.0}

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_without_actions.csv',
            parse_dates=True, index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full_no_positions.csv',
            parse_dates=True, index_col=0).to_numpy(dtype=np.float64,
                                                    copy=True)

        ts._calculateSimulationStatistics()

        self.assertDictEqual(ts._statistics, statistics_expected_result)

    # Test _calculatePortfolioValue

    def test_calculate_portfolio_value(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_exposure=None,
                               short_exposure_factor=1.5)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_ten_rounds.csv',
            parse_dates=True, index_col=0).to_numpy(dtype=np.float64,
                                                    copy=True)

        value = ts._calculatePortfolioValue(i_index=9)

        self.assertEqual(value, 34.37 * (2 - 3))

    # Test _closeOpenPositions earnings, closed_exposure

    def test_close_open_positions_none_open_no_force_all_write(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_exposure=None,
                               short_exposure_factor=1.5)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_none_open_ten_rounds.csv',
            parse_dates=True, index_col=0).to_numpy(dtype=np.float64,
                                                    copy=True)

        portfolio_expected_result = pd.read_csv(
            './data/portfolio_simulation_data_none_open_ten_rounds.csv',
            parse_dates=True, index_col=0).to_numpy(dtype=np.float64,
                                                    copy=True)

        ts._simulation_data['exposure'].iat[8] = 100.0
        ts._simulation_data['earnings'].iat[8] = 200.0

        earnings, closed_exposure = ts._closeOpenPositions(i_index=9)

        self.assertEqual(earnings, 0.0)

        self.assertEqual(closed_exposure, 0.0)

        np.testing.assert_equal(ts._simulation_data['exposure'].iat[9], 100.0)

        np.testing.assert_equal(ts._simulation_data['earnings'].iat[9], 200.0)

        np.testing.assert_equal(ts._portfolio, portfolio_expected_result)

    def test_close_open_positions_with_open_no_force_all_write(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_exposure=None,
                               short_exposure_factor=1.5)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_all_open_ten_rounds.csv',
            parse_dates=True, index_col=0).to_numpy(dtype=np.float64,
                                                    copy=True)

        portfolio_expected_result = pd.read_csv(
            './data/portfolio_simulation_data_all_open_ten_rounds.csv',
            parse_dates=True, index_col=0).to_numpy(dtype=np.float64,
                                                    copy=True)

        portfolio_expected_result[0, 1] = 2.0
        portfolio_expected_result[2, 1] = 2.0
        portfolio_expected_result[5, 1] = 2.0

        portfolio_expected_result[5, 2] = 40.00

        ts._simulation_data['exposure'].iat[8] = 100.0
        ts._simulation_data['earnings'].iat[8] = 200.0
        ts._portfolio[5, 2] = 40.00

        ts._close_values[9, 0] = 24.0

        earnings, closed_exposure = ts._closeOpenPositions(i_index=9)

        exposure_expected = 20.50 + 22.50 + 40.00

        earnings_expected = (2 * 24.0 - 20.5 - 22.5) + \
                            ((40.00 / 1.5) - 1 * 24.0)

        self.assertEqual(earnings, earnings_expected)

        self.assertEqual(closed_exposure, exposure_expected)

        np.testing.assert_equal(ts._simulation_data['exposure'].iat[9],
                                ts._simulation_data['exposure'].iat[8] -
                                exposure_expected)

        np.testing.assert_equal(ts._simulation_data['earnings'].iat[9],
                                ts._simulation_data['earnings'].iat[8] +
                                earnings_expected)

        np.testing.assert_equal(ts._portfolio, portfolio_expected_result)

    # Tests for runSimulationRound (indirectly tests also _processSignal)

    def test_run_simulation_round_first_round_hold(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_exposure=None,
                               short_exposure_factor=1.5)

        ts.runSimulationRound(i_index=0, signal=TRADE_SIGNALS['hold'])

        self.assertListEqual(
            list(ts._portfolio[0, :]),
            [0.0,
             0.0,
             0.0])

        self.assertListEqual(
            ts._simulation_data.iloc[0, :].to_list(),
            ['hold',
             'none',
             ts._close_values[0, 0],
             0.0,
             0.0,
             0.0,
             0.0])

    def test_run_simulation_round_first_round_buy(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_exposure=None,
                               short_exposure_factor=1.5)

        ts.runSimulationRound(i_index=0, signal=TRADE_SIGNALS['buy'])

        self.assertListEqual(
            list(ts._portfolio[0, :]),
            [0.0,
             0.0,
             0.0])

        self.assertListEqual(
            ts._simulation_data.iloc[0, :].to_list(),
            ['buy',
             'none',
             ts._close_values[0, 0],
             0.0,
             0.0,
             0.0,
             0.0])

    def test_run_simulation_round_first_round_sell(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_exposure=None,
                               short_exposure_factor=1.5)

        ts.runSimulationRound(i_index=0, signal=TRADE_SIGNALS['sell'])

        self.assertListEqual(
            list(ts._portfolio[0, :]),
            [0.0,
             0.0,
             0.0])

        self.assertListEqual(
            ts._simulation_data.iloc[0, :].to_list(),
            ['sell',
             'none',
             ts._close_values[0, 0],
             0.0,
             0.0,
             0.0,
             0.0])

    def test_run_simulation_round_hold(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_exposure=None,
                               short_exposure_factor=1.5)

        ts.runSimulationRound(i_index=0, signal=TRADE_SIGNALS['hold'])
        ts.runSimulationRound(i_index=1, signal=TRADE_SIGNALS['hold'])

        self.assertListEqual(list(ts._portfolio[1, :]),
                             [0.0, 0.0, 0.0])

        self.assertListEqual(
            ts._simulation_data.iloc[1, :].to_list(),
            ['hold',
             'none',
             ts._close_values[1, 0],
             ts._simulation_data['exposure'].iat[0],
             ts._simulation_data['portfolio_value'].iat[0],
             ts._simulation_data['earnings'].iat[0],
             0.0])

    def test_run_simulation_round_buy(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_exposure=None,
                               short_exposure_factor=1.5)

        ts.runSimulationRound(i_index=0, signal=TRADE_SIGNALS['buy'])
        ts.runSimulationRound(i_index=1, signal=TRADE_SIGNALS['buy'])
        ts.runSimulationRound(i_index=2, signal=TRADE_SIGNALS['buy'])

        self.assertListEqual(list(ts._portfolio[2, :]), [2.0, 1.0,
                                                   ts._close_values[2, 0]])

        self.assertListEqual(
            ts._simulation_data.iloc[2, :].to_list(),
            ['buy',
             'long',
             ts._close_values[2, 0],
             ts._simulation_data['exposure'].iat[0] +
             ts._simulation_data['exposure'].iat[1] +
             ts._close_values[2, 0],
             2 * ts._close_values[2, 0],
             0.0,
             2 * ts._close_values[2, 0]])

    def test_run_simulation_round_sell(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_exposure=None,
                               short_exposure_factor=1.5)

        ts.runSimulationRound(i_index=0, signal=TRADE_SIGNALS['sell'])
        ts.runSimulationRound(i_index=1, signal=TRADE_SIGNALS['sell'])

        self.assertListEqual(list(ts._portfolio[1, :]),
                             [1.0, 1.0, 1.5 * ts._close_values[1, 0]])

        self.assertListEqual(
            ts._simulation_data.iloc[1, :].to_list(),
            ['sell',
             'short',
             ts._close_values[1, 0],
             ts._simulation_data['exposure'].iat[0] +
             1.5 * ts._close_values[1, 0],
             - ts._close_values[1, 0],
             0.0,
             - ts._close_values[1, 0]])

    def test_run_simulation_round_buy_max_exposure(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_exposure=1,
                               short_exposure_factor=1.5)

        ts.runSimulationRound(i_index=0, signal=TRADE_SIGNALS['buy'])
        ts.runSimulationRound(i_index=1, signal=TRADE_SIGNALS['buy'])
        ts.runSimulationRound(i_index=2, signal=TRADE_SIGNALS['buy'])

        self.assertListEqual(list(ts._portfolio[2, :]),
                             [0.0, 0.0, 0.0])

        self.assertListEqual(
            ts._simulation_data.iloc[2, :].to_list(),
            ['buy',
             'none',
             ts._close_values[2, 0],
             0.0,
             0.0,
             0.0,
             0.0])

    def test_run_simulation_round_sell_max_exposure(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_exposure=1,
                               short_exposure_factor=1.5)

        ts.runSimulationRound(i_index=0, signal=TRADE_SIGNALS['sell'])
        ts.runSimulationRound(i_index=1, signal=TRADE_SIGNALS['sell'])

        self.assertListEqual(list(ts._portfolio[1, :]),
                             [0.0, 0.0, 0.0])

        self.assertListEqual(
            ts._simulation_data.iloc[1, :].to_list(),
            ['sell',
             'none',
             ts._close_values[1, 0],
             0.0,
             0.0,
             0.0,
             0.0])

    # Tests for closeSimulation

    def test_close_simulation(self):
        # close values DataFrame
        cv_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)[['close']]

        # input_data DataFrame
        id_df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                            index_col=0)

        ts = TradingSimulation(input_data_index=id_df.index,
                               close_values=cv_df,
                               max_exposure=None,
                               short_exposure_factor=1.5)

        self.maxDiff = None

        statistics_expected_result = {
            'number_of_trading_days': 3169,
            'number_of_buy_signals': 1297,
            'number_of_ignored_buy_signals': 1029,
            'number_of_sell_signals': 1152,
            'number_of_ignored_sell_signals': 741,
            'last_stock_value': 140.41,
            'last_exposure': 3268.0,
            'last_open_long_positions': 397,
            'last_open_short_positions': 396,
            'last_portfolio_value': 3368.0,
            'last_earnings': 3468.0,
            'final_balance': 3568.0}

        ts._simulation_data = pd.read_csv(
            './data/simulation_data_full_with_actions.csv',
            parse_dates=True, index_col=0)

        ts._portfolio = pd.read_csv(
            './data/portfolio_simulation_data_full.csv',
            parse_dates=True, index_col=0).to_numpy(dtype=np.float64,
                                                    copy=True)

        sd_result, st_result = ts.closeSimulation()

        pd.testing.assert_frame_equal(sd_result, ts._simulation_data)
        self.assertDictEqual(st_result, statistics_expected_result)
