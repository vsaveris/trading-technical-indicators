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

    Args:
        input_data (pandas.DataFrame): The input data. Required input columns
            are ``high``, ``low``, ``close``, ``volume``. The index is of type
            ``pandas.DatetimeIndex``.

        fill_missing_values (bool, default=True): If set to True, missing
            values in the input data are being filled.

    Attributes:
        _input_data (pandas.DataFrame): The ``input_data`` after preprocessing.

        _ti_data (pandas.DataFrame): The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains one column, the ``adl``.

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
        Calculates the technical indicator for the given input data.

        Returns:
            pandas.DataFrame: The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains one column, the ``adl``.
        """

        adl = pd.DataFrame(index=self._input_data.index, columns=['adl'],
                           data=0, dtype='int64')

        adl['adl'] = self._input_data['volume'] * (
                (self._input_data['close'] - self._input_data['low']) -
                (self._input_data['high'] - self._input_data['close'])
        ) / (self._input_data['high'] - self._input_data['low'])

        adl = adl.cumsum(axis=0)

        return adl.astype(dtype='int64', errors='ignore')

    def getTiSignal(self):
        """
        Calculates and returns the trading signal for the calculated technical
        indicator.

        Returns:
            {('hold', 0), ('buy', -1), ('sell', 1)}: The calculated trading
            signal.
        """

        # Trading signals Convergences/Divergences calculated in 2-days period

        # Not enough data for calculating trading signal
        if len(self._ti_data.index) < 2:
            return TRADE_SIGNALS['hold']

        price_slope = self._input_data['close'].iat[-1] - \
            self._input_data['close'].iat[-2]

        if ((price_slope < 0 < self._ti_data['adl'].iat[-1]) or
                (price_slope > 0 and self._ti_data['adl'].iat[-1] > 0)):
            return TRADE_SIGNALS['buy']

        if ((price_slope > 0 > self._ti_data['adl'].iat[-1]) or
                (price_slope < 0 and self._ti_data['adl'].iat[-1] < 0)):
            return TRADE_SIGNALS['sell']

        return TRADE_SIGNALS['hold']
