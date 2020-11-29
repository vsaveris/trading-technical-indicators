"""
Trading-Technical-Indicators (tti) python library

File name: _ease_of_movement.py
    Implements the Ease Of Movement technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class EaseOfMovement(TechnicalIndicator):
    """
    Ease Of Movement Technical Indicator class implementation.

    Parameters:
        input_data (pandas.DataFrame): The input data.

        period (int, default is 40): The past periods to be used for the
            calculation of the moving average.

        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        -

    Raises:
        -
    """
    def __init__(self, input_data, period=40, fill_missing_values=True):

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
                It contains two columns, the 'emv' and the 'emv_ma'.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < max(self._period, 2):
            raise NotEnoughInputData('Ease Of Movement', max(self._period, 2),
                                     len(self._input_data.index))

        emv = pd.DataFrame(index=self._input_data.index,
                           columns=['emv', 'emv_ma'], data=0, dtype='float64')

        midpoint_move = 0.5 * (
                (self._input_data['high'] + self._input_data['low']) -
                (self._input_data['high'].shift(1) +
                 self._input_data['low'].shift(1)))

        box_ratio = self._input_data['volume'] / (
                (self._input_data['high'] - self._input_data['low']) * 10000)

        emv['emv'] = midpoint_move / box_ratio

        emv['emv_ma'] = emv['emv'].rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).mean()

        return emv.round(4)

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
        if len(self._ti_data.index) < 2:
            return TRADE_SIGNALS['hold']

        # EMV-MA crosses above the zero line, buy signal
        if self._ti_data['emv_ma'].iat[-2] < 0.0 < \
                self._ti_data['emv_ma'].iat[-1]:
            return TRADE_SIGNALS['buy']

        # EMV-MA crosses below the zero line, sell signal
        if self._ti_data['emv_ma'].iat[-2] > 0.0 > \
                self._ti_data['emv_ma'].iat[-1]:
            return TRADE_SIGNALS['sell']

        return TRADE_SIGNALS['hold']