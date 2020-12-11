"""
Trading-Technical-Indicators (tti) python library

File name: _technical_indicator.py
    Parent class for all the technical indicators.
"""

import pandas as pd
from abc import ABC, abstractmethod

from .properties.indicators_properties import INDICATORS_PROPERTIES
from ..utils.plot import linesGraph
from ..utils.data_validation import validateInputData
from ..utils.trading_simulation import TradingSimulation
from ..utils.exceptions import WrongTypeForInputParameter, \
    NotValidInputDataForSimulation, WrongValueForInputParameter


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
        Executes trading simulation based on the trading signals produced by
        the technical indicator, by applying an Active trading strategy. With
        a ``buy`` trading signal a new ``long`` position is opened. With a
        ``sell`` trading signal a new ``short`` position is opened. Opened
        positions are scanned on each simulation round, and if conditions are
        met (current stock price > bought price for opened ``long`` positions
        and current stock price < bought price for opened ``short`` positions)
        the positions are being closed. When a position is opened, the number
        of stocks is decided by considering the input arguments.

        Args:
             close_values (pandas.DataFrame): The close prices of the stock,
                for the whole simulation period. Index is of type DateTimeIndex
                with same values as the input to the indicator data. It
                contains one column ``close``.

            max_items_per_transaction (int, default=1): The maximum number of
                stocks to be traded on each ``open_long`` or ``open_short``
                transaction.

            max_investment(float, default=None): Maximum investment for all the
                opened positions (``short`` and ``long``). If the sum of all
                the opened positions reached the maximum investment, then it is
                not allowed to open a new position. A new position can be
                opened when some balance becomes available from a position
                close. If set to  None, then there is no upper limit for the
                opened positions.

        Returns:
            (pandas.DataFrame, dict): Dataframe which holds details and
            dictionary which holds statistics about the simulation.

            The index of the dataframe is the whole trading period
            (DateTimeIndex).Columns are:

            ``signal``: the signal produced at each day of the simulation
            period.

            ``trading_action``: the trading action applied. Possible values are
            ``open_long``, ``close_long``, ``open_short``, ``close_short`` and
            ``none``.

            ``stocks_in_transaction``: the number of stocks involved in a
            trading_action.

            ``balance``: the available balance (earnings - spending).

            ``stock_value``: The value of the stock during the simulation
            period.

            ``total_value``: the available balance considering the open
            positions (if they should be closed in this transaction).

            The dictionary contains the below keys:

            ``number_of_trading_days``: the number of trading days in the
            simulation round.

            ``number_of_buy_signals``: the number of ``buy`` signals produced
            during the simulation period.

            ``number_of_ignored_buy_signals``: the number of ``buy`` signals
            ignored because of the ``max_investment`` limitation.

            ``number_of_sell_signals``: the number of ``sell`` signals produced
            during the simulation period.

            ``number_of_ignored_sell_signals``: the number of ``sell`` signals
            ignored because of the ``max_investment`` limitation.

            ``balance``: the final available balance (earnings - spending).

            ``total_stocks_in_long``: the number of stocks in long position at
            the end of the simulation.

            ``total_stocks_in_short``: the number of stocks in short position
            at the end of the simulation.

            ``stock_value``: The value of the stock at the end of the
            simulation.

            ``total_value``: The balance plus after closing all the open
            positions.
        """

        # Create Trading Simulation instance
        simulator = TradingSimulation(
            input_data_index=self._input_data.index,
            close_values=close_values,
            max_items_per_transaction=max_items_per_transaction,
            max_investment=max_investment)

        # keep safe the full input and indicator data
        full_ti_data = self._ti_data
        full_input_data = self._input_data

        # Run simulation rounds for the whole period
        for i in range(len(self._input_data.index)):

            # Limit the input and indicator data to this simulation round
            self._input_data = full_input_data[
                full_input_data.index <= full_input_data.index[i]]

            self._ti_data = full_ti_data[
                full_ti_data.index <= full_ti_data.index[i]]

            simulator.runSimulationRound(i_index=i, signal=self.getTiSignal())

        # Restore input and indicator data to full range
        self._ti_data = full_ti_data
        self._input_data = full_input_data

        return simulator.closeSimulation()
