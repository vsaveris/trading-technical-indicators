"""
Trading-Technical-Indicators (tti) python library

File name: _ichimoku_cloud.py
    Implements the Ichimoku Cloud technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS


class IchimokuCloud(TechnicalIndicator):
    """
    Ichimoku Cloud Technical Indicator class implementation.

    Parameters:
        input_data (pandas.DataFrame): The input data.

        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        -

    Raises:
        -
    """
    def __init__(self, input_data, fill_missing_values=True):

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
                It contains four columns the 'tenkan_sen', 'kijun_sen',
                'senkou_a', 'senkou_b'.
        """

        # Build the indicator's dataframe
        ic = pd.DataFrame(index = input_data.index, columns = ['Tenkan Sen',
            'Kijun Sen', 'Senkou A', 'Senkou B'], data = None)

        ic['Tenkan Sen'] = (input_data['High'].rolling(window = 9,
            min_periods = 1).max() + input_data['Low'].rolling(window = 9,
            min_periods = 1).min())/2

        ic['Kijun Sen'] = (input_data['High'].rolling(window = 26,
            min_periods = 1).max() + input_data['Low'].rolling(window = 26,
            min_periods = 1).min())/2

        # Is optional, not needed in this version of the indicator. Column
        # removed also from the ic dataframe definition.
        #ic['Chiku Span'] = input_data['Adj Close'].shift(-26)

        ic['Senkou A'] = ((ic['Tenkan Sen'] + ic['Kijun Sen'])/2).shift(26)

        ic['Senkou B'] = ((input_data['High'].rolling(window = 52,
            min_periods = 1).max() + input_data['Low'].rolling(window = 52,
            min_periods = 1).min())/2).shift(26)

        return ic


        obv = pd.DataFrame(index=self._input_data.index, columns=['OBV'],
                           data=None, dtype='int64')

        obv.iat[0, 0] = 0
        for i in range(1, len(self._input_data.index)):

            # Today's close is greater than yesterday's close
            if self._input_data['close'].iat[i] > \
                    self._input_data['close'].iat[i - 1]:
                obv.iat[i, 0] = obv.iat[i - 1, 0] + \
                                self._input_data['volume'].iat[i]

            # Today's close is less than yesterday's close
            elif self._input_data['close'].iat[i] < \
                    self._input_data['close'].iat[i - 1]:
                obv.iat[i, 0] = obv.iat[i - 1, 0] - \
                                self._input_data['volume'].iat[i]

            # Today's close is equal the yesterday's close
            else:
                obv.iat[i, 0] = obv.iat[i - 1, 0]

        return obv

    def _whereInCloud(self, value, cloud):
        '''
        Checks the relative position of the value to the cloud.

        Args:
            value (pfloat): The value for which the relative position to the
                cloud should be calculated.

            cloud (list of two floats): Bounds of the cloud in not guaranteed
                order.

        Raises:
            -

        Returns:
            int: 0 means that value is within the cloud, 1 means that value
                is above the cloud, -1 means that value is below the cloud.
        '''

        ordered_values = cloud + [value]
        ordered_values.sort()

        return ordered_values.index(value) - 1

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

        # A buy signal is reinforced when the Tenkan Sen crosses above the Kijun
        # Sen while the Tenkan Sen, Kijun Sen, and price are all above the cloud
        if self._ti_data.iat[-1, 0] > self._ti_data.iat[-1, 1] and \
                self._whereInCloud(
                    self._input_data['Adj Close'].to_frame().iat[-1, 0],
                    [self._ti_data.iat[-1, 2],
                     self._ti_data.iat[-1, 3]]) == 1 and \
                self._whereInCloud(self._ti_data.iat[-1, 0],
                                   [self._ti_data.iat[-1, 2],
                                    self._ti_data.iat[-1, 3]]) == 1 and \
                self._whereInCloud(self._ti_data.iat[-1, 1],
                                   [self._ti_data.iat[-1, 2],
                                    self._ti_data.iat[-1, 3]]) == 1:
            return ('Buy', TRADE_SIGNALS['Buy'])

        # A sell signal is reinforced when the TenKan Sen crosses below the
        # Kijun Sen while the Tenkan Sen, Kijun Sen, and price are all below the
        # cloud.
        if self._ti_data.iat[-1, 0] < self._ti_data.iat[-1, 1] and \
                self._whereInCloud(
                    self._input_data['Adj Close'].to_frame().iat[-1, 0],
                    [self._ti_data.iat[-1, 2],
                     self._ti_data.iat[-1, 3]]) == -1 and \
                self._whereInCloud(self._ti_data.iat[-1, 0],
                                   [self._ti_data.iat[-1, 2],
                                    self._ti_data.iat[-1, 3]]) == -1 and \
                self._whereInCloud(self._ti_data.iat[-1, 1],
                                   [self._ti_data.iat[-1, 2],
                                    self._ti_data.iat[-1, 3]]) == -1:
            return ('Sell', TRADE_SIGNALS['Sell'])

        return ('Hold', TRADE_SIGNALS['Hold'])


        # Trading signals on warnings for breakout (upward or downward)
        # 3-days period is used for trend calculation

        # Not enough data for calculating trading signal
        if len(self._ti_data.index) < 3:
            return TRADE_SIGNALS['hold']

        # Warning for a downward breakout
        if self._ti_data['OBV'].iat[-3] > self._ti_data['OBV'].iat[-2] > \
                self._ti_data['OBV'].iat[-1]:
            return TRADE_SIGNALS['buy']

        # Warning for a upward breakout
        elif self._ti_data['OBV'].iat[-3] < self._ti_data['OBV'].iat[-2] < \
                self._ti_data['OBV'].iat[-1]:
            return TRADE_SIGNALS['sell']

        else:
            return TRADE_SIGNALS['hold']
