"""
Trading-Technical-Indicators (tti) python library

File name: _relative_strength_index.py
    Implements the Relative Strength Index technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class RelativeStrengthIndex(TechnicalIndicator):
    """
    Relative Strength Index Technical Indicator class implementation.

    Args:
        input_data (pandas.DataFrame): The input data. Required input column
            is ``close``. The index is of type ``pandas.DatetimeIndex``.

        period (int, default=14): The past periods to be used for the
            calculation of the indicator. Popular values are 14, 9 and 25.

        fill_missing_values (bool, default=True): If set to True, missing
            values in the input data are being filled.

    Attributes:
        _input_data (pandas.DataFrame): The ``input_data`` after preprocessing.

        _ti_data (pandas.DataFrame): The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains one column ``rsi``.

        _properties (dict): Indicator properties.

        _calling_instance (str): The name of the class.

    Raises:
        WrongTypeForInputParameter: Input argument has wrong type.
        WrongValueForInputParameter: Unsupported value for input argument.
        NotEnoughInputData: Not enough data for calculating the indicator.
        TypeError: Type error occurred when validating the ``input_data``.
        ValueError: Value error occurred when validating the ``input_data``.
    """
    def __init__(self, input_data, period=14, fill_missing_values=True):

        # Validate and store if needed, the input parameters
        if isinstance(period, int):
            if period > 0:
                self._period = period
            else:
                raise WrongValueForInputParameter(
                    period, 'period', '>0')
        else:
            raise WrongTypeForInputParameter(
                type(period), 'period', 'int')

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
            ``pandas.DatetimeIndex``. It contains one column ``rsi``.

        Raises:
            NotEnoughInputData: Not enough data for calculating the indicator.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._period + 1:
            raise NotEnoughInputData('Relative Strength Index',
                                     self._period + 1,
                                     len(self._input_data.index))

        rsi = pd.DataFrame(data=None, index=self._input_data.index,
                           columns=['rsi'], dtype='float64')

        # Calculate Upward Price Change
        upc = pd.DataFrame(data=None, index=self._input_data.index,
                           columns=['upc', 'smoothed_upc'])

        for i in range(1, len(self._input_data.index)):
            upc['upc'].values[i] = round(self._input_data['close'].values[i] -
                self._input_data['close'].values[i - 1] if
                    self._input_data['close'].values[i] >
                    self._input_data['close'].values[i - 1] else 0.0, 4)

        upc['smoothed_upc'].iat[self._period] = \
            upc['upc'].iloc[:self._period + 1].mean()

        for i in range(self._period + 1, len(self._input_data.index)):
            upc['smoothed_upc'].values[i] = round(
                upc['smoothed_upc'].values[i - 1] +
                (upc['upc'].values[i] - upc['smoothed_upc'].values[i - 1]
                 ) / self._period, 4)

        # Calculate Downward Price Change
        dpc = pd.DataFrame(data=None, index=self._input_data.index,
                           columns=['dpc', 'smoothed_dpc'])

        for i in range(1, len(self._input_data.index)):
            dpc['dpc'].values[i] = round(
                self._input_data['close'].values[i - 1] -
                self._input_data['close'].values[i] if
                self._input_data['close'].values[i] <
                self._input_data['close'].values[i - 1] else 0.0, 4)

        dpc['smoothed_dpc'].iat[self._period] = \
            dpc['dpc'].iloc[:self._period + 1].mean()

        for i in range(self._period + 1, len(self._input_data.index)):
            dpc['smoothed_dpc'].values[i] = round(
                dpc['smoothed_dpc'].values[i - 1] +
                (dpc['dpc'].values[i] - dpc['smoothed_dpc'].values[i - 1]
                 ) / self._period, 4)

        rsi['rsi'] = \
            100.0 - \
            (100.0 / ((upc['smoothed_upc'] / dpc['smoothed_dpc']) + 1.0))

        return rsi.astype('float64').round(4)

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

        # Overbought region
        if self._ti_data['rsi'].iat[-2] < 70. < self._ti_data['rsi'].iat[-1]:
            return TRADE_SIGNALS['sell']

        # Oversold region
        if self._ti_data['rsi'].iat[-2] > 30. > self._ti_data['rsi'].iat[-1]:
            return TRADE_SIGNALS['buy']

        return TRADE_SIGNALS['hold']
