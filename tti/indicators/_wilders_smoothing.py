"""
Trading-Technical-Indicators (tti) python library

File name: _wilders_smoothing.py
    Implements the Wilders Smoothing technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class WildersSmoothing(TechnicalIndicator):
    """
    Wilders Smoothing Technical Indicator class implementation.

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
                It contains one column, the 'ws'.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._period:
            raise NotEnoughInputData('Wilder\'s Smoothing', self._period,
                                     len(self._input_data.index))

        ws = pd.DataFrame(index=self._input_data.index, columns=['ws'],
                          data=None, dtype='float64')

        # Wilder's Moving Average
        ws['ws'].iat[self._period - 1] = \
            self._input_data['close'].iloc[:self._period].mean()

        for i in range(self._period, len(self._input_data.index)):
            ws['ws'].iat[i] = ws['ws'].iat[i - 1] + (
                    self._input_data['close'].iat[i] - ws['ws'].iat[i - 1]
            ) / self._period

        return ws.round(4)

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

        # Close price goes below indicator
        if ((self._input_data['close'].iat[-2] > self._ti_data['ws'].iat[-2])
                and (self._input_data['close'].iat[-1] <
                     self._ti_data['ws'].iat[-1])):
            return TRADE_SIGNALS['buy']

        # Close price goes above indicator
        if ((self._input_data['close'].iat[-2] < self._ti_data['ws'].iat[-2])
                and (self._input_data['close'].iat[-1] >
                     self._ti_data['ws'].iat[-1])):
            return TRADE_SIGNALS['sell']

        return TRADE_SIGNALS['hold']
