"""
Trading-Technical-Indicators (tti) python library

File name: <_indicator_name.py>
    Implements the <Indicator Name> technical indicator.
"""

import pandas as pd
import numpy as np

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter

from sklearn.linear_model import LinearRegression


class LinearRegressionIndicator(TechnicalIndicator):
    """
    <Indicator Name> Technical Indicator class implementation.

    Parameters:
        input_data (pandas.DataFrame): The input data.

        period (int, default is 14): The past periods to be used for the
            calculation of the forecast.

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
                It contains one column, the 'lri'. -->
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._period:
            raise NotEnoughInputData('Linear Regression Indicator',
                                     self._period,
                                     len(self._input_data.index))

        lri = pd.DataFrame(index=self._input_data.index,
                           columns=['lri'], data=None,
                           dtype='float64')

        lr = LinearRegression(fit_intercept=True, normalize=False,
                              copy_X=True, n_jobs=None)

        # n-period forecast
        for i in range(self._period, len(self._input_data.index) + 1):

            lr.fit(np.reshape(range(i - self._period, i), (-1, 1)),
                   self._input_data['close'].iloc[i - self._period:i])

            lri['lri'].iat[i - 1] = lr.predict(np.reshape(i - 1, (1, -1)))

        return lri.round(4)

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

        # Close price goes below Linear Regression
        if self._input_data['close'].iat[-2] > self._ti_data['lri'].iat[-2] \
           and \
           self._input_data['close'].iat[-1] < self._ti_data['lri'].iat[-1]:
            return TRADE_SIGNALS['buy']

        # Close price goes above Linear Regression
        if self._input_data['close'].iat[-2] < self._ti_data['lri'].iat[-2] \
           and \
           self._input_data['close'].iat[-1] > self._ti_data['lri'].iat[-1]:
            return TRADE_SIGNALS['sell']

        return TRADE_SIGNALS['hold']
