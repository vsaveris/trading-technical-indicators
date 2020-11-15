"""
Trading-Technical-Indicators (tti) python library

File name: _qstick.py
    Implements the Qstick technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class Qstick(TechnicalIndicator):
    """
    Qstick Technical Indicator class implementation.

    Parameters:
        input_data (pandas.DataFrame): The input data.

        period (int, default is 8): The past periods to be used for the
            calculation of the indicator.

        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        -

    Raises:
        -
    """
    def __init__(self, input_data, period=8, fill_missing_values=True):

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
                It contains one column, the 'qstick'.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._period:
            raise NotEnoughInputData('Qstick', self._period,
                                     len(self._input_data.index))

        qstick = pd.DataFrame(index=self._input_data.index, columns=['qstick'],
                            data=None, dtype='float64')

        qstick['qstick'] = \
            (self._input_data['close'] - self._input_data['open']).rolling(
                window=self._period, min_periods=self._period, center=False,
                win_type=None, on=None, axis=0, closed=None).sum(
            ) / self._period

        return qstick.round(4)

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
        if len(self._input_data) < 4:
            return TRADE_SIGNALS['hold']

        # Signals based on Crossovers (zero line)
        if (self._ti_data['qstick'].iat[-4] <
                self._ti_data['qstick'].iat[-3] <
                0 <
                self._ti_data['qstick'].iat[-2] <
                self._ti_data['qstick'].iat[-1]):
            return TRADE_SIGNALS['buy']

        if (self._ti_data['qstick'].iat[-4] >
                self._ti_data['qstick'].iat[-3] >
                0 >
                self._ti_data['qstick'].iat[-2] >
                self._ti_data['qstick'].iat[-1]):
            return TRADE_SIGNALS['sell']

        return TRADE_SIGNALS['hold']
