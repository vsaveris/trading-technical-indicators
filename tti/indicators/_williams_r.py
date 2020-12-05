"""
Trading-Technical-Indicators (tti) python library

File name: _williams_r.py
    Implements the Williams %R technical indicator.
"""

import pandas as pd
import numpy as np

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class WilliamsR(TechnicalIndicator):
    """
    Williams %R Technical Indicator class implementation.

    Args:
        input_data (pandas.DataFrame): The input data. Required input columns
            are ``high``, ``low``, ``close``. The index is of type
            ``pandas.DatetimeIndex``.

        period (int, default=5): The past periods to be used for the
            calculation of the indicator.

        fill_missing_values (bool, default=True): If set to True, missing
            values in the input data are being filled.

    Attributes:
        _input_data (pandas.DataFrame): The ``input_data`` after preprocessing.

        _ti_data (pandas.DataFrame): The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains one column, the ``wr``.

        _properties (dict): Indicator properties.

        _calling_instance (str): The name of the class.

    Raises:
        WrongTypeForInputParameter: Input argument has wrong type.
        WrongValueForInputParameter: Unsupported value for input argument.
        NotEnoughInputData: Not enough data for calculating the indicator.
        TypeError: Type error occurred when validating the ``input_data``.
        ValueError: Value error occurred when validating the ``input_data``.
    """
    def __init__(self, input_data, period=5, fill_missing_values=True):

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
            ``pandas.DatetimeIndex``. It contains one column, the ``wr``.

        Raises:
            NotEnoughInputData: Not enough data for calculating the indicator.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._period:
            raise NotEnoughInputData('William\'s %R', self._period,
                                     len(self._input_data.index))

        wr = pd.DataFrame(index=self._input_data.index, columns=['wr'],
                          data=None, dtype='float64')

        wr['highest_high'] = self._input_data['high'].rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).max()

        wr['lowest_low'] = self._input_data['low'].rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).min()

        wr['wr'] = -100 * ((wr['highest_high'] - self._input_data['close']) /
                           (wr['highest_high'] - wr['lowest_low']))

        return wr[['wr']].round(4)

    def getTiSignal(self):
        """
        Calculates and returns the trading signal for the calculated technical
        indicator.

        Returns:
            {('hold', 0), ('buy', -1), ('sell', 1)}: The calculated trading
            signal.
        """

        # Not enough data for trading signal
        if len(self._ti_data.index) < 2:
            return TRADE_SIGNALS['hold']

        # Oversold area is <= -80
        try:
            last_oversold_index = np.where(
                self._ti_data['wr'].iloc[:-1] <= -80)[0][-1]
        except:
            last_oversold_index = -1

        # Overbought area is >= -20
        try:
            last_overbought_index = np.where(
                self._ti_data['wr'].iloc[:-1] >= -20)[0][-1]
        except:
            last_overbought_index = -1

        # Indicator was not in the overbought or in the oversold area before
        if last_oversold_index == -1 and last_overbought_index == -1:
            return TRADE_SIGNALS['hold']

        # Indicator was in the oversold area before
        if ((last_oversold_index > last_overbought_index) and
                (self._ti_data['wr'].iat[-2] < -50 <
                 self._ti_data['wr'].iat[-1])):
            return TRADE_SIGNALS['buy']

        # Indicator was in the overbought area before
        if ((last_oversold_index < last_overbought_index) and
                (self._ti_data['wr'].iat[-2] > -50 >
                 self._ti_data['wr'].iat[-1])):
            return TRADE_SIGNALS['sell']

        return TRADE_SIGNALS['hold']
