"""
Trading-Technical-Indicators (tti) python library

File name: _linear_regression_slope.py
    Implements the Linear Regression Slope technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class LinearRegressionSlope(TechnicalIndicator):
    """
    Linear Regression Slope Technical Indicator class implementation.

    Parameters:
        input_data (pandas.DataFrame): The input data.

        period (int, default is 200): The past periods to be used for the
            calculation of the indicator.

        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        -

    Raises:
        -
    """
    def __init__(self, input_data, period=14, fill_missing_values=True):

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

        Parameters:
            -

        Raises:
            -

        Returns:
            pandas.DataFrame: The calculated indicator. Index is of type date.
                It contains one column, the 'lrs'.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._period:
            raise NotEnoughInputData('Linear Regression Slope',
                                     self._period,
                                     len(self._input_data.index))

        lrs = pd.DataFrame(index=self._input_data.index, columns=['lrs'],
                           data=0.0, dtype='float64')

        xy = (self._input_data['close'] *
              range(1, len(self._input_data.index) + 1)
              ).rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).sum()

        x = pd.Series(
            index=self._input_data.index,
            data=range(1, len(self._input_data.index) + 1)
        ).rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).sum()

        xx = pd.Series(
            index=self._input_data.index,
            data=[x**2 for x in range(1, len(self._input_data.index) + 1)]
        ).rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).sum()

        y = self._input_data['close'].rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).sum()

        lrs['lrs'] = \
            (self._period * xy - (x * y)) / ((self._period * xx) - (x * x))

        return lrs.round(4)

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

        # Slope becomes positive
        if self._ti_data['lrs'].iat[-2] < 0.0 < self._ti_data['lrs'].iat[-1]:
            return TRADE_SIGNALS['sell']

        # Slope becomes negative
        elif self._ti_data['lrs'].iat[-2] > 0.0 > self._ti_data['lrs'].iat[-1]:
            return TRADE_SIGNALS['buy']

        else:
            return TRADE_SIGNALS['hold']
