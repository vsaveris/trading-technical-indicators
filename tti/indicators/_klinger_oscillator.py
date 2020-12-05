"""
Trading-Technical-Indicators (tti) python library

File name: _klinger_oscillator.py
    Implements the Klinger Oscillator technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData


class KlingerOscillator(TechnicalIndicator):
    """
    Klinger Oscillator Technical Indicator class implementation.

    Args:
        input_data (pandas.DataFrame): The input data. Required input columns
            are ``high``, ``low``, ``close``, ``volume``. The index is of type
            ``pandas.DatetimeIndex``.

        fill_missing_values (bool, default=True): If set to True, missing
            values in the input data are being filled.

    Attributes:
        _input_data (pandas.DataFrame): The ``input_data`` after preprocessing.

        _ti_data (pandas.DataFrame): The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains one column, the ``ko``.

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
            ``pandas.DatetimeIndex``. It contains one column, the ``ko``.

        Raises:
            NotEnoughInputData: Not enough data for calculating the indicator.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < 55:
            raise NotEnoughInputData('Klinger Oscillator', 55,
                                     len(self._input_data.index))

        ko = pd.DataFrame(index=self._input_data.index, columns=['ko'],
                          data=None, dtype='float64')

        # Trend Direction
        t = self._input_data[['high', 'low', 'close']].sum(axis=1) - \
            self._input_data[['high', 'low', 'close']].sum(axis=1).shift(1)
        t[t > 0.0] = 1.0
        t[t <= 0.0] = -1.0

        # Daily Measurement
        dm = self._input_data['high'] - self._input_data['low']

        # Cumulative Measurement
        cm = [0.0]
        for i in range(1, len(self._input_data)):
            if t[i] == t[i - 1]:
                cm.append(cm[i - 1] + dm[i])
            else:
                cm.append(dm[i - 1] + dm[i])

        volume_force = \
            self._input_data['volume'] * abs(2 * (dm / cm) - 1) * t * 100

        ko['ko'] = volume_force.ewm(
            span=34, min_periods=34, adjust=False, axis=0
        ).mean() - volume_force.ewm(
            span=55, min_periods=55, adjust=False, axis=0
        ).mean()

        return ko.round(4)

    def getTiSignal(self):
        """
        Calculates and returns the trading signal for the calculated technical
        indicator.

        Returns:
            {('hold', 0), ('buy', -1), ('sell', 1)}: The calculated trading
            signal.
        """

        # Not enough data for calculating trading signal
        if len(self._ti_data.index) < 2:
            return TRADE_SIGNALS['hold']

        # Signal based on crossovers with zero line
        if self._ti_data['ko'].iat[-2] < 0.0 < self._ti_data['ko'].iat[-1]:
            return TRADE_SIGNALS['sell']

        if self._ti_data['ko'].iat[-2] > 0.0 > self._ti_data['ko'].iat[-1]:
            return TRADE_SIGNALS['buy']

        return TRADE_SIGNALS['hold']
