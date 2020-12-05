"""
Trading-Technical-Indicators (tti) python library

File name: _on_balance_volume.py
    Implements the On Balance Volume technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS


class OnBalanceVolume(TechnicalIndicator):
    """
    On Balance Volume Technical Indicator class implementation.

    Args:
        input_data (pandas.DataFrame): The input data. Required input columns
            are ``close``, ``volume``. The index is of type
            ``pandas.DatetimeIndex``.

        fill_missing_values (bool, default=True): If set to True, missing
            values in the input data are being filled.

    Attributes:
        _input_data (pandas.DataFrame): The ``input_data`` after preprocessing.

        _ti_data (pandas.DataFrame): The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains one column, the ``obv``.

        _properties (dict): Indicator properties.

        _calling_instance (str): The name of the class.

    Raises:
        WrongTypeForInputParameter: Input argument has wrong type.
        WrongValueForInputParameter: Unsupported value for input argument.
        NotEnoughInputData: Not enough data for calculating the indicator.
        TypeError: Type error occurred when validating the ``input_data``.
        ValueError: Value error occurred when validating the ``input_data``.
    """
    def __init__(self, input_data, fill_missing_values=True):

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
            ``pandas.DatetimeIndex``. It contains one column, the ``obv``.
        """

        obv = pd.DataFrame(index=self._input_data.index, columns=['obv'],
                           data=0, dtype='int64')

        obv['obv'][self._input_data['close'] > self._input_data['close'].
            shift(1)] = self._input_data['volume']

        obv['obv'][self._input_data['close'] < self._input_data['close'].
            shift(1)] = -self._input_data['volume']

        obv['obv'] = obv['obv'].cumsum()

        return obv

    def getTiSignal(self):
        """
        Calculates and returns the trading signal for the calculated technical
        indicator.

        Returns:
            {('hold', 0), ('buy', -1), ('sell', 1)}: The calculated trading
            signal.
        """

        # Trading signals on warnings for breakout (upward or downward)
        # 3-days period is used for trend calculation

        # Not enough data for calculating trading signal
        if len(self._ti_data.index) < 3:
            return TRADE_SIGNALS['hold']

        # Warning for a downward breakout
        if self._ti_data['obv'].iat[-3] > self._ti_data['obv'].iat[-2] > \
                self._ti_data['obv'].iat[-1]:
            return TRADE_SIGNALS['buy']

        # Warning for a upward breakout
        elif self._ti_data['obv'].iat[-3] < self._ti_data['obv'].iat[-2] < \
                self._ti_data['obv'].iat[-1]:
            return TRADE_SIGNALS['sell']

        else:
            return TRADE_SIGNALS['hold']
