"""
Trading-Technical-Indicators (tti) python library

File name: _williams_accumulation_distribution.py
    Implements the Williams Accumulation Distribution technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS


class WilliamsAccumulationDistribution(TechnicalIndicator):
    """
    Williams Accumulation Distribution Technical Indicator class
    implementation.

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
                It contains one column, the 'wad'.
        """

        wad = pd.DataFrame(index=self._input_data.index, columns=['wad'],
                           data=None, dtype='float64')

        # Calculate the true range high
        wad['trh'] = pd.concat(
            [self._input_data['close'].shift(1), self._input_data['high']],
            axis=1).max(axis=1, skipna=False)

        # Calculate the true range low
        wad['trl'] = pd.concat(
            [self._input_data['close'].shift(1), self._input_data['low']],
            axis=1).min(axis=1, skipna=False)

        # Calculate today's Accumulation Distribution
        wad['wad'] = self._input_data['close'] - \
                     self._input_data['close'].shift(1)

        wad['wad'][wad['wad'] > 0] = self._input_data['close'] - wad['trl']

        wad['wad'][wad['wad'] < 0] = self._input_data['close'] - wad['trh']

        return wad[['wad']].round(4)

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

        # Last periods to consider when looking for divergences
        span_period = 30

        # Not enough data for trading signal
        if len(self._input_data.index) < span_period:
            return TRADE_SIGNALS['hold']

        if ((self._input_data['close'].iloc[-span_period:].min() ==
                self._input_data['close'].iat[-1]) and
                (self._ti_data['wad'].iloc[-span_period:].min() !=
                 self._ti_data['wad'].iat[-1])):
            return TRADE_SIGNALS['buy']

        if ((self._input_data['close'].iloc[-span_period:].max() ==
                self._input_data['close'].iat[-1]) and
                (self._ti_data['wad'].iloc[-span_period:].max() !=
                 self._ti_data['wad'].iat[-1])):
            return TRADE_SIGNALS['sell']

        return TRADE_SIGNALS['hold']
