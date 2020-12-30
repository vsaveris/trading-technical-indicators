"""
Trading-Technical-Indicators (tti) python library

File name: test_indicators_common.py
    tti.indicators package, Abstract class for common unit tests applicable for
    all the indicators.
"""

from abc import ABC, abstractmethod

import pandas as pd
import matplotlib.pyplot as plt
import copy
import numpy as np

from tti.utils.exceptions import NotEnoughInputData, \
    WrongTypeForInputParameter, WrongValueForInputParameter, \
    TtiPackageDeprecatedMethod


class TestIndicatorsCommon(ABC):

    # Definition of the abstract methods and properties
    @abstractmethod
    def assertRaises(self, *kwargs):
        raise NotImplementedError

    @abstractmethod
    def subTest(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def assertEqual(self, *kwargs):
        raise NotImplementedError

    @abstractmethod
    def assertIn(self, *kwargs):
        raise NotImplementedError

    @property
    @abstractmethod
    def indicator(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def indicator_input_arguments(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def indicator_other_input_arguments(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def indicator_minimum_required_data(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def graph_file_name(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def indicator_test_data_file_name(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def mandatory_arguments_missing_cases(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def arguments_wrong_type(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def arguments_wrong_value(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def required_input_data_columns(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def ti_data_rows(self):
        raise NotImplementedError

    precision = 4

    # Unit Tests

    # Validate indicators input arguments

    def test_mandatory_input_arguments_missing(self):
        for arguments_set in self.mandatory_arguments_missing_cases:
            with self.subTest(arguments_set=arguments_set):
                with self.assertRaises(TypeError):
                    self.indicator(**arguments_set)

    def test_input_arguments_wrong_type(self):
        for arguments_set in self.arguments_wrong_type:
            with self.subTest(arguments_set=arguments_set):
                with self.assertRaises(WrongTypeForInputParameter):
                    self.indicator(**arguments_set)

    def test_input_arguments_wrong_value(self):
        for arguments_set in self.arguments_wrong_value:
            with self.subTest(arguments_set=arguments_set):
                with self.assertRaises(WrongValueForInputParameter):
                    self.indicator(**arguments_set)

    # Validate input argument: input_data

    def test_argument_input_data_wrong_index_type(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=1)

        with self.assertRaises(TypeError):
            self.indicator(df)

    def test_argument_input_data_required_column_missing(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        for missing_column in self.required_input_data_columns:
            with self.subTest(
                    missing_column=missing_column):
                with self.assertRaises(ValueError):
                    self.indicator(pd.DataFrame(
                        df.drop(columns=[missing_column])))

    def test_argument_input_data_values_wrong_type(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df.iloc[0, :] = 'no-numeric'

        with self.assertRaises(ValueError):
            self.indicator(df)

    def test_argument_input_data_empty(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(ValueError):
            self.indicator(pd.DataFrame(df[df.index >= '2032-01-01']))

    # Validate input argument: fill_missing_values

    def test_argument_fill_missing_values_is_true(self):
        df = pd.read_csv('./data/missing_values_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/missing_values_filled.csv', parse_dates=True, index_col=0
        )[self.required_input_data_columns].round(self.precision)

        df_result = self.indicator(
            df, fill_missing_values=True, **self.indicator_input_arguments
        )._input_data[self.required_input_data_columns]

        pd.testing.assert_frame_equal(df_result, df_expected_result)

    def test_argument_fill_missing_values_is_false(self):
        df = pd.read_csv('./data/missing_values_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/missing_values_data_sorted.csv', parse_dates=True,
            index_col=0)[self.required_input_data_columns].round(
            self.precision)

        df_result = self.indicator(
            df, fill_missing_values=False, **self.indicator_input_arguments
        )._input_data[self.required_input_data_columns]

        pd.testing.assert_frame_equal(df_result, df_expected_result)

    def test_argument_fill_missing_values_is_default_true(self):
        df = pd.read_csv('./data/missing_values_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(
            './data/missing_values_filled.csv', parse_dates=True, index_col=0
        )[self.required_input_data_columns].round(self.precision)

        df_result = self.indicator(
            df, **self.indicator_input_arguments
        )._input_data[self.required_input_data_columns]

        pd.testing.assert_frame_equal(df_result, df_expected_result)

    # Validate indicator creation

    def test_validate_indicator_input_data_one_row(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        if self.indicator_minimum_required_data > 1:
            with self.assertRaises(NotEnoughInputData):
                self.indicator(df[df.index == '2000-02-01'])
        else:
            self.indicator(df[df.index == '2000-02-01'])

    def test_validate_indicator_less_than_required_input_data(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        if self.indicator_minimum_required_data != 1:
            with self.assertRaises(NotEnoughInputData):
                self.indicator(
                    df.iloc[:self.indicator_minimum_required_data - 1],
                    **self.indicator_input_arguments)
        else:
            pass

    def test_validate_indicator_exactly_required_input_data(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        self.indicator(df.iloc[:self.indicator_minimum_required_data],
            **self.indicator_input_arguments)

    def test_validate_indicator_full_data(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(self.indicator_test_data_file_name,
            parse_dates=True, index_col=0).round(self.precision)

        df_result = self.indicator(
            df, **self.indicator_input_arguments)._ti_data

        pd.testing.assert_frame_equal(df_expected_result, df_result,
                                      check_dtype=False)

    def test_validate_indicator_full_data_default_arguments(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        self.indicator(df)

    def test_validate_indicator_full_data_other_arguments_values(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        for arguments_set in self.indicator_other_input_arguments:
            with self.subTest(arguments_set=arguments_set):
                self.indicator(df, **arguments_set)

    # Validate API

    def test_getTiGraph(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        indicator = self.indicator(df, **self.indicator_input_arguments)

        # Needs manual check of the produced graph
        self.assertEqual(indicator.getTiGraph(), plt)

        indicator.getTiGraph().savefig(self.graph_file_name)
        plt.close('all')

    def test_getTiData(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(self.indicator_test_data_file_name,
            parse_dates=True, index_col=0).round(self.precision)

        pd.testing.assert_frame_equal(
            df_expected_result,
            self.indicator(df, **self.indicator_input_arguments).getTiData(),
            check_dtype=False)

    def test_getTiValue_specific(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(self.indicator_test_data_file_name,
            parse_dates=True, index_col=0).round(self.precision)

        self.assertEqual(list(df_expected_result.loc['2009-10-19', :]),
            self.indicator(df, **self.indicator_input_arguments).
                         getTiValue('2009-10-19'))

    def test_getTiValue_latest(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        df_expected_result = pd.read_csv(self.indicator_test_data_file_name,
            parse_dates=True, index_col=0).round(self.precision)

        # Adaptation for the pandas release 1.2.0, check github issue #20
        expected_result = list(df_expected_result.iloc[-1])
        actual_result = self.indicator(df, **self.indicator_input_arguments).\
            getTiValue()

        for x, y in zip(expected_result, actual_result):
            try:
                self.assertAlmostEqual(x, y, places=4)
            except:
                self.assertAlmostEqual(x, y, places=3)

    def test_getTiSignal(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        self.assertIn(self.indicator(
            df, **self.indicator_input_arguments).getTiSignal(),
                      [('buy', -1), ('hold', 0), ('sell', 1)])

    def test_getTiSignal_minimum_required_data(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        self.assertIn(
            self.indicator(df.iloc[:self.indicator_minimum_required_data],
                           **self.indicator_input_arguments).getTiSignal(),
            [('buy', -1), ('hold', 0), ('sell', 1)])

    def test_simulation_deprecated(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        with self.assertRaises(TtiPackageDeprecatedMethod):
            self.indicator(df[df.index >= '2011-09-12'],
                           **self.indicator_input_arguments).runSimulation(
                close_values=df[df.index >= '2011-09-12'])

    def test_getTiSimulation(self):

        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        ti = self.indicator(df, **self.indicator_input_arguments)

        orig_input_data = copy.deepcopy(ti._input_data)
        orig_ti_data = copy.deepcopy(ti._ti_data)
        simulation_data, statistics, graph = \
            ti.getTiSimulation(df[['close']])

        if str(self.indicator) == \
                "<class 'tti.indicators._detrended_price_oscillator." + \
                "DetrendedPriceOscillator'>":
            self.assertEqual(simulation_data.isnull().values[:-4].any(), False)
            self.assertEqual(statistics['number_of_trading_days'], 3165)
        else:
            self.assertEqual(simulation_data.isnull().values.any(), False)
            self.assertEqual(statistics['number_of_trading_days'], 3169)

        self.assertEqual(any(np.isnan(val) for val in statistics.values()),
                         False)

        pd.testing.assert_frame_equal(ti._input_data, orig_input_data)
        pd.testing.assert_frame_equal(ti._ti_data, orig_ti_data)

        # Needs manual check of the produced graph
        self.assertEqual(graph, plt)

        graph.savefig('./figures/trading_simulation_graph_' +
            str(self.indicator).split('.')[-1][:-2] + '.png')
        plt.close('all')

    # Validate API for specific number of rows in calculated indicator
    def test_api_for_variable_ti_data_length(self):
        df = pd.read_csv('./data/sample_data.csv', parse_dates=True,
                         index_col=0)

        for rows in self.ti_data_rows:
            with self.subTest(rows=rows):

                ti = self.indicator(pd.DataFrame(df))
                ti._ti_data = ti._ti_data.iloc[:rows]

                ti.getTiSignal()
                ti.getTiValue()
                ti.getTiData()
                ti.getTiGraph()
                ti.getTiSimulation(df[['close']])
