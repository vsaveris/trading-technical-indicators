"""
Trading-Technical-Indicators (tti) python library

File name: _range_indicator.py
    Implements the Range Indicator technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class RangeIndicator(TechnicalIndicator):
    """
    Range Indicator Technical Indicator class implementation.

    Parameters:
        input_data (pandas.DataFrame): The input data.

        range_period (int, default is 5): The range periods to be used for the
            calculation of the indicator.

        smoothing_period (int, default is 3): The smoothing periods to be used
            for the calculation of the indicator.

        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        -

    Raises:
        -
    """

    def __init__(self, input_data, range_period=5, smoothing_period=3,
                 fill_missing_values=True):

        # Validate and store if needed, the input parameters
        if isinstance(range_period, int):
            if range_period > 0:
                self._range_period = range_period
            else:
                raise WrongValueForInputParameter(
                    range_period, 'range_period', '>0')
        else:
            raise WrongTypeForInputParameter(
                type(range_period), 'range_period', 'int')

        if isinstance(smoothing_period, int):
            if smoothing_period > 0:
                self._smoothing_period = smoothing_period
            else:
                raise WrongValueForInputParameter(
                    smoothing_period, 'smoothing_period', '>0')
        else:
            raise WrongTypeForInputParameter(
                type(smoothing_period), 'smoothing_period', 'int')

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
                It contains one column, the 'ri'.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < max(
                self._range_period, self._smoothing_period):
            raise NotEnoughInputData('Range Indicator', max(
                self._range_period, self._smoothing_period),
                                     len(self._input_data.index))

        ri = pd.DataFrame(index=self._input_data.index, columns=[
            'true_range', 'see_text', 'see_text_range_min',
            'see_text_range_max', 'see_text_range', 'ri'],
                          data=None, dtype='float64')

        ri['true_range'] = pd.concat(
            [self._input_data['high'] - self._input_data['low'],
             self._input_data['high'] - self._input_data['close'].shift(1),
             self._input_data['close'].shift(1) - self._input_data['low']],
            axis=1).max(axis=1, skipna=False)

        for i in range(1, len(self._input_data.index)):

            if (self._input_data['close'].iat[i] >
                    self._input_data['close'].iat[i - 1]):

                ri['see_text'].iat[i] = ri['true_range'].iat[i] / (
                        self._input_data['close'].iat[i] -
                        self._input_data['close'].iat[i - 1])

            else:
                ri['see_text'].iat[i] = ri['true_range'].iat[i]

        ri['see_text_range_min'] = ri['see_text'].rolling(
            window=self._range_period, min_periods=self._range_period,
            center=False, win_type=None, on=None, axis=0, closed=None).min()

        ri['see_text_range_max'] = ri['see_text'].rolling(
            window=self._range_period, min_periods=self._range_period,
            center=False, win_type=None, on=None, axis=0, closed=None).max()

        ri['see_text_range'] = ri['see_text_range_max'] - \
                               ri['see_text_range_min']

        ri['see_text_range'][ri['see_text_range'] > 0] = 100 * (
                ri['see_text'] - ri['see_text_range_min']
        ) / (ri['see_text_range_max'] - ri['see_text_range_min'])

        ri['see_text_range'][ri['see_text_range'] <= 0] = 100 * (
                ri['see_text'] - ri['see_text_range_min'])

        ri['ri'] = ri['see_text_range'].ewm(
            span=self._smoothing_period, min_periods=self._smoothing_period,
            adjust=False, axis=0).mean()

        return ri[['ri']].round(4)

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

        # Not enough data for trading signal
        if len(self._input_data.index) < 2:
            return TRADE_SIGNALS['hold']

        # Indication that a new trend starts
        if self._ti_data['ri'].iat[-2] < 20 < self._ti_data['ri'].iat[-1]:
            if (self._input_data['close'].iat[-2] <
                    self._input_data['close'].iat[-1]):
                return TRADE_SIGNALS['buy']
            else:
                return TRADE_SIGNALS['sell']

        # Indication that current trend ends
        if self._ti_data['ri'].iat[-2] < 70 < self._ti_data['ri'].iat[-1]:
            try:
                if (self._input_data['close'][
                    self._ti_data['ri'] < 20].iat[-1] <
                        self._input_data['close'].iat[-1]):
                    return TRADE_SIGNALS['sell']
                else:
                    return TRADE_SIGNALS['buy']
            except KeyError:
                return TRADE_SIGNALS['hold']

        return TRADE_SIGNALS['hold']
