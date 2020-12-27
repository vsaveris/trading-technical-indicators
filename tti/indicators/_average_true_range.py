"""
Trading-Technical-Indicators (tti) python library

File name: _average_true_range.py
    Implements the Average True Range technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData


class AverageTrueRange(TechnicalIndicator):
    """
    Average True Range Technical Indicator class implementation.

    Args:
        input_data (pandas.DataFrame): The input data. Required input columns
            are ``high``, ``low``, ``close``. The index is of type
            ``pandas.DatetimeIndex``.

        fill_missing_values (bool, default=True): If set to True, missing
            values in the input data are being filled.

    Attributes:
        _input_data (pandas.DataFrame): The ``input_data`` after preprocessing.

        _ti_data (pandas.DataFrame): The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains one column, the ``atr``.

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
            ``pandas.DatetimeIndex``. It contains one column, the ``atr``.

        Raises:
            NotEnoughInputData: Not enough data for calculating the indicator.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < 14:
            raise NotEnoughInputData('Average True Range', 2,
                                     len(self._input_data.index))

        atr = pd.DataFrame(index=self._input_data.index, columns=['atr'],
                           data=0, dtype='float64')

        # Calculate Today's High - Today's Low
        atr['TH-TL'] = self._input_data['high'] - self._input_data['low']

        # Calculate Today's High - Yesterday's Close
        atr['YC-TH'] = \
            self._input_data['high'] - self._input_data['close'].shift(1)

        # Calculate Yesterday's Close - Today's Low
        atr['YC-TL'] = \
            self._input_data['close'].shift(1) - self._input_data['low']

        atr['atr'] = atr[['TH-TL', 'YC-TH', 'YC-TL']].max(axis=1)

        # Wilder's Moving Average
        atr['atr'] = pd.Series(
            data=[atr['atr'].iloc[:14].mean()], index=[atr.index[13]]
        ).append(atr['atr'].iloc[14:]).ewm(alpha=1 / 14,
                                           adjust=False,).mean().round(4)

        return atr[['atr']]

    def getTiSignal(self):
        """
        Calculates and returns the trading signal for the calculated technical
        indicator.

        Returns:
            {('hold', 0), ('buy', -1), ('sell', 1)}: The calculated trading
            signal.
        """

        # Not enough data for calculating trading signal
        if len(self._ti_data.index) < 10:
            return TRADE_SIGNALS['hold']

        # Calculate Simple Moving Averages
        sma_05 = self._input_data.rolling(
            window=5, min_periods=5, center=False, win_type=None, on=None,
            axis=0, closed=None).mean()

        sma_10 = self._input_data.rolling(
            window=10, min_periods=5, center=False, win_type=None, on=None,
            axis=0, closed=None).mean()

        # Assumption on what high volatility means
        if self._ti_data['atr'].values[-1] > \
                0.01 * self._input_data['close'].values[-1]:

            # Price falling is expected or secondary rally
            if self._input_data['close'].iat[-1] > sma_05.iat[-1, 0]:

                # Assuming long term upward rally
                if self._input_data['close'].iat[-1] > sma_10.iat[-1, 0]:
                    return TRADE_SIGNALS['buy']
                else:
                    return TRADE_SIGNALS['sell']

            # Price raise is expected
            if self._input_data['close'].iat[-1] < sma_05.iat[-1, 0]:
                return TRADE_SIGNALS['buy']

        return TRADE_SIGNALS['hold']
