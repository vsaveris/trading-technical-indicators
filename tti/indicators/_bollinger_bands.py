"""
Trading-Technical-Indicators (tti) python library

File name: _bollinger_bands.py
    Implements the Bollinger Bands technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class BollingerBands(TechnicalIndicator):
    """
    Bollinger Bands Technical Indicator class implementation.

    Args:
        input_data (pandas.DataFrame): The input data. Required input columns
            is ``close``. The index is of type ``pandas.DatetimeIndex``.

        period (int, default=20): The past periods to be used for the
            calculation of the middle band (simple moving average).

        std_number (int, default=2): The number of standard deviations to
            be used for calculating the upper and lower bands.

        fill_missing_values (bool, default=True): If set to True, missing
            values in the input data are being filled.

    Attributes:
        _input_data (pandas.DataFrame): The ``input_data`` after preprocessing.

        _ti_data (pandas.DataFrame): The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains three columns, the
            ``middle_band``, ``upper_band`` and ``lower_band``.

        _properties (dict): Indicator properties.

        _calling_instance (str): The name of the class.

    Raises:
        WrongTypeForInputParameter: Input argument has wrong type.
        WrongValueForInputParameter: Unsupported value for input argument.
        NotEnoughInputData: Not enough data for calculating the indicator.
        TypeError: Type error occurred when validating the ``input_data``.
        ValueError: Value error occurred when validating the ``input_data``.
    """
    def __init__(self, input_data, period=20, std_number=2,
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

        if isinstance(std_number, (int, float)):
            if std_number > 0.0:
                self._std_number = std_number
            else:
                raise WrongValueForInputParameter(
                    std_number, 'std_number', '>0')
        else:
            raise WrongTypeForInputParameter(
                type(std_number), 'std_number', 'int or float')

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
            ``pandas.DatetimeIndex``. It contains three columns, the
            ``middle_band``, ``upper_band`` and ``lower_band``.

        Raises:
            NotEnoughInputData: Not enough data for calculating the indicator.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._period:
            raise NotEnoughInputData('Bollinger Bands', self._period,
                                     len(self._input_data.index))

        # Calculate the Middle Band using Simple Moving Average
        bb = self._input_data.rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).mean().round(4)

        # Calculate Upper and Lower Bands
        standard_deviation = self._input_data.rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).std(ddof=0)

        bb = pd.concat([bb,
                        round(bb + standard_deviation * self._std_number, 4),
                        round(bb - standard_deviation * self._std_number, 4)],
                       axis=1)

        bb.columns = ['middle_band', 'upper_band', 'lower_band']

        return bb

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
