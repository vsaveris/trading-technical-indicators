"""
Trading-Technical-Indicators (tti) python library

File name: _negative_volume_index.py
    Implements the Negative Volume Index technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData


class NegativeVolumeIndex(TechnicalIndicator):
    """
    Negative Volume Index Technical Indicator class implementation.

    Args:
        input_data (pandas.DataFrame): The input data. Required input columns
            are ``close``, ``volume``. The index is of type
            ``pandas.DatetimeIndex``.

        fill_missing_values (bool, default=True): If set to True, missing
            values in the input data are being filled.

    Attributes:
        _input_data (pandas.DataFrame): The ``input_data`` after preprocessing.

        _ti_data (pandas.DataFrame): The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains one column, the ``nvi``.

        _properties (dict): Indicator properties.

        _calling_instance (str): The name of the class.

    Raises:
        WrongTypeForInputParameter: Input argument has wrong type.
        WrongValueForInputParameter: Unsupported value for input argument.
        NotEnoughInputData: Not enough data for calculating the indicator.
        TypeError: Type error occurred when validating the ``input_data``.
        ValueError: Value error occurred when validating the ``input_data``.
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

        Returns:
            pandas.DataFrame: The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains one column, the ``nvi``.

        Raises:
            NotEnoughInputData: Not enough data for calculating the indicator.
        """

        # Not enough data
        if len(self._input_data.index) < 2:
            raise NotEnoughInputData('Negative Volume Index', 2,
                                     len(self._input_data.index))

        nvi = pd.DataFrame(index=self._input_data.index, columns=['nvi'],
                           data=None, dtype='float64')

        nvi['nvi'].iat[0] = 1000.0

        for i in range(1, len(self._input_data.index)):

            if self._input_data['volume'].iat[i] < \
                    self._input_data['volume'].iat[i - 1]:
                nvi['nvi'].iat[i] = \
                    nvi['nvi'].iat[i - 1] + (
                            self._input_data['close'].iat[i] -
                            self._input_data['close'].iat[i - 1]) * (
                            nvi['nvi'].iat[i - 1] /
                            self._input_data['close'].iat[i - 1])
            else:
                nvi['nvi'].iat[i] = nvi['nvi'].iat[i - 1]

        return nvi.round(4)

    def getTiSignal(self):
        """
        Calculates and returns the trading signal for the calculated technical
        indicator.

        Returns:
            {('hold', 0), ('buy', -1), ('sell', 1)}: The calculated trading
            signal.
        """

        # Not enough data for calculating trading signal
        if len(self._ti_data.index) < 255:
            return TRADE_SIGNALS['hold']

        # Yearly moving average of the indicator (255 periods)
        ema = self._ti_data['nvi'].ewm(span=255, min_periods=255, adjust=False,
                                       axis=0).mean()

        if self._ti_data['nvi'][-1] > ema[-1]:
            return TRADE_SIGNALS['buy']

        return TRADE_SIGNALS['hold']
