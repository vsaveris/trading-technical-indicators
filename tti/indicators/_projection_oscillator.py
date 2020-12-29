"""
Trading-Technical-Indicators (tti) python library

File name: _projection_oscillator.py
    Implements the Projection Oscillator technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ._projection_bands import ProjectionBands
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import WrongTypeForInputParameter,\
    WrongValueForInputParameter, NotEnoughInputData


class ProjectionOscillator(TechnicalIndicator):
    """
    Projection Oscillator Technical Indicator class implementation.

    Args:
        input_data (pandas.DataFrame): The input data. Required input columns
            are ``high``, ``low``, ``close``. The index is of type
            ``pandas.DatetimeIndex``.

        period (int, default=14): The past periods to be used for the
            calculation of the indicator.

        fill_missing_values (bool, default=True): If set to True, missing
            values in the input data are being filled.

    Attributes:
        _input_data (pandas.DataFrame): The ``input_data`` after preprocessing.

        _ti_data (pandas.DataFrame): The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains two columns, the ``posc`` and
            the ``trigger_line``.

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
            if period > 1:
                self._period = period
            else:
                raise WrongValueForInputParameter(
                    period, 'period', '>1')
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
            ``pandas.DatetimeIndex``. It contains two columns, the ``posc`` and
            the ``trigger_line``.

        Raises:
            NotEnoughInputData: Not enough data for calculating the indicator.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._period:
            raise NotEnoughInputData('Projection Oscillator', self._period,
                                     len(self._input_data.index))

        # Calculate Projection Bands
        projection_bands = ProjectionBands(input_data=self._input_data,
                                           period=self._period).getTiData()

        posc = pd.DataFrame(index=self._input_data.index,
                            columns=['posc', 'trigger_line'],
                            data=None, dtype='float64')

        posc['posc'] = 100 * (
                self._input_data['close'] - projection_bands['lower_band']) / (
            projection_bands['upper_band'] - projection_bands['lower_band']
        )

        # Trigger line, Exponential Moving Average of three days, can be an
        # input argument to the class constructor in a later release
        posc['trigger_line'] = posc['posc'] .ewm(
            span=3, min_periods=3, adjust=False, axis=0).mean()

        return posc.round(4)

    def getTiSignal(self):
        """
        Calculates and returns the trading signal for the calculated technical
        indicator.

        Returns:
            {('hold', 0), ('buy', -1), ('sell', 1)}: The calculated trading
            signal.
        """

        # Not enough data for trading signal
        if len(self._ti_data.index) < 4:
            return TRADE_SIGNALS['hold']

        # Signals based on Overbought / Oversold Regions
        if self._ti_data['posc'].iat[-2] < 15 < self._ti_data['posc'].iat[-1]:
            return TRADE_SIGNALS['buy']

        if self._ti_data['posc'].iat[-2] > 85 > self._ti_data['posc'].iat[-1]:
            return TRADE_SIGNALS['sell']

        # Signals based on Crossovers
        if ((self._ti_data['posc'].iat[-4] <
             self._ti_data['trigger_line'].iat[-4]) and
                (self._ti_data['posc'].iat[-3] <
                 self._ti_data['trigger_line'].iat[-3]) and
                (self._ti_data['posc'].iat[-2] >
                 self._ti_data['trigger_line'].iat[-2]) and
                (self._ti_data['posc'].iat[-1] >
                 self._ti_data['trigger_line'].iat[-1])):
            return TRADE_SIGNALS['buy']

        if ((self._ti_data['posc'].iat[-4] >
             self._ti_data['trigger_line'].iat[-4]) and
                (self._ti_data['posc'].iat[-3] >
                 self._ti_data['trigger_line'].iat[-3]) and
                (self._ti_data['posc'].iat[-2] <
                 self._ti_data['trigger_line'].iat[-2]) and
                (self._ti_data['posc'].iat[-1] <
                 self._ti_data['trigger_line'].iat[-1])):
            return TRADE_SIGNALS['sell']

        return TRADE_SIGNALS['hold']
