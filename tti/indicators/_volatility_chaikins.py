"""
Trading-Technical-Indicators (tti) python library

File name: _volatility_chaikins.py
    Implements the Volatility Chaikins technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class VolatilityChaikins(TechnicalIndicator):
    """
    Volatility Chaikins Technical Indicator class implementation.

    Args:
        input_data (pandas.DataFrame): The input data. Required input columns
            are ``high``, ``low``. The index is of type
            ``pandas.DatetimeIndex``.

        ema_period (int, default=10): The past periods to be used for the
            calculation of the daily high and low prices exponential moving
            average.

        change_period (int, default=10): The period for calculating the
            change in the exponential moving average of the daily high and low
            prices.

        fill_missing_values (bool, default=True): If set to True, missing
            values in the input data are being filled.

    Attributes:
        _input_data (pandas.DataFrame): The ``input_data`` after preprocessing.

        _ti_data (pandas.DataFrame): The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains one column, the ``vch``.

        _properties (dict): Indicator properties.

        _calling_instance (str): The name of the class.

    Raises:
        WrongTypeForInputParameter: Input argument has wrong type.
        WrongValueForInputParameter: Unsupported value for input argument.
        NotEnoughInputData: Not enough data for calculating the indicator.
        TypeError: Type error occurred when validating the ``input_data``.
        ValueError: Value error occurred when validating the ``input_data``.
    """
    def __init__(self, input_data, ema_period=10, change_period=10,
                 fill_missing_values=True):

        # Validate and store if needed, the input parameters
        if isinstance(ema_period, int):
            if ema_period > 0:
                self._ema_period = ema_period
            else:
                raise WrongValueForInputParameter(
                    ema_period, 'ema_period', '>0')
        else:
            raise WrongTypeForInputParameter(
                type(ema_period), 'ema_period', 'int')

        if isinstance(change_period, int):
            if change_period > 0:
                self._change_period = change_period
            else:
                raise WrongValueForInputParameter(
                    change_period, 'change_period', '>0')
        else:
            raise WrongTypeForInputParameter(
                type(change_period), 'change_period', 'int')

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
            ``pandas.DatetimeIndex``. It contains one column, the ``vch``.

        Raises:
            NotEnoughInputData: Not enough data for calculating the indicator.
        """

        # Not enough data for the requested period
        if (len(self._input_data.index) <
                max(self._ema_period, self._change_period)):
            raise NotEnoughInputData(
                'Volatility Chaikins',
                max(self._ema_period, self._change_period),
                len(self._input_data.index))

        vch = pd.DataFrame(index=self._input_data.index, columns=['vch'],
                           data=None, dtype='float64')

        vch['high_low_diff_ema'] = (
                self._input_data['high'] - self._input_data['low']).ewm(
            span=self._ema_period, min_periods=self._ema_period,
            adjust=False, axis=0).mean()

        vch['high_low_diff_ema_change'] = (vch['high_low_diff_ema'] -
            vch['high_low_diff_ema'].shift(self._change_period))

        vch['vch'] = 100 * (vch['high_low_diff_ema_change'] /
                            vch['high_low_diff_ema'].shift(self._change_period)
                            )

        return vch[['vch']].round(4)

    def getTiSignal(self):
        """
        Calculates and returns the trading signal for the calculated technical
        indicator.

        Returns:
            {('hold', 0), ('buy', -1), ('sell', 1)}: The calculated trading
            signal.
        """

        # Not enough data for trading signal
        if len(self._ti_data.index) < 3:
            return TRADE_SIGNALS['hold']

        if (self._ti_data['vch'].iat[-3] < self._ti_data['vch'].iat[-2] <
                self._ti_data['vch'].iat[-1]):
            return TRADE_SIGNALS['buy']

        if (self._ti_data['vch'].iat[-3] > self._ti_data['vch'].iat[-2] >
                self._ti_data['vch'].iat[-1]):
            return TRADE_SIGNALS['sell']

        return TRADE_SIGNALS['hold']
