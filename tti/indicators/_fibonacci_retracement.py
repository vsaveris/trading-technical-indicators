"""
Trading-Technical-Indicators (tti) python library

File name: _fibonacci_retracement.py
    Implements the Fibonacci Retracement technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS


class FibonacciRetracement(TechnicalIndicator):
    """
    Fibonacci Retracement Technical Indicator class implementation.

    Args:
        input_data (pandas.DataFrame): The input data. Required input column
            is ``close``. The index is of type ``pandas.DatetimeIndex``.

        fill_missing_values (bool, default=True): If set to True, missing
            values in the input data are being filled.

    Attributes:
        _input_data (pandas.DataFrame): The ``input_data`` after preprocessing.

        _ti_data (pandas.DataFrame): The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains five columns, the resistance
            levels ``rl_0.0``,`` rl_23.6``, ``rl_38.2``, ``rl_50.0``,
            ``rl_61.8`` and ``rl_100.0``.

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
            ``pandas.DatetimeIndex``. It contains five columns, the resistance
            levels ``rl_0.0``,`` rl_23.6``, ``rl_38.2``, ``rl_50.0``,
            ``rl_61.8`` and ``rl_100.0``.
        """

        # Calculate max and min for the whole input data
        total_max = self._input_data['close'].max()
        total_min = self._input_data['close'].min()

        max_min_difference = total_max - total_min

        # Retracement levels, only the first six are calculated
        levels_multipliers = [0.0, 0.236, 0.382, 0.50, 0.618, 1.0]

        retracement_levels = [total_max - c * max_min_difference for c in
                              levels_multipliers]

        return pd.DataFrame(index=self._input_data.index,
                            data=[[retracement_levels[i] for i in
                                   range(len(retracement_levels))]] * len(
                                self._input_data.index),
                            columns=['rl_' + str(round(100*i, 1)) for i in
                                     levels_multipliers]).round(4)

    def getTiSignal(self):
        """
        Calculates and returns the trading signal for the calculated technical
        indicator.

        Returns:
            {('hold', 0), ('buy', -1), ('sell', 1)}: The calculated trading
            signal.
        """

        # Not enough data for calculating a trading signal
        if len(self._ti_data.index) < 2:
            return TRADE_SIGNALS['hold']

        # Moves from one support level to another in downward direction
        if self._input_data['close'].iat[-2] > \
                self._ti_data['rl_61.8'].iat[-2] and \
                self._input_data['close'].iat[-1] < \
                self._ti_data['rl_61.8'].iat[-1]:
            return TRADE_SIGNALS['buy']

        if self._input_data['close'].iat[-2] > \
                self._ti_data['rl_50.0'].iat[-2] and \
                self._input_data['close'].iat[-1] < \
                self._ti_data['rl_50.0'].iat[-1]:
            return TRADE_SIGNALS['buy']

        if self._input_data['close'].iat[-2] > \
                self._ti_data['rl_38.2'].iat[-2] and \
                self._input_data['close'].iat[-1] < \
                self._ti_data['rl_38.2'].iat[-1]:
            return TRADE_SIGNALS['buy']

        if self._input_data['close'].iat[-2] > \
                self._ti_data['rl_23.6'].iat[-2] and \
                self._input_data['close'].iat[-1] < \
                self._ti_data['rl_23.6'].iat[-1]:
            return TRADE_SIGNALS['buy']

        # Moves from one support level to another in the upward direction
        if self._input_data['close'].iat[-2] < \
                self._ti_data['rl_61.8'].iat[-2] and \
                self._input_data['close'].iat[-1] > \
                self._ti_data['rl_61.8'].iat[-1]:
            return TRADE_SIGNALS['sell']

        if self._input_data['close'].iat[-2] < \
                self._ti_data['rl_50.0'].iat[-2] and \
                self._input_data['close'].iat[-1] > \
                self._ti_data['rl_50.0'].iat[-1]:
            return TRADE_SIGNALS['sell']

        if self._input_data['close'].iat[-2] < \
                self._ti_data['rl_38.2'].iat[-2] and \
                self._input_data['close'].iat[-1] > \
                self._ti_data['rl_38.2'].iat[-1]:
            return TRADE_SIGNALS['sell']

        if self._input_data['close'].iat[-2] < \
                self._ti_data['rl_23.6'].iat[-2] and \
                self._input_data['close'].iat[-1] > \
                self._ti_data['rl_23.6'].iat[-1]:
            return TRADE_SIGNALS['sell']

        return TRADE_SIGNALS['hold']
