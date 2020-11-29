"""
Trading-Technical-Indicators (tti) python library

File name: _average_true_range.py
    Implements the Average True Range technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData


class AverageTrueRange(TechnicalIndicator):
    """
    Average True Range Technical Indicator class implementation.

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
                It contains one column, the 'atr'.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < 14:
            raise NotEnoughInputData('Average True Range', 2,
                                     len(self._input_data.index))

        atr = pd.DataFrame(index=self._input_data.index, columns=['atr'],
                           data=0, dtype='float64')

        # Calculate Today's High - Today's Low
        atr['TH-TL'] = self._input_data['high'] - self._input_data['low']

        # Calculate Today's High - Yesterday's Close
        atr['YC-TH'] = \
            self._input_data['high'] - self._input_data['close'].shift(1)

        # Calculate Yesterday's Close - Today's Low
        atr['YC-TL'] = \
            self._input_data['close'].shift(1) - self._input_data['low']

        atr['atr'] = atr[['TH-TL', 'YC-TH', 'YC-TL']].max(axis=1)

        # Wilder's Moving Average
        atr['atr'] = pd.Series(
            data=[atr['atr'].iloc[:14].mean()], index=[atr.index[13]]
        ).append(atr['atr'].iloc[14:]).ewm(alpha=1 / 14,
                                           adjust=False,).mean().round(4)

        return atr[['atr']]

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

        # Calculate Simple Moving Average
        sma = self._input_data.rolling(
            window=14, min_periods=14, center=False,
            win_type=None, on=None, axis=0, closed=None).mean().round(4)

        # Not enough data for calculating trading signal
        if len(self._ti_data.index) < 1:
            return TRADE_SIGNALS['hold']

        # Price above average and ATR is high
        if self._input_data['close'].iat[-1] > sma.iat[-1, 0] and \
                self._ti_data['atr'].iat[-1] > 2:
            return TRADE_SIGNALS['sell']

        # Price below average and ATR is high
        if self._input_data['close'].iat[-1] < sma.iat[-1, 0] and \
                self._ti_data['atr'].iat[-1] > 2:
            return TRADE_SIGNALS['buy']

        return TRADE_SIGNALS['hold']
