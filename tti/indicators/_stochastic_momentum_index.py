"""
Trading-Technical-Indicators (tti) python library

File name: _stochastic_momentum_index.py
    Implements the Stochastic Momentum Index technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class StochasticMomentumIndex(TechnicalIndicator):
    """
    Stochastic Momentum Index Technical Indicator class implementation.

    Parameters:
        input_data (pandas.DataFrame): The input data.

        period (int, default is 5): The past periods to be used for the
            calculation of the indicator.

        smoothing_period (int, default is 3): The number of periods to be used
            when smoothing.

        double_smoothing_period (int, default is 3): The number of periods to
            be used when double smoothing.


        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        -

    Raises:
        -
    """
    def __init__(self, input_data, period=5, smoothing_period=3,
                 double_smoothing_period=3, fill_missing_values=True):

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

        if isinstance(smoothing_period, int):
            if smoothing_period > 0:
                self._smoothing_period = smoothing_period
            else:
                raise WrongValueForInputParameter(
                    smoothing_period, 'smoothing_period', '>0')
        else:
            raise WrongTypeForInputParameter(
                type(smoothing_period), 'smoothing_period', 'int')

        if isinstance(double_smoothing_period, int):
            if double_smoothing_period > 0:
                self._double_smoothing_period = double_smoothing_period
            else:
                raise WrongValueForInputParameter(
                    double_smoothing_period, 'double_smoothing_period', '>0')
        else:
            raise WrongTypeForInputParameter(
                type(double_smoothing_period), 'double_smoothing_period',
                'int')

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
                It contains one column, the 'smi'.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._period:
            raise NotEnoughInputData('Stochastic Momentum Index', self._period,
                                     len(self._input_data.index))

        smi = pd.DataFrame(index=self._input_data.index, columns=['smi'],
                           data=None, dtype='float64')

        # Calculate highest high for the last periods
        smi['highest_high'] = self._input_data['high'].rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).max()

        # Calculate highest high for the last periods
        smi['lowest_low'] = self._input_data['low'].rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).min()

        # Midpoint between highest high and lowest low
        smi['midpoint'] = (smi['highest_high'] + smi['lowest_low']) / 2

        # Distance of Close from Midpoint
        smi['distance'] = self._input_data['close'] - smi['midpoint']

        # Exponential Moving Average of the distance
        smi['distance_ema'] = smi['distance'].ewm(
            span=self._smoothing_period, min_periods=self._smoothing_period,
            adjust=False, axis=0).mean()

        # Double Exponential Moving Average of the distance
        smi['distance_double_ema'] = smi['distance_ema'].ewm(
            span=self._double_smoothing_period,
            min_periods=self._double_smoothing_period, adjust=False, axis=0
        ).mean()

        # Difference between highest high and lowest low
        smi['hh_ll_diff'] = smi['highest_high'] - smi['lowest_low']

        # Exponential Moving Average of the difference between highest high and
        # lowest low
        smi['hh_ll_diff_ema'] = smi['hh_ll_diff'].ewm(
            span=self._smoothing_period, min_periods=self._smoothing_period,
            adjust=False, axis=0).mean()

        # Double Exponential Moving Average of the difference between highest
        # high and lowest low
        smi['hh_ll_diff_double_ema'] = smi['hh_ll_diff_ema'].ewm(
            span=self._double_smoothing_period,
            min_periods=self._double_smoothing_period, adjust=False, axis=0
        ).mean()

        # Calculate SMI
        smi['smi'] = 100 * (smi['distance_double_ema'] / (
                0.5 * smi['hh_ll_diff_double_ema']))

        return smi[['smi']].round(4)

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

        # Buy when SMI falls below -40
        if self._ti_data['smi'].iat[-2] > -40. > self._ti_data['smi'].iat[-1]:
            return TRADE_SIGNALS['buy']

        # Sell when SMI raises above +40
        if self._ti_data['smi'].iat[-2] < 40. < self._ti_data['smi'].iat[-1]:
            return TRADE_SIGNALS['sell']

        return TRADE_SIGNALS['hold']
