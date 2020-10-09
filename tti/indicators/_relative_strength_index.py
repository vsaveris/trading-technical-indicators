"""
Trading-Technical-Indicators (tti) python library

File name: _relative_strength_index.py
    Implements the Relative Strength Index technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS


class RelativeStrengthIndex(TechnicalIndicator):
    """
    Relative Strength Index Technical Indicator class implementation.

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
                It contains one column 'rsi'.
        """

        rsi = pd.DataFrame(data = None, index = input_data.index,
            columns = ['RSI'])

        # Calculate RSI for each period (first look_back periods are skipped)
        for i in range (self._look_back, len(input_data.index)):

            # Initialize for each look_back period
            upward_price_change = 0
            downward_price_change = 0

            # Calculate the total upward and downward changes in the look_back
            # period
            for t in range(i - self._look_back+1, i+1):

                delta = input_data.iat[t, 0] - input_data.iat[t-1, 0]

                if delta >= 0.:
                    upward_price_change += delta
                else:
                    downward_price_change -= delta

            # Calculate the averages for upward and downward changes
            upward_average = upward_price_change/self._look_back
            downward_average = downward_price_change/self._look_back

            # Set RSI for the day i
            if downward_average == 0.:
                rsi.iat[i, 0] = 100
            else:
                rsi.iat[i, 0] = 100-(100/(1+(upward_average/downward_average)))

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
        if self._ti_data.iat[-2, 0] < 70. and self._ti_data.iat[-1, 0] > 70.:
            return ('Sell', TRADE_SIGNALS['Sell'])

        # Oversold region
        if self._ti_data.iat[-2, 0] > 30. and self._ti_data.iat[-1, 0] < 30.:
            return ('Buy', TRADE_SIGNALS['Buy'])

        return ('Hold', TRADE_SIGNALS['Hold'])


        # Trading signals on warnings for breakout (upward or downward)
        # 3-days period is used for trend calculation

        # Not enough data for calculating trading signal
        if len(self._ti_data.index) < 3:
            return TRADE_SIGNALS['hold']

        # Warning for a downward breakout
        if self._ti_data['OBV'].iat[-3] > self._ti_data['OBV'].iat[-2] > \
                self._ti_data['OBV'].iat[-1]:
            return TRADE_SIGNALS['buy']

        # Warning for a upward breakout
        elif self._ti_data['OBV'].iat[-3] < self._ti_data['OBV'].iat[-2] < \
                self._ti_data['OBV'].iat[-1]:
            return TRADE_SIGNALS['sell']

        else:
            return TRADE_SIGNALS['hold']
