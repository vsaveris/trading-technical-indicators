"""
Trading-Technical-Indicators (tti) python library

File name: _trading_simulation.py
    Trading simulation class implementation defined under the tti.utils
    package.
"""

import pandas as pd
from ..utils.data_validation import validateInputData
from ..utils.exceptions import WrongTypeForInputParameter, \
    NotValidInputDataForSimulation, WrongValueForInputParameter


class TradingSimulation:
    """
    Trading Simulation class implementation. Provides utilities methods for
    the runSimulation method of the tti.indicators package.

    Args:
        input_data (pandas.DataFrame): The indicator's input data after
            preprocessing.

        ti_data (pandas.DataFrame): The technical Indicator calculated data.

        close_values (pandas.DataFrame): The close prices of the stock, for
            the whole simulation period. Index is of type DateTimeIndex
            with same values as the input to the indicator data. It
            contains one column ``close``.

        max_items_per_transaction (int, default=1): The maximum number of
            stocks to be traded on each ``open_long`` or ``open_short``
            transaction.

        commission (float, default=0.0): Commission for each transaction.

        max_investment(float, default=None): Maximum investment for all the
            opened positions (``short`` and ``long``). If the sum of all
            the opened positions reached the maximum investment, then it is
            not allowed to open a new position. A new position can be
            opened when some balance becomes available from a position
            close. If set to  None, then there is no upper limit for the opened
            positions.

    Attributes:
         _input_data (pandas.DataFrame): The indicator's input data after
            preprocessing.

        _ti_data (pandas.DataFrame): The technical Indicator calculated data.

        _close_values (pandas.DataFrame): The close prices of the stock, for
            the whole simulation period. Index is of type DateTimeIndex
            with same values as the input to the indicator data. It
            contains one column ``close``.

        _max_items_per_transaction (int, default=1): The maximum number of
            stocks to be traded on each ``open_long`` or ``open_short``
            transaction.

        _commission (float, default=0.0): Commission for each transaction.

        _max_investment(float, default=None): Maximum investment for all the
            opened positions (``short`` and ``long``). If the sum of all
            the opened positions reached the maximum investment, then it is
            not allowed to open a new position. A new position can be
            opened when some balance becomes available from a position
            close. If set to  None, then there is no upper limit for the opened
            positions.

        _portfolio (pandas.DataFrame): Simulation portfolio, keeps a track of
            the entered positions during the simulation. Position: ``long``,
            ``short`` or ``none``. Items: Number of stocks. Unit_Price: Price
            of each item when entered the position. Status: ``open``, ``close``
            or none

        _simulation_data (pandas.DataFrame): Dataframe which holds details and
            about the simulation. The index of the dataframe is the whole
            trading period(DateTimeIndex). Columns are:

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
            positions (if they would be closed in this transaction).

        _statistics (dict): Statistics about the simulation. contains the below
            keys:

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

    Raises:
        WrongTypeForInputParameter: Input argument has wrong type.
        WrongValueForInputParameter: Unsupported value for input argument.
        NotValidInputDataForSimulation: Invalid ``close_values`` `passed for
            the simulation.
    """

    def __init__(self, input_data, ti_data, close_values,
                 max_items_per_transaction=1, commission=0.0,
                 max_investment=None):

        self._input_data = input_data
        self._ti_data = ti_data
        self._close_values = close_values
        self._max_items_per_transaction = max_items_per_transaction
        self._commission = commission
        self._max_investment = max_investment

        # Validate input arguments
        self._validateSimulationArguments()

        # Simulation portfolio, keeps a track of the entered positions during
        # the simulation. Position: `long`, `short` or `none`. Items: Number of
        # stocks. Unit_Price: Price of each item when entered the position.
        # Status: `open`, `close` or none
        self._portfolio = pd.DataFrame(
            index=self._input_data.index,
            columns=['position', 'items', 'unit_price', 'status'], data=None)

        # Initialize simulation data structure (DataFrame)
        self._simulation_data = pd.DataFrame(
            index=self._ti_data.index,
            columns=['signal', 'trading_action', 'stocks_in_transaction',
                     'balance', 'stock_value', 'total_value'],
            data=None)

        # Initialize statistics data structure (dict)
        self._statistics = {
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

        # Validate close_values pandas.DataFrame
        try:
            self._close_values = validateInputData(
                input_data=self._close_values, required_columns=['close'],
                indicator_name='TradingSimulation',
                fill_missing_values=True)

        except Exception as e:
            raise NotValidInputDataForSimulation(
                'close_values', str(e).replace('input_data', 'close_values'))

        if not self._close_values.index.equals(self._input_data.index):
            raise NotValidInputDataForSimulation(
                'close_values', 'Index of the `close_values` DataFrame ' +
                                'should be the same as the index of the ' +
                                '`input_data` argument in the indicator\'s ' +
                                'constructor.')

        # Validate _max_items_per_transaction
        if isinstance(self._max_items_per_transaction, int):
            if self._max_items_per_transaction <= 0:
                raise WrongValueForInputParameter(
                    self._max_items_per_transaction,
                    'max_items_per_transaction', '>0')
        else:
            raise WrongTypeForInputParameter(
                type(self._max_items_per_transaction),
                'max_items_per_transaction', 'int')

        # Validate commission
        if isinstance(self._commission, (int, float)):
            if self._commission < 0:
                raise WrongValueForInputParameter(
                    self._commission, 'commission', '>=0')
        else:
            raise WrongTypeForInputParameter(
                type(self._commission), 'commission', 'int or float')

        # Validate max_investment
        if isinstance(self._max_investment, (int, float)):
            if self._max_investment <= 0:
                raise WrongValueForInputParameter(
                    self._max_investment, 'max_investment', '>0')
        elif self._max_investment is None:
            pass
        else:
            raise WrongTypeForInputParameter(
                type(self._max_investment), 'max_investment',
                'int or float or None')

    def _calculateSimulationStatistics(self):
        """
        Calculate simulation statistics, at the end of the simulation.
        """

        self._statistics = {
            'number_of_trading_days': len(self._simulation_data.index),

            'number_of_buy_signals':
                len(self._simulation_data[
                        self._simulation_data['signal'] == 'buy'].index),

            'number_of_ignored_buy_signals':
                len(self._simulation_data[
                        self._simulation_data['signal'] == 'buy' and
                        self._simulation_data['trading_action'] == 'none'].
                    index),

            'number_of_sell_signals':
                len(self._simulation_data[
                        self._simulation_data['signal'] == 'sell'].index),

            'number_of_ignored_sell_signals':
                len(self._simulation_data[
                        self._simulation_data['signal'] == 'sell' and
                        self._simulation_data['trading_action'] == 'none'].
                    index),

            'balance': self._simulation_data['balance'].iat[-1],

            'total_stocks_in_long':
                self._portfolio[
                    self._portfolio['position'] == 'long' and
                    self._portfolio['close'] == 'open']['items'].sum(),

            'total_stocks_in_short':
                self._portfolio[
                    self._portfolio['position'] == 'short' and
                    self._portfolio['close'] == 'open']['items'].sum(),

            'stock_value': self._simulation_data['stock_value'].iat[-1],

            'total_value': self._simulation_data['total_value'].iat[-1]}
