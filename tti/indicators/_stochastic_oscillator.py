"""
Trading-Technical-Indicators (tti) python library

File name: _stochastic_oscillator.py
    Implements the Stochastic Oscillator technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class StochasticOscillator(TechnicalIndicator):
    """
    Stochastic Oscillator Technical Indicator class implementation.

    Args:
        input_data (pandas.DataFrame): The input data. Required input columns
            are ``high``, ``low``, ``close``. The index is of type
            ``pandas.DatetimeIndex``.

        k_periods (int, default=14): Number of periods to be used in the
            stochastic calculation %K.

        k_slowing_periods (int, default=1): Smoothing to be used in the
            stochastic calculation. Supported values are `1` and `3`. ``1`` is
            considered as ``Fast Stochastic`` and ``3`` is considered as
            ``Slow Stochastic``.

        d_periods (int, default=3): Periods to be used when calculating the
            moving average ``%D`` of ``%K``.

        d_method (str, default='simple'): The moving average to be used when
            calculating ``%D``. Supported values are ``simple`` for Simple
            Moving Average and ``exponential`` for Exponential Moving Average.
            More methods can be supported in a future release.

        fill_missing_values (bool, default=True): If set to True, missing
            values in the input data are being filled.

    Attributes:
        _input_data (pandas.DataFrame): The ``input_data`` after preprocessing.

        _ti_data (pandas.DataFrame): The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains two columns: the stochastic
            oscillator ``%K`` and the moving average of ``%K`` the ``%D``.

        _properties (dict): Indicator properties.

        _calling_instance (str): The name of the class.

    Raises:
        WrongTypeForInputParameter: Input argument has wrong type.
        WrongValueForInputParameter: Unsupported value for input argument.
        NotEnoughInputData: Not enough data for calculating the indicator.
        TypeError: Type error occurred when validating the ``input_data``.
        ValueError: Value error occurred when validating the ``input_data``.
    """
    def __init__(self, input_data, k_periods=14, k_slowing_periods=1,
                 d_periods=3, d_method='simple', fill_missing_values=True):

        # Validate and store if needed, the input parameters
        if isinstance(k_periods, int):
            if k_periods > 0:
                self._k_periods = k_periods
            else:
                raise WrongValueForInputParameter(
                    k_periods, 'k_periods', '>0')
        else:
            raise WrongTypeForInputParameter(
                type(k_periods), 'k_periods', 'int')

        if isinstance(k_slowing_periods, int):
            if k_slowing_periods in [1, 3]:
                self._k_slowing_periods = k_slowing_periods
            else:
                raise WrongValueForInputParameter(
                    k_slowing_periods, 'k_slowing_periods', '1 or 3')
        else:
            raise WrongTypeForInputParameter(
                type(k_slowing_periods), 'k_slowing_periods', 'int')

        if isinstance(d_periods, int):
            if d_periods > 0:
                self._d_periods = d_periods
            else:
                raise WrongValueForInputParameter(
                    d_periods, 'd_periods', '>0')
        else:
            raise WrongTypeForInputParameter(
                type(d_periods), 'd_periods', 'int')

        if isinstance(d_method, str):
            if d_method in ['simple', 'exponential']:
                self._d_method = d_method
            else:
                raise WrongValueForInputParameter(
                    d_method, 'd_method', '\'simple\' or \'exponential\'')
        else:
            raise WrongTypeForInputParameter(type(d_method), 'd_method', 'str')

        # Control is passing to the parent class
        super().__init__(calling_instance=self.__class__.__name__,
                         input_data=input_data,
                         fill_missing_values=fill_missing_values)

    def _calculateTi(self):
        """
        Calculates the technical indicator for the given input data. The input
        data are taken from an attribute of the parent class.

        Raises:
            NotEnoughInputData

        Returns:
            pandas.DataFrame: The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains two columns: the stochastic
            oscillator ``%K`` and the moving average of ``%K`` the ``%D``.

        Raises:
            NotEnoughInputData: Not enough data for calculating the indicator.
        """

        # Not enough data for the requested k_periods
        if len(self._input_data.index) < self._k_periods:
            raise NotEnoughInputData('Stochastic Oscillator', self._k_periods,
                                     len(self._input_data.index))

        so = pd.concat([
            self._input_data,
            self._input_data['low'].rolling(self._k_periods).min(),
            self._input_data['high'].rolling(self._k_periods).max()], axis=1)

        columns_names = list(self._input_data.columns) + ['lowest_low',
                                                          'highest_high']

        so.columns = columns_names

        so = pd.concat([
            so,
            self._input_data['close']-so['lowest_low'],
            so['highest_high']-so['lowest_low']], axis=1)

        columns_names += ['numerator', 'denominator']

        so.columns = columns_names

        so = pd.concat([
            so,
            so['numerator'].rolling(self._k_slowing_periods).sum(),
            so['denominator'].rolling(self._k_slowing_periods).sum()], axis=1)

        columns_names += ['smoothed_numerator', 'smoothed_denominator']

        so.columns = columns_names

        so = round(100*so['smoothed_numerator']/so['smoothed_denominator'], 4)
        so = pd.concat([
            so,
            so.rolling(window=self._d_periods, min_periods=self._d_periods,
                       center=False,
                       win_type=None if self._d_method == 'simple' else
                       self._d_method, on=None, axis=0, closed=None).
            mean().round(4)], axis=1)

        so.columns = ['%K', '%D']

        return so

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

        # A sell signal is given when the oscillator rises above the 80 and
        # then falls below 80.
        if self._ti_data['%K'].iat[-2] > 80. > self._ti_data['%K'].iat[-1] or\
           self._ti_data['%D'].iat[-2] > 80. > self._ti_data['%D'].iat[-1]:
            return TRADE_SIGNALS['sell']

        # A buy signal is given when the oscillator falls below 20 and then
        # rises above 20.
        if self._ti_data['%K'].iat[-2] < 20. < self._ti_data['%K'].iat[-1] or\
           self._ti_data['%D'].iat[-2] < 20. < self._ti_data['%D'].iat[-1]:
            return TRADE_SIGNALS['buy']

        # A sell signal occurs when a decreasing %K line crosses below the %D
        # line in the overbought region (%K > 80.)
        if self._ti_data['%K'].iat[-2] - self._ti_data['%K'].iat[-1] > 0. >\
                self._ti_data['%K'].iat[-1] - self._ti_data['%D'].iat[-1] and\
                self._ti_data['%K'].iat[-1] > 80.:
            return TRADE_SIGNALS['sell']

        # A buy signal occurs when an increasing %K line crosses above the %D
        # line in the  oversold region (%K < 20.)
        if self._ti_data['%K'].iat[-2] - self._ti_data['%K'].iat[-1] < 0. <\
                self._ti_data['%K'].iat[-1] - self._ti_data['%D'].iat[-1] and\
                self._ti_data['%K'].iat[-1] < 20.:
            return TRADE_SIGNALS['buy']

        return TRADE_SIGNALS['hold']
