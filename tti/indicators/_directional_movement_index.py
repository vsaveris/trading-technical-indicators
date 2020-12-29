"""
Trading-Technical-Indicators (tti) python library

File name: _directional_movement_index.py
    Implements the Directional Movement Index technical indicator.
"""

import pandas as pd
import numpy as np

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData


class DirectionalMovementIndex(TechnicalIndicator):
    """
    Directional Movement Index Technical Indicator class implementation.

    Args:
        input_data (pandas.DataFrame): The input data. Required input columns
            are ``high``, ``low``, ``close``. The index is of type
            ``pandas.DatetimeIndex``.

        fill_missing_values (bool, default=True): If set to True, missing
            values in the input data are being filled.

    Attributes:
        _input_data (pandas.DataFrame): The ``input_data`` after preprocessing.

        _ti_data (pandas.DataFrame): The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains three columns, the ``+di``,
            ``-di``, ``dx``, ``adx`` and the ``adxr``.

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
            ``pandas.DatetimeIndex``. It contains three columns, the ``+di``,
            ``-di``, ``dx``, ``adx`` and the ``adxr``.

        Raises:
            NotEnoughInputData: Not enough data for calculating the indicator.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < 28:
            raise NotEnoughInputData('Directional Movement Index', 28,
                                     len(self._input_data.index))

        dmi = pd.DataFrame(
            index=self._input_data.index,
            columns=['true_range', '+dm1', '-dm1', 'tr14', '+dm14', '-dm14',
                     '+di14', '-di14', 'di_diff', 'di_sum', 'dx', 'adx',
                     'adxr'], dtype='float64', data=None)

        # Calculate the True Range
        candidates = [self._input_data['high'].values[1:] -
                      self._input_data['low'].values[1:],
                      self._input_data['high'].values[1:] -
                      self._input_data['close'].values[:-1],
                      self._input_data['close'].values[:-1] -
                      self._input_data['low'].values[1:]]

        dmi['true_range'].values[1:] = np.max(np.column_stack(candidates),
                                              axis=1)

        # Calculate Directional Movement for one period
        for i in range(1, len(self._input_data.index)):

            dmi['+dm1'].values[i] = self._input_data['high'].values[i] - \
                self._input_data['high'].values[i-1] if \
                ((self._input_data['high'].values[i] -
                  self._input_data['high'].values[i-1] >
                  self._input_data['low'].values[i-1] -
                  self._input_data['low'].values[i])
                 and (self._input_data['high'].values[i] -
                      self._input_data['high'].values[i-1] > 0)) else 0

            dmi['-dm1'].values[i] = self._input_data['low'].values[i-1] - \
                self._input_data['low'].values[i] if \
                ((self._input_data['high'].values[i] -
                  self._input_data['high'].values[i-1] <
                  self._input_data['low'].values[i-1] -
                  self._input_data['low'].values[i])
                 and (self._input_data['low'].values[i-1] -
                      self._input_data['low'].values[i] > 0)) else 0

        # Calculate True Range and Directional Movement for 14 periods
        # (smoothed)
        dmi['tr14'].iat[13] = dmi['true_range'].iloc[:14].sum()
        dmi['+dm14'].iat[13] = dmi['+dm1'].iloc[:14].sum()
        dmi['-dm14'].iat[13] = dmi['-dm1'].iloc[:14].sum()

        for i in range(14, len(dmi.index)):
            dmi['tr14'].values[i] = dmi['tr14'].values[i - 1] - \
                (dmi['tr14'].values[i - 1] / 14) + dmi['true_range'].values[i]

            dmi['+dm14'].values[i] = dmi['+dm14'].values[i - 1] - \
                (dmi['+dm14'].values[i - 1] / 14) + dmi['+dm1'].values[i]

            dmi['-dm14'].values[i] = dmi['-dm14'].values[i - 1] - \
                (dmi['-dm14'].values[i - 1] / 14) + dmi['-dm1'].values[i]

        # Calculate the +DI and -DI
        dmi['+di14'].iloc[14:] = 100 * dmi['+dm14'].iloc[14:] / \
            dmi['tr14'].iloc[14:]

        dmi['-di14'].iloc[14:] = 100 * dmi['-dm14'].iloc[14:] / \
            dmi['tr14'].iloc[14:]

        # Calculate DX, ADX and ADXR
        dmi['di_diff'] = abs(dmi['+di14'] - dmi['-di14'])
        dmi['di_sum'] = abs(dmi['+di14'] + dmi['-di14'])

        dmi['dx'] = 100. * dmi['di_diff'] / dmi['di_sum']

        dmi['adx'].iat[27] = dmi['dx'].iloc[:28].sum() / 14

        for i in range(28, len(dmi.index)):
            dmi['adx'].values[i] = \
                ((13 * dmi['adx'].values[i - 1]) + dmi['dx'].values[i]) / 14

        for i in range(40, len(dmi.index)):
            dmi['adxr'].values[i] = \
                (dmi['adx'].values[i] + dmi['adx'].values[i - 13]) / 2.0

        # Keep the required columns
        dmi = dmi[['+di14', '-di14', 'dx', 'adx', 'adxr']]
        dmi.columns = ['+di', '-di', 'dx', 'adx', 'adxr']

        return dmi.round(4)

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

        # A buy signal is given when +DI crosses above -DI
        # A sell signal is given when -DI crosses above +DI
        # ADXR > 25 is a strong trend, ADXR < 20 indicates no trend

        if self._ti_data['+di'].iat[-2] > self._ti_data['-di'].iat[-2] and \
                self._ti_data['+di'].iat[-1] < self._ti_data['-di'].iat[-1] \
                and self._ti_data['adxr'].iat[-1] >= 20:
            return TRADE_SIGNALS['sell']

        elif self._ti_data['+di'].iat[-2] < self._ti_data['-di'].iat[-2] and \
                self._ti_data['+di'].iat[-1] > self._ti_data['-di'].iat[-1] \
                and self._ti_data['adxr'].iat[-1] >= 20:
            return TRADE_SIGNALS['buy']

        else:
            return TRADE_SIGNALS['hold']
