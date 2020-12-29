"""
Trading-Technical-Indicators (tti) python library

File name: _swing_index.py
    Implements the Swing Index technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS


class SwingIndex(TechnicalIndicator):
    """
    Swing Index Technical Indicator class implementation.

    Args:
        input_data (pandas.DataFrame): The input data. Required input columns
            are ``open``, ``high``, ``low``, ``close``. The index is of type
            ``pandas.DatetimeIndex``.

        fill_missing_values (bool, default=True): If set to True, missing
            values in the input data are being filled.

    Attributes:
        _input_data (pandas.DataFrame): The ``input_data`` after preprocessing.

        _ti_data (pandas.DataFrame): The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains one column, the ``swi``.

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
            ``pandas.DatetimeIndex``. It contains one column, the ``swi``.
        """

        swi = pd.DataFrame(index=self._input_data.index, columns=['swi'],
                           data=None, dtype='float64')

        # Absolute Difference between today's high and yesterday's close
        swi['abs_th_yc_diff'] = (
                self._input_data['high'] - self._input_data['close'].shift(1)
        ).abs()

        # Absolute Difference between today's low and yesterday's close
        swi['abs_tl_yc_diff'] = (
                self._input_data['low'] - self._input_data['close'].shift(1)
        ).abs()

        # Difference between high and low
        swi['th_tl_diff'] = \
            self._input_data['high'] - self._input_data['low']

        # Absolute Difference between yesterday's close and open
        swi['abs_yc_yo_diff'] = (
                self._input_data['close'].shift(1) -
                self._input_data['open'].shift(1)
        ).abs()

        # Difference between today's and yesterday's close
        swi['tc_yc_diff'] = (
                self._input_data['close'] - self._input_data['close'].shift(1)
        )

        # Difference between today's close and open
        swi['tc_to_diff'] = (
                self._input_data['close'] - self._input_data['open']
        )

        # Difference between yesterday's close and open
        swi['yc_yo_diff'] = (
                self._input_data['close'].shift(1) -
                self._input_data['open'].shift(1)
        )

        # Calculate Indicator
        swi['numerator'] = (swi['tc_yc_diff'] + 0.5 * swi['tc_to_diff'] +
                            0.25 * swi['yc_yo_diff'])

        swi['K'] = pd.concat(
            [swi['abs_th_yc_diff'],  swi['abs_tl_yc_diff']], axis=1
        ).max(axis=1)

        swi['R'] = pd.concat([
            swi['abs_th_yc_diff'],  swi['abs_tl_yc_diff'], swi['th_tl_diff']
        ], axis=1).max(axis=1) + 0.25 * swi['abs_yc_yo_diff']

        swi['swi'] = 50 * (swi['numerator'] / swi['R']) * (swi['K'] / 3)
        swi.loc[swi['swi'] > 100.0, ['swi']] = 100.0
        swi.loc[swi['swi'] < -100.0, ['swi']] = -100.0

        return swi[['swi']].round(4)

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

        # SWI raises above zero, short uptrend
        if self._ti_data['swi'].iat[-2] < 0.0 < self._ti_data['swi'].iat[-1]:
            return TRADE_SIGNALS['sell']

        # SWI falls below zero, short downtrend
        if self._ti_data['swi'].iat[-2] > 0.0 > self._ti_data['swi'].iat[-1]:
            return TRADE_SIGNALS['buy']

        return TRADE_SIGNALS['hold']
