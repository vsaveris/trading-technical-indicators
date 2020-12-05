"""
Trading-Technical-Indicators (tti) python library

File name: _envelopes.py
    Implements the Envelopes technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class Envelopes(TechnicalIndicator):
    """
    Envelopes Technical Indicator class implementation.

    Args:
        input_data (pandas.DataFrame): The input data. Required input column
            is ``close``. The index is of type ``pandas.DatetimeIndex``.

        period (int, default=20): The past periods to be used for the
            calculation of the moving average.

        shift (float, default=0.10): The shift percentage to be applied.

        fill_missing_values (bool, default=True): If set to True, missing
            values in the input data are being filled.

    Attributes:
        _input_data (pandas.DataFrame): The ``input_data`` after preprocessing.

        _ti_data (pandas.DataFrame): The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains two columns, the
            ``upper_band`` and the ``lower_band``.

        _properties (dict): Indicator properties.

        _calling_instance (str): The name of the class.

    Raises:
        WrongTypeForInputParameter: Input argument has wrong type.
        WrongValueForInputParameter: Unsupported value for input argument.
        NotEnoughInputData: Not enough data for calculating the indicator.
        TypeError: Type error occurred when validating the ``input_data``.
        ValueError: Value error occurred when validating the ``input_data``.
    """
    def __init__(self, input_data, period=20, shift=0.10,
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

        if isinstance(shift, float):
            if 1.0 > shift > 0.0:
                self._shift = shift
            else:
                raise WrongValueForInputParameter(
                    period, 'shift', '>0.0 and <1.0')
        else:
            raise WrongTypeForInputParameter(
                type(period), 'shift', 'float')

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
            ``pandas.DatetimeIndex``. It contains two columns, the
            ``upper_band`` and the ``lower_band``.

        Raises:
            NotEnoughInputData: Not enough data for calculating the indicator.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._period:
            raise NotEnoughInputData('Envelopes', self._period,
                                     len(self._input_data.index))

        env = pd.DataFrame(index=self._input_data.index,
                           columns=['upper_band', 'lower_band'], data=0,
                           dtype='float64')

        ma = self._input_data.rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).mean()

        env['upper_band'] = (1 + self._shift) * ma
        env['lower_band'] = (1 - self._shift) * ma

        return env.round(4)

    def getTiSignal(self):
        """
        Calculates and returns the trading signal for the calculated technical
        indicator.

        Returns:
            {('hold', 0), ('buy', -1), ('sell', 1)}: The calculated trading
            signal.
        """

        # Not enough data for calculating trading signal
        if len(self._ti_data.index) < 1:
            return TRADE_SIGNALS['hold']

        # Price goes above upper band
        if self._input_data['close'].iat[-1] > \
                self._ti_data['upper_band'].iat[-1]:
            return TRADE_SIGNALS['sell']

        # Price goes below lower band
        elif self._input_data['close'].iat[-1] < \
                self._ti_data['lower_band'].iat[-1]:
            return TRADE_SIGNALS['buy']

        else:
            return TRADE_SIGNALS['hold']
