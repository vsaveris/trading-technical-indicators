"""
Trading-Technical-Indicators (tti) python library

File name: _relative_momentum_index.py
    Implements the Relative Momentum Index technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class RelativeMomentumIndex(TechnicalIndicator):
    """
    Relative Momentum Index Technical Indicator class implementation.

    Args:
        input_data (pandas.DataFrame): The input data. Required input column
            is ``close``. The index is of type  ``pandas.DatetimeIndex``.

        period (int, default=8): The past periods to be used for the
            calculation of the indicator.

        momentum_period (int, default=4): The momentum periods to be used for
            the calculation of the indicator.

        fill_missing_values (bool, default=True): If set to True, missing
            values in the input data are being filled.

    Attributes:
        _input_data (pandas.DataFrame): The ``input_data`` after preprocessing.

        _ti_data (pandas.DataFrame): The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains one column, the ``rmi``.

        _properties (dict): Indicator properties.

        _calling_instance (str): The name of the class.

    Raises:
        WrongTypeForInputParameter: Input argument has wrong type.
        WrongValueForInputParameter: Unsupported value for input argument.
        NotEnoughInputData: Not enough data for calculating the indicator.
        TypeError: Type error occurred when validating the ``input_data``.
        ValueError: Value error occurred when validating the ``input_data``.
    """
    def __init__(self, input_data, period=8, momentum_period=4,
                 fill_missing_values=True):

        # Validate and store if needed, the input parameters
        if isinstance(period, int):
            if period > 0:
                self._period = period
            else:
                raise WrongValueForInputParameter(
                    period, 'period', '>0')
        else:
            raise WrongTypeForInputParameter(
                type(period), 'period', 'int')

        if isinstance(momentum_period, int):
            if momentum_period > 0:
                self._momentum_period = momentum_period
            else:
                raise WrongValueForInputParameter(
                    momentum_period, 'momentum_period', '>0')
        else:
            raise WrongTypeForInputParameter(
                type(momentum_period), 'momentum_period', 'int')

        # Control is passing to the parent class
        super().__init__(calling_instance=self.__class__.__name__,
                         input_data=input_data,
                         fill_missing_values=fill_missing_values)

    def _calculateTi(self):
        """
        Calculates the technical indicator for the given input data. The input
        data are taken from an attribute of the parent class.

        Returns:
            pandas.DataFrame: The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains one column, the ``rmi``.

        Raises:
            NotEnoughInputData: Not enough data for calculating the indicator.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._period + self._momentum_period:
            raise NotEnoughInputData('Relative Momentum Index',
                                     self._period + self._momentum_period,
                                     len(self._input_data.index))

        rmi = pd.DataFrame(index=self._input_data.index,
                           columns=['rmi', 'upc', 'dpc', 'smoothed_upc',
                                   'smoothed_dpc'],
                          data=None, dtype='float64')

        # Calculate price change (current close - close momentum periods ago)
        close_price_change = self._input_data['close'] - self._input_data[
            'close'].shift(self._momentum_period)

        # Upward price change
        rmi['upc'][close_price_change > 0] = close_price_change
        rmi['upc'][close_price_change <= 0] = 0

        # Downward price change
        rmi['dpc'][close_price_change < 0] = abs(close_price_change)
        rmi['dpc'][close_price_change >= 0] = 0

        # Wilder's Moving Average for upc and dpc
        rmi['smoothed_upc'].iat[self._period + self._momentum_period - 1] = \
            rmi['upc'].iloc[
            self._momentum_period:self._period + self._momentum_period].mean()

        rmi['smoothed_dpc'].iat[self._period + self._momentum_period - 1] = \
            rmi['dpc'].iloc[
            self._momentum_period:self._period + self._momentum_period].mean()

        for i in range(self._period + self._momentum_period,
                       len(self._input_data.index)):

            rmi['smoothed_upc'].iat[i] = rmi['smoothed_upc'].iat[i - 1] + (
                    rmi['upc'].iat[i] - rmi['smoothed_upc'].iat[i - 1]
            ) / self._period

            rmi['smoothed_dpc'].iat[i] = rmi['smoothed_dpc'].iat[i - 1] + (
                    rmi['dpc'].iat[i] - rmi['smoothed_dpc'].iat[i - 1]
            ) / self._period

        # Calculate indicator
        rmi['rmi'] = 100 * (rmi['smoothed_upc'] / rmi['smoothed_dpc']) / (
                1 + rmi['smoothed_upc'] / rmi['smoothed_dpc'])

        return rmi[['rmi']].round(4)

    def getTiSignal(self):
        """
        Calculates and returns the trading signal for the calculated technical
        indicator.

        Returns:
            {('hold', 0), ('buy', -1), ('sell', 1)}: The calculated trading
            signal.
        """

        # Not enough data for trading signal
        if len(self._ti_data.index) < 2:
            return TRADE_SIGNALS['hold']

        # Overbought region
        if self._ti_data['rmi'].iat[-2] < 70. < self._ti_data['rmi'].iat[-1]:
            return TRADE_SIGNALS['sell']

        # Oversold region
        if self._ti_data['rmi'].iat[-2] > 30. > self._ti_data['rmi'].iat[-1]:
            return TRADE_SIGNALS['buy']

        return TRADE_SIGNALS['hold']
