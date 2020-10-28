"""
Trading-Technical-Indicators (tti) python library

File name: _envelopes.py
    Implements the Envelopes technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class Envelopes(TechnicalIndicator):
    """
    Envelopes Technical Indicator class implementation.

    Parameters:
        input_data (pandas.DataFrame): The input data.

        period (int, default is 20): The past periods to be used for the
            calculation of the moving average.

        shift (float, default is 0.10): The shift percentage to be applied.

        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        -

    Raises:
        -
    """
    def __init__(self, input_data, period=20, shift=0.10,
                 fill_missing_values=True):

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

        if isinstance(shift, float):
            if 1.0 > shift > 0.0:
                self._shift = shift
            else:
                raise WrongValueForInputParameter(
                    period, 'shift', '>0.0 and <1.0')
        else:
            raise WrongTypeForInputParameter(
                type(period), 'shift', 'float')

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
                It contains two columns, the 'upper_band' and the 'lower_band'.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._period:
            raise NotEnoughInputData('Envelopes', self._period,
                                     len(self._input_data.index))

        env = pd.DataFrame(index=self._input_data.index,
                           columns=['upper_band', 'lower_band'], data=0,
                           dtype='float64')

        ma = self._input_data.rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).mean()

        env['upper_band'] = (1 + self._shift) * ma
        env['lower_band'] = (1 - self._shift) * ma

        return env.round(4)

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

        # Price goes above upper band
        if self._input_data['close'].iat[-1] > \
                self._ti_data['upper_band'].iat[-1]:
            return TRADE_SIGNALS['sell']

        # Price goes below lower band
        elif self._input_data['close'].iat[-1] < \
                self._ti_data['lower_band'].iat[-1]:
            return TRADE_SIGNALS['buy']

        else:
            return TRADE_SIGNALS['hold']
