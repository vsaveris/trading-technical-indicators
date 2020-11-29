"""
Trading-Technical-Indicators (tti) python library

File name: _moving_average_convergence_divergence.py
    Implements the Moving Average Convergence Divergence technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData


class MovingAverageConvergenceDivergence(TechnicalIndicator):
    """
    Moving Average Convergence Divergence Technical Indicator class
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
                It contains two columns, the 'macd' and the 'signal_line'.
        """

        # Not enough data, 26 periods are required
        if len(self._input_data.index) < 26:
            raise NotEnoughInputData('Moving Average Convergence Divergence',
                                     26, len(self._input_data.index))

        # Calculate Exponential Moving Average for 26 periods
        ema_26 = self._input_data.ewm(span=26, min_periods=26, adjust=False,
                                      axis=0).mean().round(4)

        # Calculate Exponential Moving Average for 12 periods
        ema_12 = self._input_data.ewm(span=12, min_periods=12, adjust=False,
                                      axis=0).mean().round(4)

        # Calculate MACD
        macd = ema_12 - ema_26
        macd = pd.concat([macd, macd.ewm(span=9, min_periods=9, adjust=False,
                                         axis=0).mean()], axis=1).round(4)

        macd.columns = ['macd', 'signal_line']

        return macd

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

        # MACD rises above zero
        if self._ti_data['macd'][-2] < 0 < self._ti_data['macd'][-1]:
            return TRADE_SIGNALS['buy']

        # MACD fall below zero
        if self._ti_data['macd'][-2] > 0 > self._ti_data['macd'][-1]:
            return TRADE_SIGNALS['sell']

        # MACD falls below Signal Line
        if self._ti_data['macd'][-2] > self._ti_data['signal_line'][-2] and \
           self._ti_data['macd'][-1] < self._ti_data['signal_line'][-1]:
            return TRADE_SIGNALS['sell']

        # MACD rises above Signal Line
        if self._ti_data['macd'][-2] < self._ti_data['signal_line'][-2] and \
           self._ti_data['macd'][-1] > self._ti_data['signal_line'][-1]:
            return TRADE_SIGNALS['buy']

        return TRADE_SIGNALS['hold']

