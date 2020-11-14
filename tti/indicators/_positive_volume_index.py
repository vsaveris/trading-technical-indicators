"""
Trading-Technical-Indicators (tti) python library

File name: _positive_volume_index.py
    Implements the Positive Volume Index technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData


class PositiveVolumeIndex(TechnicalIndicator):
    """
    Positive Volume Index Technical Indicator class implementation.

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
                It contains one column, the 'pvi'.
        """

        # Not enough data
        if len(self._input_data.index) < 2:
            raise NotEnoughInputData('Positive Volume Index', 2,
                                     len(self._input_data.index))

        pvi = pd.DataFrame(index=self._input_data.index, columns=['pvi'],
                           data=None, dtype='float64')

        pvi['pvi'].iat[0] = 1000.0

        for i in range(1, len(self._input_data.index)):

            if self._input_data['volume'].iat[i] > \
                    self._input_data['volume'].iat[i - 1]:
                pvi['pvi'].iat[i] = \
                    pvi['pvi'].iat[i - 1] + (
                            self._input_data['close'].iat[i] -
                            self._input_data['close'].iat[i - 1]) * (
                            pvi['pvi'].iat[i - 1] /
                            self._input_data['close'].iat[i - 1])
            else:
                pvi['pvi'].iat[i] = pvi['pvi'].iat[i - 1]

        return pvi.round(4)

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
        if len(self._ti_data.index) < 255:
            return TRADE_SIGNALS['hold']

        # Yearly moving average of the indicator (255 periods)
        ema = self._ti_data['pvi'].ewm(span=255, min_periods=255, adjust=False,
                                       axis=0).mean()

        if ((self._ti_data['pvi'][-2] < ema[-2]) and
                (self._ti_data['pvi'][-1] > ema[-1])):
            return TRADE_SIGNALS['buy']

        if ((self._ti_data['pvi'][-2] > ema[-2]) and
                (self._ti_data['pvi'][-1] < ema[-1])):
            return TRADE_SIGNALS['sell']

        return TRADE_SIGNALS['hold']
