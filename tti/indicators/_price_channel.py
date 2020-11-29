"""
Trading-Technical-Indicators (tti) python library

File name: _price_channel.py
    Implements the Price Channel technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class PriceChannel(TechnicalIndicator):
    """
    Price Channel Technical Indicator class implementation.

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
                It contains two columns, the 'highest_high' and the
                'lowest_low'.
        """

        # Not enough data
        if len(self._input_data.index) < self._period:
            raise NotEnoughInputData('Price Channel', self._period,
                                     len(self._input_data.index))

        pch = pd.DataFrame(index=self._input_data.index,
                           columns=['highest_high', 'lowest_low'],
                           data=None, dtype='float64')

        pch['highest_high'] = self._input_data['high'].rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).max().shift(1)

        pch['lowest_low'] = self._input_data['low'].rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).min().shift(1)

        return pch.round(4)

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

        # Not enough data for calculating trading signal
        if len(self._ti_data.index) < 1:
            return TRADE_SIGNALS['hold']

        # Price goes above highest high
        if self._input_data['close'].iat[-1] > \
                self._ti_data['highest_high'].iat[-1]:
            return TRADE_SIGNALS['sell']

        # Price goes below lowest low
        elif self._input_data['close'].iat[-1] < \
                self._ti_data['lowest_low'].iat[-1]:
            return TRADE_SIGNALS['buy']

        else:
            return TRADE_SIGNALS['hold']
