"""
Trading-Technical-Indicators (tti) python library

File name: _intraday_movement_index.py
    Implements the Intraday Movement Index technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class IntradayMovementIndex(TechnicalIndicator):
    """
    Intraday Movement Index Technical Indicator class implementation.

    Args:
        input_data (pandas.DataFrame): The input data. Required input columns
            are ``open``, ``close``. The index is of type
            ``pandas.DatetimeIndex``.

        period (int, default=14): The past periods to be used for the
            calculation of the indicator.

        fill_missing_values (bool, default=True): If set to True, missing
            values in the input data are being filled.

    Attributes:
        _input_data (pandas.DataFrame): The ``input_data`` after preprocessing.

        _ti_data (pandas.DataFrame): The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains one column, the ``imi``.

        _properties (dict): Indicator properties.

        _calling_instance (str): The name of the class.

    Raises:
        WrongTypeForInputParameter: Input argument has wrong type.
        WrongValueForInputParameter: Unsupported value for input argument.
        NotEnoughInputData: Not enough data for calculating the indicator.
        TypeError: Type error occurred when validating the ``input_data``.
        ValueError: Value error occurred when validating the ``input_data``.
    """
    def __init__(self, input_data, period=14, fill_missing_values=True):

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
            ``pandas.DatetimeIndex``. It contains one column, the ``imi``.

        Raises:
            NotEnoughInputData: Not enough data for calculating the indicator.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._period:
            raise NotEnoughInputData('Intraday Movement Index',
                                     self._period,
                                     len(self._input_data.index))

        imi = pd.DataFrame(index=self._input_data.index, columns=['imi'],
                           data=None, dtype='float64')

        # Calculate Upward Price Change
        upc = self._input_data['close'] - self._input_data['open']
        upc[upc < 0.0] = 0.0

        upc_sum = upc.rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).sum()

        # Calculate Downward Price Change
        dpc = self._input_data['open'] - self._input_data['close']
        dpc[dpc < 0.0] = 0.0

        dpc_sum = dpc.rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).sum()

        imi['imi'] = 100 * upc_sum / (upc_sum + dpc_sum)

        return imi.round(4)

    def getTiSignal(self):
        """
        Calculates and returns the trading signal for the calculated technical
        indicator.

        Returns:
            {('hold', 0), ('buy', -1), ('sell', 1)}: The calculated trading
            signal.
        """

        # Not enough data for calculating trading signal
        if len(self._ti_data.index) < 2:
            return TRADE_SIGNALS['hold']

        # Overbought region
        if self._ti_data['imi'].iat[-2] < 70. < self._ti_data['imi'].iat[-1]:
            return TRADE_SIGNALS['sell']

        # Oversold region
        if self._ti_data['imi'].iat[-2] > 30. > self._ti_data['imi'].iat[-1]:
            return TRADE_SIGNALS['buy']

        return TRADE_SIGNALS['hold']
