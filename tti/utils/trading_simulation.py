"""
Trading-Technical-Indicators (tti) python library

File name: trading_simulation.py
    Trading simulation class implementation defined under the tti.utils
    package.
"""

import pandas as pd
import numpy as np
from ..utils.data_validation import validateInputData
from ..utils.exceptions import WrongTypeForInputParameter, \
    NotValidInputDataForSimulation, WrongValueForInputParameter


class TradingSimulation:
    """
    Trading Simulation class implementation. Provides utilities methods for
    the runSimulation method of the tti.indicators package.

    Args:
        input_data_index (pandas.DateTimeIndex): The indicator's input data
            index. Is used for validating that the close values DataFrame
            includes data for the whole simulation period.

        close_values (pandas.DataFrame): The close prices of the stock, for
            the whole simulation period. Index is of type DateTimeIndex
            with same values as the input to the indicator data. It
            contains one column ``close``.

        max_exposure(float, default=None): Maximum allowed exposure for all the
            opened positions (``short`` and ``long``). If the exposure reaches
            this threshold, no further positions are being opened. A new
            position can be opened again only when exposure reduces through a
            position close. If set to None, then there is no upper limit for
            the opened positions (exposure). When a new ``long`` position is
            opened, exposure is increased by the ``stock_price``. When a
            ``short`` position is opened, exposure is increased by the
            ``short_exposure_factor * stock_price``. Values >0.0 or None are
            supported.

        short_exposure_factor (float, default=1.5): The exposure factor when
            a new ``short`` position is opened. Usually is above 1.0 and it
            is used as security when a short position is opened. Values >=1.0
            are supported.

    Attributes:
         _input_data_index (pandas.DateTimeIndex): The indicator's input data
            index. Is used for validating that the close values DataFrame
            includes data for the whole simulation period.

        _close_values (numpy.ndarray): The close prices of the stock, for
            the whole simulation period.

        _max_exposure(float, default=None): Maximum allowed exposure for all
            the opened positions (``short`` and ``long``). If the exposure
            reaches this threshold, no further positions are being opened. A
            new position can be opened again only when exposure reduces through
            a position close. If set to None, then there is no upper limit for
            the opened positions (exposure). When a new ``long`` position is
            opened, exposure is increased by the ``stock_price``. When a
            ``short`` position is opened, exposure is increased by the
            ``short_exposure_factor * stock_price``. Values >0.0 or None are
            supported.

        _short_exposure_factor (float, default=1.5): The exposure factor when
            a new ``short`` position is opened. Usually is above 1.0 and it
            is used as security when a short position is opened. Values >=1.0
            are supported.

        _portfolio (pandas.DataFrame): Simulation portfolio, keeps a track of
            the entered positions during the simulation. Position: ``long``,
            ``short`` or ``none``. Status: ``open``, ``close`` or none.
            Exposure: ``stock_price`` when position is ``long``, and
            ``short_exposure_factor * stock_price`` when position is ``short``.

        _simulation_data (pandas.DataFrame): Dataframe which holds details and
            about the simulation. The index of the dataframe is the whole
            trading period(DateTimeIndex). Columns are:

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

        _statistics (dict): Statistics about the simulation. contains the below
            keys:

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
        NotValidInputDataForSimulation: Invalid ``close_values`` `passed for
            the simulation.
    """

    def __init__(self, input_data_index, close_values, max_exposure=None,
                 short_exposure_factor=1.5):

        self._input_data_index = input_data_index
        self._close_values = close_values
        self._max_exposure = max_exposure
        self._short_exposure_factor = short_exposure_factor

        # Validate input arguments
        self._validateSimulationArguments()

        # Simulation portfolio, keeps a track of the entered positions during
        # the simulation. Position: `long`, `short` or `none`. Status: `open`,
        # `close` or none. Exposure: stock_price when position is long, and
        # short_exposure_factor * stock_price when position is short. Use
        # numpy array improved performance.
        # Columns are:
        #   position: 0.0 is None, 1.0 is short, 2.0 is long
        #   status: 0.0 is None, 1.0 is open, 2.0 is closed
        #   exposure: float indicating the exposure value
        self._portfolio = np.zeros(shape=(len(self._input_data_index), 3),
                                   dtype=np.float64)

        # Change type to numpy array for better performance
        self._close_values = self._close_values.to_numpy(dtype=np.float64,
                                                         copy=True)

        # Initialize simulation data structure (DataFrame)
        self._simulation_data = pd.DataFrame(
            index=self._input_data_index,
            columns=['signal', 'open_trading_action', 'stock_value',
                     'exposure', 'portfolio_value', 'earnings', 'balance'
                     ],
            data=None)

        # Initialize statistics data structure (dict)
        self._statistics = {
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

    def _validateSimulationArguments(self):
        """
        Validates the input arguments passed in the constructor. input_data and
        ti_data are already validated by the tti.indicators package.

        Raises:
            WrongTypeForInputParameter: Input argument has wrong type.
            WrongValueForInputParameter: Unsupported value for input argument.
            NotValidInputDataForSimulation: Invalid ``close_values`` `passed
                for the simulation.
        """

        # Validate input_data_index that is an index
        if not isinstance(self._input_data_index, pd.DatetimeIndex):
            raise NotValidInputDataForSimulation(
                'input_data_index', 'input_data_index should be of type ' +
                                    'pandas.DatetimeIndex but type ' +
                                    str(type(self._input_data_index)) +
                                    ' found.')

        # Sort data
        self._input_data_index = self._input_data_index.sort_values(
            ascending=True)

        # Validate close_values pandas.DataFrame
        try:
            self._close_values = validateInputData(
                input_data=self._close_values, required_columns=['close'],
                indicator_name='TradingSimulation',
                fill_missing_values=True)

        except Exception as e:
            raise NotValidInputDataForSimulation(
                'close_values', str(e).replace('input_data', 'close_values'))

        if not self._close_values.index.equals(self._input_data_index):
            raise NotValidInputDataForSimulation(
                'close_values', 'Index of the `close_values` DataFrame ' +
                                'should be the same as the index of the ' +
                                '`input_data` argument in the indicator\'s ' +
                                'constructor.')

        # Validate max_exposure
        if isinstance(self._max_exposure, (int, float)):
            if self._max_exposure <= 0:
                raise WrongValueForInputParameter(
                    self._max_exposure, 'max_exposure', '>0 or None')
        elif self._max_exposure is None:
            pass
        else:
            raise WrongTypeForInputParameter(
                type(self._max_exposure), 'max_exposure',
                'int or float or None')

        # Validate short_exposure_factor
        if isinstance(self._short_exposure_factor, (int, float)):
            if self._short_exposure_factor < 1.0:
                raise WrongValueForInputParameter(
                    self._short_exposure_factor, 'short_exposure_factor',
                    '>=1.0')
        else:
            raise WrongTypeForInputParameter(
                type(self._short_exposure_factor), 'short_exposure_factor',
                'int or float')

    def _calculateSimulationStatistics(self):
        """
        Calculate simulation statistics, at the end of the simulation.
        """

        # Simulation rounds which have been executed till now
        executed_simulation_rounds = len(
            self._simulation_data.dropna(subset=['signal'],
                                         inplace=False).index)

        self._statistics = {
            'number_of_trading_days': executed_simulation_rounds,

            'number_of_buy_signals':
                len(self._simulation_data[
                        self._simulation_data['signal'] == 'buy'].index),

            'number_of_ignored_buy_signals':
                len(self._simulation_data[
                    (self._simulation_data['signal'] == 'buy') &
                    (self._simulation_data['open_trading_action'] == 'none')].
                    index),

            'number_of_sell_signals':
                len(self._simulation_data[
                        self._simulation_data['signal'] == 'sell'].index),

            'number_of_ignored_sell_signals':
                len(self._simulation_data[
                    (self._simulation_data['signal'] == 'sell') &
                    (self._simulation_data['open_trading_action'] == 'none')]
                    .index),

            'last_stock_value':  0.0 if executed_simulation_rounds == 0
                else self._simulation_data['stock_value'].iat[
                    executed_simulation_rounds - 1].round(2),

            'last_exposure': 0.0 if executed_simulation_rounds == 0
                else round(self._simulation_data['exposure'].iat[
                    executed_simulation_rounds - 1], 2),

            'last_open_long_positions': np.count_nonzero(
                self._portfolio[
                    (self._portfolio[:, 0] == 2.0) &
                    (self._portfolio[:, 1] == 1.0), 0]),

            'last_open_short_positions': np.count_nonzero(
                self._portfolio[
                    (self._portfolio[:, 0] == 1.0) &
                    (self._portfolio[:, 1] == 1.0), 0]),

            'last_portfolio_value': 0.0 if executed_simulation_rounds == 0
                else round(self._simulation_data['portfolio_value'].iat[
                    executed_simulation_rounds - 1], 2),

            'last_earnings': 0.0 if executed_simulation_rounds == 0
                else round(self._simulation_data['earnings'].iat[
                    executed_simulation_rounds - 1], 2),

            'final_balance': 0.0 if executed_simulation_rounds == 0
                else round(self._simulation_data['balance'].iat[
                    executed_simulation_rounds - 1], 2)
        }

    def _calculatePortfolioValue(self, i_index):
        """
        Calculate the portfolio value (for the opened positions).

        Args:
            i_index (int): The integer index of the current simulation round.
                Refers to the index of all the DataFrames used in the
                simulation.

        Returns:
            float: The portfolio value.
        """

        open_long_positions = np.count_nonzero(
            self._portfolio[
                (self._portfolio[:, 0] == 2.0) &
                (self._portfolio[:, 1] == 1.0), 0])

        open_short_positions = np.count_nonzero(
            self._portfolio[
                (self._portfolio[:, 0] == 1.0) &
                (self._portfolio[:, 1] == 1.0), 0])

        return self._close_values[i_index, 0] * (
                open_long_positions - open_short_positions)

    def _closeOpenPositions(self, i_index):
        """
        Closes the opened positions existing in portfolio.

        Args:
            i_index (int): The integer index of the current simulation round.
                Refers to the index of all the DataFrames used in the
                simulation.

        Returns:
            float: The earnings of the transactions executed.

            float: The closed exposure.
        """

        # Close only positions that bring earnings

        long_to_be_closed = np.count_nonzero(self._portfolio[
            (self._portfolio[:, 1] == 1.0) &
            (self._portfolio[:, 0] == 2.0) &
            (self._portfolio[:, 2] < self._close_values[i_index, 0]), 0])

        short_to_be_closed = np.count_nonzero(self._portfolio[
            (self._portfolio[:, 1] == 1.0) &
            (self._portfolio[:, 0] == 1.0) &
            (self._portfolio[:, 2] > (
                    self._short_exposure_factor *
                    self._close_values[i_index, 0])), 0])

        long_closed_exposure = np.sum(self._portfolio[
            (self._portfolio[:, 1] == 1.0) &
            (self._portfolio[:, 0] == 2.0) &
            (self._portfolio[:, 2] < self._close_values[i_index, 0]), 2])

        short_closed_exposure = np.sum(self._portfolio[
            (self._portfolio[:, 1] == 1.0) &
            (self._portfolio[:, 0] == 1.0) &
            (self._portfolio[:, 2] > (
                    self._short_exposure_factor *
                    self._close_values[i_index, 0])), 2])

        # Calculate earnings and closed_exposure

        earnings = (
            long_to_be_closed * self._close_values[i_index, 0] -
            long_closed_exposure) + (
                (short_closed_exposure / self._short_exposure_factor) -
                short_to_be_closed * self._close_values[i_index, 0])

        closed_exposure = long_closed_exposure + short_closed_exposure

        # Register close actions
        self._portfolio[
            (self._portfolio[:, 1] == 1.0) &
            (self._portfolio[:, 0] == 2.0) &
            (self._portfolio[:, 2] <
            self._close_values[i_index, 0]), 1] = 2.0

        self._portfolio[
            (self._portfolio[:, 1] == 1.0) &
            (self._portfolio[:, 0] == 1.0) &
            (self._portfolio[:, 2] >
                (self._short_exposure_factor *
                self._close_values[i_index, 0])), 1] = 2.0

        # create simulation data row, set only the 'exposure' and
        # earnings, rest of the row will be created in the
        # processSignal method
        self._simulation_data['exposure'].iat[i_index] = \
            self._simulation_data['exposure'].iat[i_index - 1] - \
            closed_exposure

        self._simulation_data['earnings'].iat[i_index] = \
            self._simulation_data['earnings'].iat[i_index - 1] + earnings

        return earnings, closed_exposure

    def _processSignal(self, i_index, signal):
        """
        Process a trading signal.

        Args:
            i_index (int): The integer index of the current simulation round.
                Refers to the index of all the DataFrames used in the
                simulation.

            signal ({('hold', 0), ('buy', -1), ('sell', 1)} or None): The
                signal to be considered in this simulation round.
        """

        if signal[0] == 'hold':

            # Add portfolio row, columns: 'position', 'status', 'exposure'
            self._portfolio[i_index, :] = [0.0, 0.0, 0.0]

            portfolio_value = self._calculatePortfolioValue(i_index)

            # Add simulation data row, columns: 'signal',
            # 'open_trading_action', 'stock_value', 'exposure',
            # 'portfolio_value', 'earnings', 'balance'. Note that 'earnings'
            # and 'exposure' had been already updated in runSimulationRound
            self._simulation_data.iloc[i_index, :] = [
                'hold',
                'none',
                self._close_values[i_index, 0],
                self._simulation_data['exposure'].iat[i_index],
                portfolio_value,
                self._simulation_data['earnings'].iat[i_index],
                portfolio_value +
                self._simulation_data['earnings'].iat[i_index]
            ]

        elif signal[0] == 'buy':

            # Maximum exposure reached
            if self._max_exposure is not None and self._max_exposure < (
                    self._simulation_data['exposure'].iat[i_index] +
                    self._close_values[i_index, 0]):

                # Add portfolio row, columns: 'position', 'status', 'exposure'
                self._portfolio[i_index, :] = [0.0, 0.0, 0.0]

                portfolio_value = self._calculatePortfolioValue(i_index)

                # Add simulation data row, columns: 'signal',
                # 'open_trading_action', 'stock_value', 'exposure',
                # 'portfolio_value', 'earnings', 'balance'. Note that
                # 'earnings' and 'exposure' had been already updated in
                # runSimulationRound
                self._simulation_data.iloc[i_index, :] = [
                    'buy',
                    'none',
                    self._close_values[i_index, 0],
                    self._simulation_data['exposure'].iat[i_index],
                    portfolio_value,
                    self._simulation_data['earnings'].iat[i_index],
                    portfolio_value +
                    self._simulation_data['earnings'].iat[i_index]
                ]

            # Open long position
            else:

                # Add portfolio row, columns: 'position', 'status', 'exposure'
                self._portfolio[i_index, :] = [
                    2.0, 1.0, self._close_values[i_index, 0]]

                portfolio_value = self._calculatePortfolioValue(i_index)

                # Add simulation data row, columns: 'signal',
                # 'open_trading_action', 'stock_value', 'exposure',
                # 'portfolio_value', 'earnings', 'balance'. Note that
                # 'earnings' and 'exposure' had been already updated in
                # runSimulationRound
                self._simulation_data.iloc[i_index, :] = [
                    'buy',
                    'long',
                    self._close_values[i_index, 0],
                    self._simulation_data['exposure'].iat[i_index] +
                    self._close_values[i_index, 0],
                    portfolio_value,
                    self._simulation_data['earnings'].iat[i_index],
                    portfolio_value +
                    self._simulation_data['earnings'].iat[i_index]
                ]

        elif signal[0] == 'sell':

            # Maximum exposure reached
            if self._max_exposure is not None and self._max_exposure < (
                    self._simulation_data['exposure'].iat[i_index] +
                    self._short_exposure_factor *
                    self._close_values[i_index, 0]):

                # Add portfolio row, columns: 'position', 'status', 'exposure'
                self._portfolio[i_index, :] = [0.0, 0.0, 0.0]

                portfolio_value = self._calculatePortfolioValue(i_index)

                # Add simulation data row, columns: 'signal',
                # 'open_trading_action', 'stock_value', 'exposure',
                # 'portfolio_value', 'earnings', 'balance'. Note that
                # 'earnings' and 'exposure' had been already updated in
                # runSimulationRound
                self._simulation_data.iloc[i_index, :] = [
                    'sell',
                    'none',
                    self._close_values[i_index, 0],
                    self._simulation_data['exposure'].iat[i_index],
                    portfolio_value,
                    self._simulation_data['earnings'].iat[i_index],
                    portfolio_value +
                    self._simulation_data['earnings'].iat[i_index]
                ]

            # Open short position
            else:

                # Add portfolio row, columns: 'position', 'status', 'exposure'
                self._portfolio[i_index, :] = [
                    1.0, 1.0,
                    self._short_exposure_factor *
                    self._close_values[i_index, 0]]

                portfolio_value = self._calculatePortfolioValue(i_index)

                # Add simulation data row, columns: 'signal',
                # 'open_trading_action', 'stock_value', 'exposure',
                # 'portfolio_value', 'earnings', 'balance'. Note that
                # 'earnings' and 'exposure' had been already updated in
                # runSimulationRound
                self._simulation_data.iloc[i_index, :] = [
                    'sell',
                    'short',
                    self._close_values[i_index, 0],
                    self._simulation_data['exposure'].iat[i_index] +
                    self._short_exposure_factor *
                    self._close_values[i_index, 0],
                    portfolio_value,
                    self._simulation_data['earnings'].iat[i_index],
                    portfolio_value +
                    self._simulation_data['earnings'].iat[i_index]
                ]

    def runSimulationRound(self, i_index, signal):
        """
        Executes a simulation round based on given signal.

        Args:
            i_index (int): The integer index of the current simulation round.
                Refers to the index of all the DataFrames used in the
                simulation.

            signal ({('hold', 0), ('buy', -1), ('sell', 1)} or None): The
                signal to be considered in this simulation round.
        """

        # Just initializations at the first day
        # Columns for the simulation data: 'signal', 'open_trading_action',
        # 'stock_value', 'exposure', 'portfolio_value', 'earnings', 'balance'
        if i_index == 0:
            self._simulation_data.iloc[0, :] = [
                signal[0], 'none', self._close_values[0, 0], 0.0,
                0.0, 0.0, 0.0]

            # Columns for the portfolio: 'position', 'status', 'exposure'
            self._portfolio[0, :] = [0.0, 0.0, 0.0]

        else:
            # First check if any open position can be closed
            self._closeOpenPositions(i_index=i_index)

            self._processSignal(i_index, signal)

    def closeSimulation(self):
        """
        Closes this simulation and returns simulation data and statistics.

        Returns:
            (pandas.DataFrame, dict): Dataframe which holds details and
            dictionary which holds statistics about the simulation.

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
        """

        self._calculateSimulationStatistics()

        return self._simulation_data, self._statistics
