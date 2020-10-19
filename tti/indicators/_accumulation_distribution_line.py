"""
Trading-Technical-Indicators (tti) python library

File name: _accumulation_distribution_line.py
    Implements the Accumulation Distribution Line technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS


class AccumulationDistributionLine(TechnicalIndicator):
    """
    Accumulation Distribution Line Technical Indicator class implementation.

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
                It contains one column, the 'adl'.
        """

        adl = pd.DataFrame(index=self._input_data.index, columns=['adl'],
                           data=0, dtype='int64')

        adl['adl'] = self._input_data['volume'] * (
                (self._input_data['close'] - self._input_data['low']) -
                (self._input_data['high'] - self._input_data['close'])
        ) / (self._input_data['high'] - self._input_data['low'])

        for i in range(1, len(adl.index)):
            adl['adl'].iat[i] += adl['adl'].iat[i - 1]

        return adl.astype(dtype='int64', errors='ignore')

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

        # Trading signals Divergences calculated in 2-days period

        # Not enough data for calculating trading signal
        if len(self._ti_data.index) < 3:
            return TRADE_SIGNALS['hold']

        # Warning for a upward breakout
        if self._ti_data['adl'].iat[-3] > self._ti_data['adl'].iat[-2] > \
                self._ti_data['adl'].iat[-1]:
            return TRADE_SIGNALS['buy']

        # Warning for a downward breakout
        elif self._ti_data['adl'].iat[-3] < self._ti_data['adl'].iat[-2] < \
                self._ti_data['adl'].iat[-1]:
            return TRADE_SIGNALS['sell']

        else:
            return TRADE_SIGNALS['hold']
