"""
Trading-Technical-Indicators (tti) python library

File name: _relative_volatility_index.py
    Implements the Relative Volatility Index technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class RelativeVolatilityIndex(TechnicalIndicator):
    """
    Relative Volatility Index Technical Indicator class implementation.

    Args:
        input_data (pandas.DataFrame): The input data. Required input columns
            are ``high``, ``low``. The index is of type
            ``pandas.DatetimeIndex``.

        period (int, default=5): The past periods to be used for the
            calculation of the indicator.

        fill_missing_values (bool, default=True): If set to True, missing
            values in the input data are being filled.

    Attributes:
        _input_data (pandas.DataFrame): The ``input_data`` after preprocessing.

        _ti_data (pandas.DataFrame): The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains one column, the ``rvi``.

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
            ``pandas.DatetimeIndex``. It contains one column, the ``rvi``.

        Raises:
            NotEnoughInputData: Not enough data for calculating the indicator.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._period + 10:
            raise NotEnoughInputData('Relative Volatility Index',
                                     self._period + 10,
                                     len(self._input_data.index))

        rvi = pd.DataFrame(index=self._input_data.index,
                           columns=['rvi', 'uh', 'ul', 'dh', 'dl',
                                    'smoothed_uh', 'smoothed_ul',
                                    'smoothed_dh', 'smoothed_dl',
                                    'rvih', 'rvil'],
                           data=None, dtype='float64')

        high_change = self._input_data['high'] - self._input_data['high'].\
            shift(1)

        low_change = self._input_data['low'] - self._input_data['low']. \
            shift(1)

        # Upward high and low change
        rvi['uh'] = 0.0
        rvi['uh'][high_change > 0] = self._input_data['high'].rolling(
            window=10, min_periods=10, center=False, win_type=None, on=None,
            axis=0, closed=None).std(ddof=0)

        rvi['ul'] = 0.0
        rvi['ul'][low_change > 0] = self._input_data['low'].rolling(
            window=10, min_periods=10, center=False, win_type=None, on=None,
            axis=0, closed=None).std(ddof=0)

        # Downward high and low change
        rvi['dh'] = 0.0
        rvi['dh'][high_change < 0] = self._input_data['high'].rolling(
            window=10, min_periods=10, center=False, win_type=None, on=None,
            axis=0, closed=None).std(ddof=0)

        rvi['dl'] = 0.0
        rvi['dl'][low_change < 0] = self._input_data['low'].rolling(
            window=10, min_periods=10, center=False, win_type=None, on=None,
            axis=0, closed=None).std(ddof=0)

        # Wilder's Moving Average for uh, ul and dh, dl
        rvi['smoothed_uh'].iat[9 + self._period - 1] = \
            rvi['uh'].iloc[9:self._period + 9].mean()

        rvi['smoothed_dh'].iat[9 + self._period - 1] = \
            rvi['dh'].iloc[9:self._period + 9].mean()

        rvi['smoothed_ul'].iat[9 + self._period - 1] = \
            rvi['ul'].iloc[9:self._period + 9].mean()

        rvi['smoothed_dl'].iat[9 + self._period - 1] = \
            rvi['dl'].iloc[9:self._period + 9].mean()

        for i in range(self._period + 9, len(self._input_data.index)):
            rvi['smoothed_uh'].iat[i] = rvi['smoothed_uh'].iat[i - 1] + (
                    rvi['uh'].iat[i] - rvi['smoothed_uh'].iat[i - 1]
            ) / self._period

            rvi['smoothed_dh'].iat[i] = rvi['smoothed_dh'].iat[i - 1] + (
                    rvi['dh'].iat[i] - rvi['smoothed_dh'].iat[i - 1]
            ) / self._period

            rvi['smoothed_ul'].iat[i] = rvi['smoothed_ul'].iat[i - 1] + (
                    rvi['ul'].iat[i] - rvi['smoothed_ul'].iat[i - 1]
            ) / self._period

            rvi['smoothed_dl'].iat[i] = rvi['smoothed_dl'].iat[i - 1] + (
                    rvi['dl'].iat[i] - rvi['smoothed_dl'].iat[i - 1]
            ) / self._period

        # Calculate RVI High and Low
        rvi['rvih'] = 100 * rvi['smoothed_uh'] / (
                rvi['smoothed_uh'] + rvi['smoothed_dh'])

        rvi['rvil'] = 100 * rvi['smoothed_ul'] / (
                rvi['smoothed_ul'] + rvi['smoothed_dl'])

        # Calculate indicator
        rvi['rvi'] = (rvi['rvih'] + rvi['rvil']) / 2

        return rvi[['rvi']].round(4)

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

        if self._ti_data['rvi'].iat[-2] > 40 > self._ti_data['rvi'].iat[-1]:
            return TRADE_SIGNALS['buy']

        if self._ti_data['rvi'].iat[-2] < 60 < self._ti_data['rvi'].iat[-1]:
            return TRADE_SIGNALS['sell']

        return TRADE_SIGNALS['hold']
