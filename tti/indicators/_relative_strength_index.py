"""
Trading-Technical-Indicators (tti) python library

File name: _relative_strength_index.py
    Implements the Relative Strength Index technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class RelativeStrengthIndex(TechnicalIndicator):
    """
    Relative Strength Index Technical Indicator class implementation.

    Parameters:
        input_data (pandas.DataFrame): The input data.

        period (int, default is 14): The past periods to be used for the
            calculation of the indicator. Popular values are 14, 9 and 25.

        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        -

    Raises:
        -
    """
    def __init__(self, input_data, period=14, fill_missing_values=True):

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
                It contains one column 'rsi'.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._period + 1:
            raise NotEnoughInputData('Relative Strength Index',
                                     self._period + 1,
                                     len(self._input_data.index))

        rsi = pd.DataFrame(data=None, index=self._input_data.index,
                           columns=['rsi'])

        # Calculate Upward Price Change
        upc = pd.DataFrame(data=None, index=self._input_data.index,
                           columns=['upc', 'smoothed_upc'])

        upc['upc'] = self._input_data.rolling(
            window=2, min_periods=2, center=False, win_type=None, on=None,
            axis=0, closed=None).apply(
            lambda x: x[-1] - x[-2] if x[-1] > x[-2] else 0.0).round(4)

        upc['smoothed_upc'].iat[self._period] = \
            upc['upc'].iloc[:self._period + 1].mean()

        for i in range(self._period + 1, len(self._input_data.index)):
            upc['smoothed_upc'].iat[i] = round(
                upc['smoothed_upc'].iat[i - 1] +
                (upc['upc'].iat[i] - upc['smoothed_upc'].iat[i - 1]
                 ) / self._period, 4)

        # Calculate Downward Price Change
        dpc = pd.DataFrame(data=None, index=self._input_data.index,
                           columns=['dpc', 'smoothed_dpc'])

        dpc['dpc'] = self._input_data.rolling(
            window=2, min_periods=2, center=False, win_type=None, on=None,
            axis=0, closed=None).apply(
            lambda x: x[-2] - x[-1] if x[-1] < x[-2] else 0.0).round(4)

        dpc['smoothed_dpc'].iat[self._period] = \
            dpc['dpc'].iloc[:self._period + 1].mean()

        for i in range(self._period + 1, len(self._input_data.index)):
            dpc['smoothed_dpc'].iat[i] = round(
                dpc['smoothed_dpc'].iat[i - 1] +
                (dpc['dpc'].iat[i] - dpc['smoothed_dpc'].iat[i - 1]
                 ) / self._period, 4)

        rsi['rsi'] = \
            100.0 - \
            (100.0 / ((upc['smoothed_upc'] / dpc['smoothed_dpc']) + 1.0))

        return rsi

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

        # Overbought region
        if self._ti_data['rsi'].iat[-2] < 70. < self._ti_data['rsi'].iat[-1]:
            return TRADE_SIGNALS['sell']

        # Oversold region
        if self._ti_data['rsi'].iat[-2] > 30. > self._ti_data['rsi'].iat[-1]:
            return TRADE_SIGNALS['buy']

        return TRADE_SIGNALS['hold']
