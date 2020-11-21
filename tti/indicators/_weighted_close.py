"""
Trading-Technical-Indicators (tti) python library

File name: _weighted_close.py
    Implements the Weighted Close technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS


class WeightedClose(TechnicalIndicator):
    """
    Weighted Close Technical Indicator class implementation.

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
                It contains one column, the 'wc'.
        """

        wc = pd.DataFrame(index=self._input_data.index, columns=['wc'],
                          data=None, dtype='float64')

        wc['wc'] = (2 * self._input_data['close'] + self._input_data['high'] +
                    self._input_data['low']) / 4

        return wc.round(4)

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

        # Close price goes below Weighted Close
        if ((self._input_data['close'].iat[-2] > self._ti_data['wc'].iat[-2])
                and (self._input_data['close'].iat[-1] <
                     self._ti_data['wc'].iat[-1])):
            return TRADE_SIGNALS['buy']

        # Close price goes above Weighted Close
        if ((self._input_data['close'].iat[-2] < self._ti_data['wc'].iat[-2])
                and (self._input_data['close'].iat[-1] >
                     self._ti_data['wc'].iat[-1])):
            return TRADE_SIGNALS['sell']

        return TRADE_SIGNALS['hold']
