"""
Trading-Technical-Indicators (tti) python library

File name: _technical_indicator.py
    Parent class for all the technical indicators.
"""

import pandas as pd
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod

from .properties.indicators_properties import INDICATORS_PROPERTIES
from ..utils.plot import linesGraph
from ..utils.data_validation import validateInputData
from ..utils.exceptions import WrongTypeForInputParameter, \
    TtiPackageDeprecatedMethod
from ..utils.trading_simulation import TradingSimulation


class TechnicalIndicator(ABC):
    """
    Technical Indicators class implementation. It is used as a parent class for
    each implemented technical indicator. It implements the public API for
    accessing the calculated values, graph and signal of each indicator.

    Args:
        calling_instance (str): The name of the calling class.

        input_data (pandas.DataFrame): The input data. The index is of type
            ``pandas.DatetimeIndex``.

        fill_missing_values (bool, default=True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        _calling_instance (str): The name of the calling class.

        _properties (dict): Indicator properties.

        _input_data (pandas.DataFrame): The input data after preprocessing.

        _ti_data (pandas.DataFrame): Technical Indicator calculated data.

    Raises:
        WrongTypeForInputParameter: The type of an input parameter is invalid.
        NotEnoughInputData: Not enough data for calculating the indicator.
    """

    def __init__(self, calling_instance, input_data, fill_missing_values=True):

        # Validate fill missing values input parameter
        if not isinstance(fill_missing_values, bool):
            raise WrongTypeForInputParameter(
                type(fill_missing_values), 'fill_missing_values', 'bool')

        self._calling_instance = calling_instance

        # Read the properties for the specific Technical Indicator
        self._properties = INDICATORS_PROPERTIES[calling_instance]

        # Input data preprocessing
        self._input_data = \
            validateInputData(input_data,
                              self._properties['required_input_data'],
                              calling_instance,
                              fill_missing_values=fill_missing_values)

        # Calculation of the Technical Indicator
        self._ti_data = self._calculateTi()

    @staticmethod
    def _rolling_pipe(df, window, function):
        """
        Applies a function to a pandas rolling pipe.

        Args:
            df (pandas.DataFrame): The input pandas.DataFrame.

            window (int): The size of the rolling window.

            function (function): The function to be applied.

        Returns:
           pandas.Series: The result of the applied function.
        """

        return pd.Series(
            [df.iloc[i - window: i].pipe(function) if i >= window
             else None for i in range(1, len(df) + 1)],
            index=df.index)

    @abstractmethod
    def _calculateTi(self):
        """
        Calculates the technical indicator for the given input data.

        Returns:
            pandas.DataFrame: The calculated indicator. Index is of type date.
            It can contain several columns depending the indicator.

        Raises:
            NotImplementedError: Abstract method not implemented.
        """

        raise NotImplementedError

    @abstractmethod
    def getTiSignal(self):
        """
        Calculates and returns the trading signal for the calculated technical
        indicator.

        Returns:
            {('hold', 0), ('buy', -1), ('sell', 1)}: The calculated trading
            signal.

        Raises:
            NotImplementedError: Abstract method not implemented.
        """

        raise NotImplementedError

    def getTiData(self):
        """
        Returns the Technical Indicator values for the whole period.

        Returns:
            pandas.DataFrame: The Technical Indicator values.
        """

        return self._ti_data

    def getTiValue(self,  date=None):
        """
        Returns the Technical Indicator value for a given date. If the date
        is None, it returns the most recent entry.

        Args:
            date (str, default=None): A date string, in the same format as the
                format of the ``input_data`` index.

        Returns:
            [float] or None: The value of the Technical Indicator for the given
            date. If none value found for the given date, returns None.
        """

        try:
            if date is None:
                return list(self._ti_data.iloc[-1, :])
            else:
                return list(self._ti_data.loc[pd.to_datetime(date), :])

        except (Exception, ValueError):
            return None

    def getTiGraph(self):
        """
        Generates a plot customized for each Technical Indicator.

        Returns:
            matplotlib.pyplot: The generated plot.
        """

        # Check if split to subplots is required for this Indicator
        if self._properties['graph_subplots']:
            data = [self._input_data[self._properties['graph_input_columns']],
                    self._ti_data]
        else:
            data = pd.concat([self._input_data[
                                  self._properties['graph_input_columns']],
                              self._ti_data], axis=1)

        return linesGraph(data=data, title=self._properties['long_name'],
                          y_label=self._properties['graph_y_label'],
                          lines_color=self._properties['graph_lines_color'],
                          alpha_values=self._properties['graph_alpha_values'],
                          areas=self._properties['graph_areas'])

    def runSimulation(self, close_values, max_items_per_transaction=1,
                      max_investment=0.0):
        """
        Deprecated method since release ``0.1.b3``. Replaced by the
        ``getTiSimulation`` method. This code will be removed from the package
        in stable-release ``1.0``.

        Raises:
            TtiPackageDeprecatedMethod: Method is deprecated.
        """

        raise TtiPackageDeprecatedMethod(
            'runSimulation', '0.1.b3',
            ' It has been replaced by the getTiSimulation method.')

    @staticmethod
    def _getSimulationGraph(simulation, title):
        """
        Returns a matplotlib.pyplot graph with simulation data.

        Parameters:
            simulation (pandas.DataFrame): Simulation data collected during the
                execution of the trading simulation.

            title (str): Title of the graph.

        Raises:
            -

        Returns:
            (matplotlib.pyplot): The produced graph.
        """

        plt.figure(figsize=(7, 5))

        plt.subplot(3, 1, 1)
        plt.plot(list(range(1, len(simulation['stock_value']) + 1)),
            simulation['stock_value'], label='close_price', color='limegreen')
        plt.legend(loc=0)
        plt.grid(which='major', axis='y', alpha=0.5)
        plt.title(title, fontsize=11, fontweight='bold')
        plt.gca().axes.get_xaxis().set_visible(False)

        plt.subplot(3, 1, 2)
        plt.plot(list(range(1, len(simulation['exposure']) + 1)),
                 simulation['exposure'], label='exposure',
                 color='tomato')
        plt.legend(loc=0)
        plt.grid(which='major', axis='y', alpha=0.5)
        plt.gca().axes.get_xaxis().set_visible(False)

        plt.subplot(3, 1, 3)
        plt.plot(list(range(1, len(simulation['balance']) + 1)),
                 simulation['balance'], label='balance',
                 color='cornflowerblue')
        plt.legend(loc=0)
        plt.grid(which='major', axis='y', alpha=0.5)

        plt.xlabel('Transactions', fontsize=11, fontweight='bold')
        plt.gcf().text(0.01, 0.5, 'Balance | Exposure | Price', fontsize=11,
                       fontweight='bold', va='center', rotation='vertical')

        return plt

    def getTiSimulation(self, close_values, max_exposure=None,
                        short_exposure_factor=1.5):
        """
        Executes trading simulation based on the trading signals produced by
        the technical indicator, by applying an Active trading strategy. With
        a ``buy`` trading signal a new ``long`` position is opened. With a
        ``sell`` trading signal a new ``short`` position is opened. Opened
        positions are scanned on each simulation round, and if conditions are
        met (current stock price > bought price for opened ``long`` positions
        and current stock price < bought price for opened ``short`` positions)
        the positions are being closed. Only one stock piece is used in each
        open transaction.

        Args:
            close_values (pandas.DataFrame): The close prices of the stock, for
                the whole simulation period. Index is of type DateTimeIndex
                with same values as the input to the indicator data. It
                contains one column ``close``.

            max_exposure(float, default=None): Maximum allowed exposure for all
                the opened positions (``short`` and ``long``). If the exposure
                reaches this threshold, no further positions are being opened.
                A new position can be opened again only when exposure reduces
                through a position close. If set to None, then there is no
                upper limit for the opened positions (exposure). When a new
                ``long`` position is opened, exposure is increased by the
                ``stock_price``. When a ``short`` position is opened, exposure
                is increased by the ``short_exposure_factor * stock_price``.
                Values >0.0 or None are supported.

            short_exposure_factor (float, default=1.5): The exposure factor
                when a new ``short`` position is opened. Usually is above 1.0
                and it is used as security when a short position is opened.
                Values >=1.0 are supported.

        Returns:
            (pandas.DataFrame, dict, matplotlib.pyplot): Dataframe which holds
            details about the trading simulation executed, dictionary which
            holds statistics about the simulation and a graph which displays
            the stock price, the exposure, and the balance during the
            simulation.

            The index of the dataframe is the whole trading period
            (DateTimeIndex).Columns are:

            ``signal``: the signal produced at each day of the simulation
            period.

            ``open_trading_action``: the open trading action applied. Possible
            values are ``long``, ``short`` and ``none``.

            ``stock_value``: The value of the stock during the simulation
            period.

            ``exposure``: The accumulated exposure during the simulation
            period. Increased by ``stock_price`` when a ``long`` position is
            opened, and by ``short_exposure_factor * stock_price`` when a
            ``short`` position is opened. Reduced by the same amounts when
            relevant positions are being closed.

            ``portfolio_value``: The portfolio value during the simulation
            period, ``current_stock_price * (opened_long - opened_short)``.

            ``earnings``: The accumulated earnings during the simulation
            period. Increased by the ``current_price - opened_position_price``
            when a ``long`` position is closed. Increased by the
            ``opened_position_price - current_price`` when a ``short`` position
            is closed.

            ``balance``: The balance during the simulation period. It is the
            ``earnings + portfolio_value``.

            The dictionary contains the below keys:

            ``number_of_trading_days``: the number of trading days in the
            simulation round.

            ``number_of_buy_signals``: the number of ``buy`` signals produced
            during the simulation period.

            ``number_of_ignored_buy_signals``: the number of ``buy`` signals
            ignored because of the ``max_exposure`` limitation.

            ``number_of_sell_signals``: the number of ``sell`` signals produced
            during the simulation period.

            ``number_of_ignored_sell_signals``: the number of ``sell`` signals
            ignored because of the ``max_exposure`` limitation.

            ``last_stock_value``: The value of the stock at the end of the
            simulation.

            ``last_exposure``: The ``exposure`` value at the end of the
            simulation period.

            ``last_open_long_positions``: The number of the still opened
            ``long`` positions at the end of the simulation period.

            ``last_open_short_positions``: The number of the still opened
            ``short`` positions at the end of the simulation period.

            ``last_portfolio_value``: The ``portfolio_value`` at the end of the
            simulation period.

            ``last_earnings``: The ``earnings`` at the end of the simulation
            period.

            ``final_balance``: The ``balance`` at the end of the simulation
            period.

        Raises:
            WrongTypeForInputParameter: Input argument has wrong type.
            WrongValueForInputParameter: Unsupported value for input argument.
            NotValidInputDataForSimulation: Invalid ``close_values`` passed
                for the simulation.
        """

        # Create Trading Simulation instance
        simulator = TradingSimulation(
            input_data_index=self._input_data.index,
            close_values=close_values,
            max_exposure=max_exposure,
            short_exposure_factor=short_exposure_factor)

        # keep safe the full input and indicator data
        full_ti_data = self._ti_data
        full_input_data = self._input_data

        # Run simulation rounds for the whole period
        for i in range(len(self._ti_data.index)):

            # Limit the input and indicator data to this simulation round
            self._input_data = full_input_data[
                full_input_data.index <= full_input_data.index[i]]

            self._ti_data = full_ti_data[
                full_ti_data.index <= full_ti_data.index[i]]

            simulator.runSimulationRound(i_index=i, signal=self.getTiSignal())

        # Restore input and indicator data to full range
        self._ti_data = full_ti_data
        self._input_data = full_input_data

        simulation_data, statistics = simulator.closeSimulation()

        return simulation_data, statistics, \
            self._getSimulationGraph(simulation_data,
            'Trading Simulation for ' + self._calling_instance)
