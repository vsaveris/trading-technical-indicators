"""
Trading-Technical-Indicators (tti) python library

File name: _directional_movement_index.py
    Implements the Directional Movement Index technical indicator.
"""

import pandas as pd

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

        # Calculate thr True Range
        dmi['true_range'].iloc[1:] = self._input_data[
            ['high', 'low', 'close']].pipe(
            self._rolling_pipe, 2,
            lambda x: max(x['high'][1] - x['low'][1],
                          x['high'][1] - x['close'][0],
                          x['close'][0] - x['low'][1],
                          )
        )

        # Calculate Directional Movement for 1 period
        dmi['+dm1'].iloc[1:] = self._input_data[['high', 'low', 'close']].pipe(
            self._rolling_pipe, 2,
            lambda x: x['high'][1] - x['high'][0]
            if x['high'][1] - x['high'][0] > x['low'][0] - x['low'][1] and
            x['high'][1] - x['high'][0] > 0
            else 0,
        )

        dmi['-dm1'].iloc[1:] = self._input_data[['high', 'low', 'close']].pipe(
            self._rolling_pipe, 2,
            lambda x: x['low'][0] - x['low'][1]
            if x['high'][1] - x['high'][0] < x['low'][0] - x['low'][1] and
            x['low'][0] - x['low'][1] > 0
            else 0,
        )

        # Calculate True Range and Directional Movement for 14 periods
        # (smoothed)
        dmi['tr14'].iat[13] = dmi['true_range'].iloc[:14].sum()
        dmi['+dm14'].iat[13] = dmi['+dm1'].iloc[:14].sum()
        dmi['-dm14'].iat[13] = dmi['-dm1'].iloc[:14].sum()

        for i in range(14, len(dmi.index)):
            dmi['tr14'].iat[i] = \
                dmi['tr14'].iat[i - 1] - (dmi['tr14'].iat[i - 1] / 14) +   \
                dmi['true_range'].iat[i]

            dmi['+dm14'].iat[i] = \
                dmi['+dm14'].iat[i - 1] - (dmi['+dm14'].iat[i - 1] / 14) + \
                dmi['+dm1'].iat[i]

            dmi['-dm14'].iat[i] = \
                dmi['-dm14'].iat[i - 1] - (dmi['-dm14'].iat[i - 1] / 14) + \
                dmi['-dm1'].iat[i]

        # Calculate the +DI and -DI
        dmi['+di14'].iloc[14:] = dmi[['+dm14', 'tr14']].iloc[14:].pipe(
            self._rolling_pipe, 1,
            lambda x: 100 * x['+dm14'][0] / x['tr14'][0],
        )

        dmi['-di14'].iloc[14:] = dmi[['-dm14', 'tr14']].iloc[14:].pipe(
            self._rolling_pipe, 1,
            lambda x: 100 * x['-dm14'][0] / x['tr14'][0],
        )

        # Calculate DX, ADX and ADXR
        dmi['di_diff'] = abs(dmi['+di14'] - dmi['-di14'])
        dmi['di_sum'] = abs(dmi['+di14'] + dmi['-di14'])

        dmi['dx'] = 100. * dmi['di_diff'] / dmi['di_sum']

        dmi['adx'].iat[27] = dmi['dx'].iloc[:28].sum() / 14

        for i in range(28, len(dmi.index)):
            dmi['adx'].iat[i] = \
                ((13 * dmi['adx'].iat[i - 1]) + dmi['dx'][i]) / 14

        for i in range(40, len(dmi.index)):
            dmi['adxr'].iat[i] = \
                (dmi['adx'].iat[i] + dmi['adx'].iat[i - 13]) / 2.0

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
        # ADX > 25 is a strong trend, ADX < 20 indicates no trend

        if self._ti_data['+di'].iat[-2] > self._ti_data['-di'].iat[-2] and \
                self._ti_data['+di'].iat[-1] < self._ti_data['-di'].iat[-1] \
                and self._ti_data['adx'].iat[-1] >= 20:
            return TRADE_SIGNALS['sell']

        elif self._ti_data['+di'].iat[-2] < self._ti_data['-di'].iat[-2] and \
                self._ti_data['+di'].iat[-1] > self._ti_data['-di'].iat[-1] \
                and self._ti_data['adx'].iat[-1] >= 20:
            return TRADE_SIGNALS['buy']

        else:
            return TRADE_SIGNALS['hold']
