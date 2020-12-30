"""
Trading-Technical-Indicators (tti) python library

File name: _time_series_forecast.py
    Implements the Time Series Forecast technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ._linear_regression_slope import LinearRegressionSlope
from ._linear_regression_indicator import LinearRegressionIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class TimeSeriesForecast(TechnicalIndicator):
    """
    Time Series Forecast Technical Indicator class implementation.

    Args:
        input_data (pandas.DataFrame): The input data. Required input column
            is ``close``. The index is of type ``pandas.DatetimeIndex``.

        period (int, default=14): The past periods to be used for the
            calculation of the indicator.

        fill_missing_values (bool, default=True): If set to True, missing
            values in the input data are being filled.

    Attributes:
        _input_data (pandas.DataFrame): The ``input_data`` after preprocessing.

        _ti_data (pandas.DataFrame): The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains one column, the ``tsf``.

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
            ``pandas.DatetimeIndex``. It contains one column, the ``tsf``.

        Raises:
            NotEnoughInputData: Not enough data for calculating the indicator.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._period:
            raise NotEnoughInputData('Time Series Forecast',
                                     self._period,
                                     len(self._input_data.index))

        tsf = pd.DataFrame(index=self._input_data.index, columns=['tsf'],
                           data=None, dtype='float64')

        tsf['tsf'].iloc[self._period-1:] = pd.concat(
            objs=[LinearRegressionSlope(input_data=self._input_data,
                                        period=self._period).getTiData(),
                  LinearRegressionIndicator(input_data=self._input_data,
                                            period=self._period).getTiData()],
            axis=1).sum(axis=1).iloc[self._period-1:]

        return tsf.round(4)

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

        # Close price goes below Time Series Forecast
        if self._input_data['close'].iat[-2] > self._ti_data['tsf'].iat[-2] \
           and \
           self._input_data['close'].iat[-1] < self._ti_data['tsf'].iat[-1]:
            return TRADE_SIGNALS['buy']

        # Close price goes above Time Series Forecast
        if self._input_data['close'].iat[-2] < self._ti_data['tsf'].iat[-2] \
           and \
           self._input_data['close'].iat[-1] > self._ti_data['tsf'].iat[-1]:
            return TRADE_SIGNALS['sell']

        return TRADE_SIGNALS['hold']
