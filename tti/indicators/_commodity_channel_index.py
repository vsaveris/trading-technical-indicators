"""
Trading-Technical-Indicators (tti) python library

File name: _commodity_channel_index.py
    Implements the Commodity Channel Index technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class CommodityChannelIndex(TechnicalIndicator):
    """
    Commodity Channel Index Technical Indicator class implementation.

    Parameters:
        input_data (pandas.DataFrame): The input data.

        period (int, default is 5): The past periods to be used for the
            calculation of the indicator.

        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        -

    Raises:
        -
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

        Parameters:
            -

        Raises:
            -

        Returns:
            pandas.DataFrame: The calculated indicator. Index is of type date.
                It contains one column, the 'cci'.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._period:
            raise NotEnoughInputData('Commodity Channel Index',  self._period,
                                     len(self._input_data.index))

        cci = pd.DataFrame(index=self._input_data.index, columns=['cci'],
                          data=0, dtype='float64')

        # Average of high, low and close
        typical_price = self._input_data.sum(axis=1) / 3.

        # Simple moving average of the typical price
        tp_sma = typical_price.rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).mean()

        # Sum of absolute differences of the typical price sma from preceding
        # periods typical prices
        differences = pd.concat(
            [tp_sma, typical_price], axis=1).iloc[:].pipe(
            self._rolling_pipe, self._period,
            lambda x: sum([abs(x[0][self._period - 1] - x[1][i])
                           for i in range(self._period)]))

        cci['cci'] = \
            (typical_price - tp_sma) / (0.015 * differences / self._period)

        return cci.round(4)

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

        # Oversold area
        if self._ti_data['cci'].iat[-1] < -100:
            return TRADE_SIGNALS['buy']

        # Overbought area
        elif self._ti_data['cci'].iat[-1] > 100:
            return TRADE_SIGNALS['sell']

        else:
            return TRADE_SIGNALS['hold']
