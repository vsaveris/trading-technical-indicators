"""
Trading-Technical-Indicators (tti) python library

File name: _typical_price.py
    Implements the Typical Price technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class TypicalPrice(TechnicalIndicator):
    """
    Typical Price Technical Indicator class implementation.

    Parameters:
        input_data (pandas.DataFrame): The input data.

        period (int, default is 200): The past periods to be used for the
            calculation of the moving average in trading signal.

        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        -

    Raises:
        -
    """
    def __init__(self, input_data, period=200, fill_missing_values=True):

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
                It contains one column, the 'tp'.
        """

        tp = pd.DataFrame(index=self._input_data.index, columns=['tp'],
                          data=self._input_data.mean(axis=1), dtype='float64')

        return tp.round(4)

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
        if len(self._input_data.index) < self._period:
            return TRADE_SIGNALS['hold']

        # Calculate moving average of the close prices
        ma = self._input_data.rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).mean()

        # Indicator goes below Moving Average
        if ((self._ti_data['tp'].iat[-2] > ma.iat[-2, 0]) and
                (self._ti_data['tp'].iat[-1] < ma.iat[-1, 0])):
            return TRADE_SIGNALS['sell']

        # Indicator goes above Moving Average
        if ((self._ti_data['tp'].iat[-2] < ma.iat[-2, 0]) and
                (self._ti_data['tp'].iat[-1] > ma.iat[-1, 0])):
            return TRADE_SIGNALS['buy']

        return TRADE_SIGNALS['hold']
