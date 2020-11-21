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

    Parameters:
        input_data (pandas.DataFrame): The input data.

        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        -

    Raises:
        -
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

        Parameters:
            -

        Raises:
            -

        Returns:
            pandas.DataFrame: The calculated indicator. Index is of type date.
                It contains one column, the 'uosc'.
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
        Calculates and returns the signal of the technical indicator. The
        Technical Indicator data are taken from an attribute of the parent
        class.

        Parameters:
            -

        Raises:
            -

        Returns:
            tuple (string, integer): The Trading signal. Possible values are
                ('hold', 0), ('buy', -1), ('sell', 1). See TRADE_SIGNALS
                constant in the tti.utils package, constants.py module.
        """

        # Last periods to consider when looking for bullish or bearish
        # divergence
        span_period = 30

        # Not enough data for trading signal
        if len(self._input_data.index) < 28 + span_period:
            return TRADE_SIGNALS['hold']

        # Check if bullish divergence occurs
        close_low_index = self._input_data['close'].iloc[
                          -span_period:].argmin()

        uosc_low_index = self._ti_data['uosc'].iloc[-span_period:].argmin()

        if close_low_index != uosc_low_index:

            # Check if indicator falls below 30 during the bullish period
            if len(self._ti_data['uosc'].iloc[-span_period:]
                   [self._ti_data['uosc'].iloc[-span_period:] < 30].index) > 0:

                # Buy when indicator makes a highest high during this period
                if len(self._ti_data['uosc'].iloc[-span_period:-1]
                       [self._ti_data['uosc'].iloc[-span_period:-1] >
                        self._ti_data['uosc'].iat[-1]].index) == 0:

                    return TRADE_SIGNALS['buy']

        # Check if bearish divergence occurs
        close_high_index = self._input_data['close'].iloc[
                          -span_period:].argmax()

        uosc_high_index = self._ti_data['uosc'].iloc[-span_period:].argmax()

        if close_high_index != uosc_high_index:

            # Check if indicator rises above 50 during the bearish period
            if len(self._ti_data['uosc'].iloc[-span_period:]
                   [self._ti_data['uosc'].iloc[-span_period:] > 50].index) > 0:

                # Sell when indicator makes a lowest low during this period
                if len(self._ti_data['uosc'].iloc[-span_period:-1]
                       [self._ti_data['uosc'].iloc[-span_period:-1] <
                        self._ti_data['uosc'].iat[-1]].index) == 0:

                    return TRADE_SIGNALS['sell']

        if ((len(self._ti_data['uosc'].iloc[-span_period:-1]
                 [self._ti_data['uosc'].iloc[-span_period:-1] > 50]) > 0) and
                (self._ti_data['uosc'].iat[-1] < 45)):
            return TRADE_SIGNALS['sell']

        if self._ti_data['uosc'].iat[-2] < 70 < self._ti_data['uosc'].iat[-1]:
            return TRADE_SIGNALS['sell']

        return TRADE_SIGNALS['hold']
