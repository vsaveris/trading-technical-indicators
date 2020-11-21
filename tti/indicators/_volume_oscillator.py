"""
Trading-Technical-Indicators (tti) python library

File name: _volume_oscillator.py
    Implements the Volume Oscillator technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class VolumeOscillator(TechnicalIndicator):
    """
    Volume Oscillator Technical Indicator class implementation.

    Parameters:
        input_data (pandas.DataFrame): The input data.

        long_period (int, default is 5): The past periods to be used for the
            calculation of the long moving average.

        short_period (int, default is 2): The past periods to be used for the
            calculation of the short moving average.

        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        -

    Raises:
        -
    """
    def __init__(self, input_data, long_period=5, short_period=2,
                 fill_missing_values=True):

        # Validate and store if needed, the input parameters
        if isinstance(long_period, int):
            if long_period > 0:
                self._long_period = long_period
            else:
                raise WrongValueForInputParameter(
                    long_period, 'long_period', '>0')
        else:
            raise WrongTypeForInputParameter(
                type(long_period), 'long_period', 'int')

        if isinstance(short_period, int):
            if short_period > 0:
                self._short_period = short_period
            else:
                raise WrongValueForInputParameter(
                    short_period, 'short_period', '>0')
        else:
            raise WrongTypeForInputParameter(
                type(short_period), 'short_period', 'int')

        if self._long_period < self._short_period:
            raise WrongValueForInputParameter(
                long_period, 'long_period ',
                '> short_period [' + str(self._short_period) + ']')

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
                It contains one column, the 'vosc'.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._long_period:
            raise NotEnoughInputData('Volume Oscillator', self._long_period,
                len(self._input_data.index))

        vosc = pd.DataFrame(index=self._input_data.index, columns=['vosc'],
                           data=None, dtype='float64')

        vosc['vosc'] = self._input_data['volume'].rolling(
            window=self._short_period, min_periods=self._short_period,
            center=False, win_type=None, on=None, axis=0, closed=None
        ).mean() - self._input_data['volume'].rolling(
            window=self._long_period, min_periods=self._long_period,
            center=False, win_type=None, on=None, axis=0, closed=None).mean()

        return vosc.round(4)

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
        if len(self._ti_data.index) < 3:
            return TRADE_SIGNALS['hold']

        if (0 < self._ti_data['vosc'].iat[-3] < self._ti_data['vosc'].iat[-2] <
                self._ti_data['vosc'].iat[-1]):
            return TRADE_SIGNALS['buy']

        if (self._ti_data['vosc'].iat[-3] > self._ti_data['vosc'].iat[-2] >
                self._ti_data['vosc'].iat[-1] > 0):
            return TRADE_SIGNALS['sell']

        return TRADE_SIGNALS['hold']
