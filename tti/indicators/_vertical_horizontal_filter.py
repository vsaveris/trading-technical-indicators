"""
Trading-Technical-Indicators (tti) python library

File name: _vertical_horizontal_filter.py
    Implements the Vertical Horizontal Filter technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ._double_exponential_moving_average import DoubleExponentialMovingAverage
from ._momentum import Momentum
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class VerticalHorizontalFilter(TechnicalIndicator):
    """
    Vertical Horizontal Filter Technical Indicator class implementation.

    Parameters:
        input_data (pandas.DataFrame): The input data.

        period (int, default is 5): The past periods to be used for the
            calculation of the indicator.

        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        -

    Raises:
        -
    """
    def __init__(self, input_data, period=5, fill_missing_values=True):

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

        Parameters:
            -

        Raises:
            -

        Returns:
            pandas.DataFrame: The calculated indicator. Index is of type date.
                It contains one column, the 'vhf'.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._period:
            raise NotEnoughInputData('Vertical Horizontal Filter',
                                     self._period, len(self._input_data.index))

        vhf = pd.DataFrame(index=self._input_data.index, columns=['vhf'],
                           data=None, dtype='float64')

        vhf['highest_close'] = self._input_data['close'].rolling(
                window=self._period, min_periods=self._period, center=False,
                win_type=None, on=None, axis=0, closed=None).max()

        vhf['lowest_close'] = self._input_data['close'].rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).min()

        # Absolute difference between highest_close and lowest_close
        vhf['hc_lc_diff'] = (vhf['highest_close'] - vhf['lowest_close']).abs()

        # Absolute difference of today's close with yesterday's close
        vhf['close_change'] = (self._input_data['close'] -
                               self._input_data['close'].shift(1)).abs()

        vhf['close_change_sum'] = vhf['close_change'].rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).sum()

        vhf['vhf'] = vhf['hc_lc_diff'] / vhf['close_change_sum']

        return vhf[['vhf']].round(4)

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

        # Not enough data for trading signal
        if len(self._input_data.index) < 3:
            return TRADE_SIGNALS['hold']

        # Rising values indicate a trend
        if (self._ti_data['vhf'].iat[-3] < self._ti_data['vhf'].iat[-2] <
                self._ti_data['vhf'].iat[-1]):

            # Not enough data for trading signal
            if len(self._input_data.index) < 5:
                return TRADE_SIGNALS['hold']
            else:
                return DoubleExponentialMovingAverage(
                    self._input_data, period=5).getTiSignal()

        # Falling values indicate a ranging market
        if (self._ti_data['vhf'].iat[-3] > self._ti_data['vhf'].iat[-2] >
                self._ti_data['vhf'].iat[-1]):

            # Not enough data for trading signal
            if len(self._input_data.index) < 12:
                return TRADE_SIGNALS['hold']
            else:
                return Momentum(self._input_data, period=12).getTiSignal()

        return TRADE_SIGNALS['hold']