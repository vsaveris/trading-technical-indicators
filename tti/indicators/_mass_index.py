"""
Trading-Technical-Indicators (tti) python library

File name: _mass_index.py
    Implements the Mass Index technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData


class MassIndex(TechnicalIndicator):
    """
    Mass Index Technical Indicator class implementation.

    Args:
        input_data (pandas.DataFrame): The input data. Required input columns
            are ``high``, ``low``, ``close``. The index is of type
            ``pandas.DatetimeIndex``.

        fill_missing_values (bool, default=True): If set to True, missing
            values in the input data are being filled.

    Attributes:
        _input_data (pandas.DataFrame): The ``input_data`` after preprocessing.

        _ti_data (pandas.DataFrame): The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains one column, the ``mi``.

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
            ``pandas.DatetimeIndex``. It contains one column, the ``mi``.

        Raises:
            NotEnoughInputData: Not enough data for calculating the indicator.
        """

        # Not enough data for the 25-Mass Index
        if len(self._input_data.index) < 25:
            raise NotEnoughInputData('Mass Index', 25,
                                     len(self._input_data.index))

        # Append to input_data the 9-ema for close prices
        # This is required for the trading signal calculation and we want
        # to include it in the graph
        self._input_data['9_ema'] = self._input_data['close'].ewm(
            span=9, min_periods=9, adjust=False, axis=0).mean()

        mi = pd.DataFrame(index=self._input_data.index, columns=['mi'],
                          data=None, dtype='float64')

        high_low_diff = self._input_data['high'] - self._input_data['low']

        # Nine periods EMA of High-Low difference
        ema_9 = high_low_diff.ewm(span=9, min_periods=9, adjust=False,
                                  axis=0).mean()

        # Nine periods EMA of the nine periods EMA of the High-Low difference
        double_ema_9 = ema_9.ewm(span=9, min_periods=9, adjust=False,
                                 axis=0).mean()

        # 25-period Mass Index
        mi['mi'] = (ema_9 / double_ema_9).rolling(
            window=25, min_periods=25, center=False,
            win_type=None, on=None, axis=0, closed=None).sum()

        return mi.round(4)

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

        # Look for a Reversal Bulge (indicator raises above 27 and then drops
        # below 26.5. Specific values for 25-Mass Index.
        reversal_bulge = False

        if True or self._ti_data['mi'].iat[-1] < 26.5:

            for i in range(-2, -len(self._ti_data.index) - 1, -1):

                if self._ti_data['mi'].iat[i] < 26.5:
                    break

                elif self._ti_data['mi'].iat[i] > 27.0:
                    reversal_bulge = True
                    break

        # Signal based on 9-EMA trend
        if reversal_bulge:
            if self._input_data['9_ema'].iat[-2] < \
                    self._input_data['9_ema'].iat[-1]:
                return TRADE_SIGNALS['sell']

            if self._input_data['9_ema'].iat[-2] > \
                    self._input_data['9_ema'].iat[-1]:
                return TRADE_SIGNALS['buy']

        return TRADE_SIGNALS['hold']
