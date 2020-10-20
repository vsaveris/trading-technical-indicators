"""
Trading-Technical-Indicators (tti) python library

File name: _chaikin_oscillator.py
    Implements the Chaikin Oscillator technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ._accumulation_distribution_line import AccumulationDistributionLine
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData


class ChaikinOscillator(TechnicalIndicator):
    """
    Chaikin Oscillator Technical Indicator class implementation.

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
                It contains one column, the 'co'.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < 10:
            raise NotEnoughInputData('Chaikin Oscillator', 10,
                                     len(self._input_data.index))

        co = pd.DataFrame(index=self._input_data.index, columns=['co'],
                          data=0, dtype='float64')

        adl = AccumulationDistributionLine(self._input_data).getTiData()

        co['co'] = \
            adl.ewm(span=3, min_periods=3, adjust=False, axis=0).mean() - \
            adl.ewm(span=10, min_periods=10, adjust=False, axis=0).mean()

        return co.round(4)

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
        if len(self._ti_data.index) < 90:
            return TRADE_SIGNALS['hold']

        # 90-periods moving average
        ma_90 = self._input_data['close'].iloc[-90:].mean()

        # Buy signal when price above 90-MA and indicator upturns in the
        # negative area
        if self._input_data['close'].iat[-1] > ma_90 and \
           self._ti_data['co'].iat[-2] < self._ti_data['co'].iat[-1] < 0.0:
            return TRADE_SIGNALS['buy']

        # Sell signal when price below 90-MA and indicator downturns in the
        # positive area
        elif self._input_data['close'].iat[-1] < ma_90 and \
                self._ti_data['co'].iat[-2] > self._ti_data['co'].iat[-1] > 0.0:
            return TRADE_SIGNALS['sell']

        else:
            return TRADE_SIGNALS['hold']
