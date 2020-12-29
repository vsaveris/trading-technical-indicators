"""
Trading-Technical-Indicators (tti) python library

File name: _ultimate_oscillator.py
    Implements the Ultimate Oscillator technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData


class UltimateOscillator(TechnicalIndicator):
    """
    Ultimate Oscillator Technical Indicator class implementation.

    Args:
        input_data (pandas.DataFrame): The input data. Required input columns
            are ``high``, ``low``, ``close``. The index is of type
            ``pandas.DatetimeIndex``.

        fill_missing_values (bool, default=True): If set to True, missing
            values in the input data are being filled.

    Attributes:
        _input_data (pandas.DataFrame): The ``input_data`` after preprocessing.

        _ti_data (pandas.DataFrame): The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains one column, the ``uosc``.

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
            ``pandas.DatetimeIndex``. It contains one column, the ``uosc``.

        Raises:
            NotEnoughInputData: Not enough data for calculating the indicator.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < 28:
            raise NotEnoughInputData('Ultimate Oscillator', 28,
                                     len(self._input_data.index))

        uosc = pd.DataFrame(index=self._input_data.index, columns=['uosc'],
                            data=None, dtype='float64')

        uosc['true_high'] = pd.concat(
            [self._input_data['high'], self._input_data['close'].shift(1)],
            axis=1).max(axis=1, skipna=False)

        uosc['true_low'] = pd.concat(
            [self._input_data['low'], self._input_data['close'].shift(1)],
            axis=1).min(axis=1, skipna=False)

        uosc['range'] = uosc['true_high'] - uosc['true_low']

        uosc['7_range_sum'] = uosc['range'].rolling(
            window=7, min_periods=7, center=False, win_type=None, on=None,
            axis=0, closed=None).sum()

        uosc['buying_units'] = self._input_data['close'] - uosc['true_low']

        uosc['7_buying_units_sum'] = uosc['buying_units'].rolling(
            window=7, min_periods=7, center=False, win_type=None, on=None,
            axis=0, closed=None).sum()

        uosc['7_bus_rs_division'] = (
                uosc['7_buying_units_sum'] / uosc['7_range_sum']
        )

        uosc['14_range_sum'] = uosc['range'].rolling(
            window=14, min_periods=14, center=False, win_type=None, on=None,
            axis=0, closed=None).sum()

        uosc['14_buying_units_sum'] = uosc['buying_units'].rolling(
            window=14, min_periods=14, center=False, win_type=None, on=None,
            axis=0, closed=None).sum()

        uosc['14_bus_rs_division'] = (
                uosc['14_buying_units_sum'] / uosc['14_range_sum']
        )

        uosc['28_range_sum'] = uosc['range'].rolling(
            window=28, min_periods=28, center=False, win_type=None, on=None,
            axis=0, closed=None).sum()

        uosc['28_buying_units_sum'] = uosc['buying_units'].rolling(
            window=28, min_periods=28, center=False, win_type=None, on=None,
            axis=0, closed=None).sum()

        uosc['28_bus_rs_division'] = (
                uosc['28_buying_units_sum'] / uosc['28_range_sum']
        )

        uosc['uosc'] = 100 * (
                (4 * uosc['7_bus_rs_division']) +
                (2 * uosc['14_bus_rs_division']) + uosc['28_bus_rs_division']
        ) / 7

        return uosc[['uosc']].round(4)

    def getTiSignal(self):
        """
        Calculates and returns the trading signal for the calculated technical
        indicator.

        Returns:
            {('hold', 0), ('buy', -1), ('sell', 1)}: The calculated trading
            signal.
        """

        # Last periods to consider when looking for bullish or bearish
        # divergence
        span_period = 30

        # Not enough data for trading signal
        if len(self._ti_data.index) < span_period:
            return TRADE_SIGNALS['hold']

        # Check if bullish divergence occurs
        close_low_index = self._input_data['close'].iloc[
                          -span_period:].argmin()

        uosc_low_index = self._ti_data['uosc'].iloc[-span_period:].argmin()

        if close_low_index != uosc_low_index:

            # Check if indicator falls below 30 during the bullish period
            if self._ti_data['uosc'].iloc[-span_period:].all() < 30:

                # Buy when indicator makes a highest high during this period
                if self._ti_data['uosc'].iloc[-span_period:-1].all() < \
                        self._ti_data['uosc'].iat[-1]:
                    return TRADE_SIGNALS['buy']

        return TRADE_SIGNALS['hold']
