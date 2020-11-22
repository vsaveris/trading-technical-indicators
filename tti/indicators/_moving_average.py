"""
Trading-Technical-Indicators (tti) python library

File name: _moving_average.py
    Implements the Moving Average (Simple, Exponential, TimeSeries, Triangular,
    and Variable) technical indicator.
"""

import pandas as pd

from ._linear_regression_slope import LinearRegressionSlope
from ._linear_regression_indicator import LinearRegressionIndicator
from ._chande_momentum_oscillator import ChandeMomentumOscillator
from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class MovingAverage(TechnicalIndicator):
    """
    Moving Average Technical Indicator class implementation.

    Parameters:
        input_data (pandas.DataFrame): The input data.

        period (int, default is 200): The past periods to be used for the
            calculation of the moving average. 5-13 days are for Very Short
            Term, 14-25 days are for Short Term, 26-49 days are for Minor
            Intermediate, 50-100 days for Intermediate and 100-200 days are for
            Long Term.

        ma_type (string, 'simple', 'exponential', 'time_series', 'triangular',
            and 'variable', default is 'simple'):
            The type of the calculated moving average.

        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        -

    Raises:
        -
    """
    def __init__(self, input_data, period=200, ma_type='simple',
                 fill_missing_values=True):

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

        if isinstance(ma_type, str):
            if ma_type in ['simple', 'exponential', 'time_series',
                           'triangular', 'variable']:
                self._ma_type = ma_type
            else:
                raise WrongValueForInputParameter(
                    ma_type, 'ma_type',
                    '\'simple\', \'exponential\', \'time_series\', ' +
                    '\'triangular\' or \'variable\'')
        else:
            raise WrongTypeForInputParameter(type(ma_type), 'ma_type', 'str')

        # Control is passing to the parent class
        super().__init__(calling_instance=self.__class__.__name__,
                         input_data=input_data,
                         fill_missing_values=fill_missing_values)

    def _calculateTi(self):
        """
        Calculates the technical indicator for the given input data. The input
        data are taken from an attribute of the parent class.

        Parameters:
            -

        Raises:
            -

        Returns:
            pandas.DataFrame: The calculated indicator. Index is of type date.
                It contains one column, the 'ma'.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._period and \
                self._ma_type != 'variable':
            raise NotEnoughInputData('Moving Average', self._period,
                                     len(self._input_data.index))

        if len(self._input_data.index) < 22 and self._ma_type == 'variable':
            raise NotEnoughInputData('Moving Average (variable)', 22,
                                     len(self._input_data.index))

        ma = pd.DataFrame(index=self._input_data.index,
                          columns=['ma-' + self._ma_type],
                          data=None, dtype='float64')

        if self._ma_type == 'simple':

            ma['ma-' + self._ma_type] = self._input_data.rolling(
                window=self._period, min_periods=self._period, center=False,
                win_type=None, on=None, axis=0, closed=None).mean()

        elif self._ma_type == 'exponential':

            ma['ma-' + self._ma_type] = self._input_data.ewm(
                span=self._period, min_periods=self._period, adjust=False,
                axis=0).mean()

        elif self._ma_type == 'time_series':

            # Similar to Time Series Forecast
            ma['ma-' + self._ma_type].iloc[self._period-1:] = pd.concat(objs=[
                LinearRegressionSlope(input_data=self._input_data,
                                      period=self._period).getTiData(),
                LinearRegressionIndicator(input_data=self._input_data,
                                          period=self._period).getTiData()],
                axis=1).sum(axis=1)

        elif self._ma_type == 'triangular':

            # Simple Moving Average of the Simple Moving Average
            ma['ma-' + self._ma_type] = self._input_data.rolling(
                window=self._period, min_periods=self._period, center=False,
                win_type=None, on=None, axis=0, closed=None).mean().rolling(
                window=self._period, min_periods=self._period, center=False,
                win_type=None, on=None, axis=0, closed=None).mean()

        elif self._ma_type == 'variable':

            # Calculate CMO indicator for 9 periods by default
            cmo = ChandeMomentumOscillator(input_data=self._input_data,
                period=9).getTiData()

            # Calculate Volatility Ratio
            vr = (cmo / 100).abs()

            # Calculate Scaling Multiplier
            sm = 2 / (self._period + 1)

            # By default we start from period 22
            ma['ma-' + self._ma_type].iat[21] = \
                self._input_data['close'].iat[21]

            for i in range(22, len(self._input_data.index)):

                ma['ma-' + self._ma_type].iat[i] = (
                    sm * self._input_data['close'].iat[i] * vr.iat[i, 0]) + (
                    1 - (sm * vr.iat[i, 0])
                ) * ma['ma-' + self._ma_type].iat[i-1]

        return ma.round(4)

    def getTiSignal(self):
        """
        Calculates and returns the signal of the technical indicator. The
        Technical Indicator data are taken from an attribute of the parent
        class.

        Parameters:
            -

        Raises:
            -

        Returns:
            tuple (string, integer): The Trading signal. Possible values are
                ('hold', 0), ('buy', -1), ('sell', 1). See TRADE_SIGNALS
                constant in the tti.utils package, constants.py module.
        """

        # Close price goes below Moving Average
        if ((self._input_data['close'].iat[-2] >
             self._ti_data['ma-' + self._ma_type].iat[-2]) and
                (self._input_data['close'].iat[-1]
                 < self._ti_data['ma-' + self._ma_type].iat[-1])):
            return TRADE_SIGNALS['sell']

        # Close price goes above Moving Average
        if((self._input_data['close'].iat[-2] <
            self._ti_data['ma-' + self._ma_type].iat[-2]) and
                (self._input_data['close'].iat[-1] >
                 self._ti_data['ma-' + self._ma_type].iat[-1])):
            return TRADE_SIGNALS['buy']

        return TRADE_SIGNALS['hold']
