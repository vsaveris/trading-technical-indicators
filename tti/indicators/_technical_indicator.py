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
from ..utils.exceptions import WrongTypeForInputParameter, \
    NotValidInputDataForSimulation, WrongValueForInputParameter


class TechnicalIndicator(ABC):
    """
    Technical Indicators class implementation. It is used as a parent class for
    each implemented technical indicator. It implements the public API for
    accessing the calculated values, graph and signal of each indicator.

    Parameters:
        calling_instance (str): The name of the calling class.

        input_data (pandas.DataFrame): The input data.

        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        _calling_instance (str): The name of the calling class.

        _properties (dictionary): Indicator properties.

        _input_data (pandas.DataFrame): The input data after preprocessing.

        _ti_data (pandas.DataFrame): Technical Indicator calculated data.

    Raises:
        -
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

        Parameters:
            df (pandas.DataFrame): The input pandas.DataFrame.

            window (int): The size of the rolling window.

            function (function object): The function to be applied.

        Raises:
            -

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

        Parameters:
            -

        Raises:
             -

        Returns:
            pandas.DataFrame: The calculated indicator. Index is of type date.
                It can contain several columns depending the indicator.
        """

        raise NotImplementedError

    @abstractmethod
    def getTiSignal(self):
        """
         Calculates and returns the signal of the technical indicator.

         Parameters:
            -

         Raises:
             -

         Returns:
            tuple (string, integer): The Trading signal. Possible values are
                ('hold', 0), ('buy', -1), ('sell', 1). See TRADE_SIGNALS
                constant in the tti.utils package, constants.py module.
         """

        raise NotImplementedError

    def getTiData(self):
        """
        Returns the Technical Indicator values for the whole period.

        Parameters:
            -

        Raises:
            -

        Returns:
            pandas.DataFrame: The Technical Indicator values.
        """

        return self._ti_data

    def getTiValue(self,  date=None):
        """
        Returns the Technical Indicator value for a given date. If the date
        is None, it returns the most recent entry.

        Parameters:
            date (string, default is None): A date string.

        Raises:
            -

        Returns:
            float: The value of the Technical Indicator for the given date.
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

        Parameters:
            -

        Raises:
            -

        Returns:
            matplotlib object: The generated plot.
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

    def runSimulation(self, close_values, max_pieces_per_buy=1,
                      commission=0.0):
        """
        Executes trading simulation based on the trading signals produced by
        the technical indicator. With a `buy` trading signal a transaction is
        executed considering the input arguments. All the stocks in possession
        are being sold with a `sell` trading signal. When there is no stock in
        possession but a `sell` signal is produced, this signal is being
        ignored.

        Parameters:
            close_values (pandas.DataFrame): The close value of the stock, for
                the whole simulation period. Index is of type DateTimeIndex
                with same values as the input to the indicator data. It
                contains one column `close`.

            max_pieces_per_buy (int, default is 1): The maximum number of
                stocks to be bought at each `buy` signal.

            commission (numeric, default is 0.0): Commission for each `buy` or
                `sell` transaction.

        Raises:
            -

        Returns:
            simulation (pandas.DataFrame): Data frame which holds details about
                the simulation. Index is the whole trading period
                (DateTimeIndex). Columns are:
                `signal`: the signal produced at each day of the simulation
                    period.
                `stocks_in_transaction`: the number of stocks bought or sold in
                    this transaction.
                `stocks_in_possession`: the number of stocks in possession.
                `balance`: the available balance (earnings from selling stocks
                    - spending from buying stocks)
                `total_value`: the balance plus the value of the stocks in
                    possession.

            statistics (dictionary): Statistics about the simulation. It
                contains the below entries:
                `number_of_trading_days`: The number of trading days in the
                    simulation round.
                `number_of_buy_signals`: The number of `buy` signals produced
                    during the simulation period.
                `number_of_sell_signals`: The number of `sell` signals produced
                    during the simulation period.
                `number_of_ignored_sell_signals`: The number of `sell` signals
                    ignored because they were not any stocks in possession.
                `balance`: The final balance (earnings from selling stocks
                    - spending from buying stocks)
                `stocks_in_possession`: The stocks in possession at the end of
                    the simulation.
                `stock_value`: The value of the stock at the end of the
                    simulation.
                `total_value`: The balance plus the value of the stocks in
                    possession at the end of the simulation.
        """

        # Validate input arguments
        # Validate close_values pandas.DataFrame
        try:
            close_values = validateInputData(input_data=close_values,
                required_columns=['close'], indicator_name='Simulation - ' +
                self._calling_instance, fill_missing_values=True)

        except Exception as e:
            raise NotValidInputDataForSimulation('close_values',
                str(e).replace('input_data', 'close_values'))

        if not close_values.index.equals(self._input_data.index):
            raise NotValidInputDataForSimulation('close_values', 'Index of ' +
                'the `close_values` DataFrame should be the same as the ' +
                'index of the `input_data` argument in the indicator\'s '
                'constructor.')

        # Validate max_pieces_per_buy
        if isinstance(max_pieces_per_buy, int):
            if max_pieces_per_buy <= 0:
                raise WrongValueForInputParameter(max_pieces_per_buy,
                    'max_pieces_per_buy', '>0')
        else:
            raise WrongTypeForInputParameter(type(max_pieces_per_buy),
                'max_pieces_per_buy', 'int')

        # Validate commission
        if isinstance(commission, (int, float)):
            if commission < 0:
                raise WrongValueForInputParameter(commission,
                    'commission', '>=0')
        else:
            raise WrongTypeForInputParameter(type(commission),
                'commission', 'int or float')

        # Initialize statistics
        statistics = {'number_of_trading_days': 0, 'number_of_buy_signals': 0,
            'number_of_sell_signals': 0, 'number_of_ignored_sell_signals': 0,
            'balance': 0.0, 'stocks_in_possession': 0, 'stock_value': 0.0,
            'total_value': 0.0}

        # Initialize simulation results data frame
        simulation = pd.DataFrame(index=self._ti_data.index, columns=['signal',
            'stocks_in_transaction', 'stocks_in_possession', 'balance',
            'total_value'], data=None)

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

            simulation['signal'].iat[i] = self.getTiSignal()

            # If `buy` signal, then buy stocks at `close` price
            if simulation['signal'].iat[i][0] == 'buy':
                statistics['number_of_buy_signals'] += 1

                simulation['stocks_in_transaction'].iat[i] = max_pieces_per_buy

                if i != 0:
                    simulation['stocks_in_possession'].iat[i] = \
                        simulation['stocks_in_possession'].iat[i-1] + \
                        simulation['stocks_in_transaction'].iat[i]

                    simulation['balance'].iat[i] = \
                        simulation['balance'].iat[i-1] - \
                        simulation['stocks_in_transaction'].iat[i] * \
                        close_values['close'].iat[i] - commission

                else:
                    simulation['stocks_in_possession'].iat[i] = \
                        simulation['stocks_in_transaction'].iat[i]

                    simulation['balance'].iat[i] = \
                        - simulation['stocks_in_transaction'].iat[i] * \
                        close_values['close'].iat[i] - commission

                simulation['total_value'].iat[i] = \
                    simulation['balance'].iat[i] + \
                    simulation['stocks_in_possession'].iat[i] * \
                    close_values['close'].iat[i]

            # If `sell` signal, then sell all stocks at `close` price
            elif simulation['signal'].iat[i][0] == 'sell':
                statistics['number_of_sell_signals'] += 1

                # Sell signal ignored, first day of simulation
                if i == 0:
                    statistics['number_of_ignored_sell_signals'] += 1

                    simulation['stocks_in_transaction'].iat[i] = 0
                    simulation['stocks_in_possession'].iat[i] = 0
                    simulation['balance'].iat[i] = 0
                    simulation['total_value'].iat[i] = 0

                # Sell signal ignored, since no stocks in possession
                elif simulation['stocks_in_possession'].iat[i-1] == 0:
                    statistics['number_of_ignored_sell_signals'] += 1

                    simulation['stocks_in_transaction'].iat[i] = 0
                    simulation['stocks_in_possession'].iat[i] = 0
                    simulation['balance'].iat[i] = \
                        simulation['balance'].iat[i-1]
                    simulation['total_value'].iat[i] = \
                        simulation['total_value'].iat[i-1]

                else:
                    simulation['stocks_in_transaction'].iat[i] = \
                        simulation['stocks_in_possession'].iat[i-1]

                    simulation['stocks_in_possession'].iat[i] = 0

                    simulation['balance'].iat[i] = \
                        simulation['balance'].iat[i - 1] + \
                        simulation['stocks_in_transaction'].iat[i] * \
                        close_values['close'].iat[i] - commission

                    simulation['total_value'].iat[i] = \
                        simulation['balance'].iat[i]

            # If `hold` signal, then do nothing
            else:
                if i == 0:
                    simulation['stocks_in_transaction'].iat[i] = 0
                    simulation['stocks_in_possession'].iat[i] = 0
                    simulation['balance'].iat[i] = 0
                    simulation['total_value'].iat[i] = 0
                else:
                    simulation['stocks_in_transaction'].iat[i] = 0
                    simulation['stocks_in_possession'].iat[i] = \
                        simulation['stocks_in_possession'].iat[i - 1]
                    simulation['balance'].iat[i] = \
                        simulation['balance'].iat[i - 1]
                    simulation['total_value'].iat[i] = \
                        simulation['balance'].iat[i] + \
                        simulation['stocks_in_possession'].iat[i] * \
                        close_values['close'].iat[i]

        # Update statistics
        statistics['number_of_trading_days'] = len(self._ti_data.index)
        statistics['balance'] = simulation['balance'].iat[-1].round(2)
        statistics['stocks_in_possession'] = \
            simulation['stocks_in_possession'].iat[-1]
        statistics['stock_value'] = close_values['close'].iat[-1]
        statistics['total_value'] = simulation['total_value'].iat[-1].round(2)

        # Restore input and indicator data to full range
        self._ti_data = full_ti_data
        self._input_data = full_input_data

        return simulation, statistics
