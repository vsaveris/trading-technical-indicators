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
        ic = pd.DataFrame(
            index=self._input_data.index,
            columns=['tenkan_sen', 'kijun_sen', 'senkou_a', 'senkou_b'],
            data=None)

        ic['tenkan_sen'] = (self._input_data['high'].
                            rolling(window=9, min_periods=1).max() +
                            self._input_data['low'].
                            rolling(window=9, min_periods=1).min()) / 2

        ic['kijun_sen'] = (self._input_data['high'].
                           rolling(window=26, min_periods=1).max() +
                           self._input_data['low'].
                           rolling(window=26, min_periods=1).min()) / 2

        ic['senkou_a'] = ((ic['tenkan_sen'] + ic['kijun_sen']) / 2).shift(26)

        ic['senkou_b'] = ((self._input_data['high'].
                           rolling(window=52, min_periods=1).max() +
                           self._input_data['low'].
                           rolling(window=52, min_periods=1).min()) / 2).\
            shift(26)

        return ic.round(4)

    @staticmethod
    def _whereInCloud(value, cloud):
        """
        Checks the relative position of the value to the cloud.

        Parameters:
            value (float): The value for which the relative position to the
                cloud should be calculated.

            cloud (list of two floats): Bounds of the cloud in a not guaranteed
                order.

        Raises:
            -

        Returns:
            int: 0 means that value is within the cloud, 1 means that value
                is above the cloud, -1 means that value is below the cloud.
        """

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

        # Not enough data for calculating a trading signal
        if len(self._input_data.index) < 2:
            return TRADE_SIGNALS['hold']

        # If 3 all 'close', 'tenkan_sen' and 'kijun_sen' are above the cloud
        # if -3 all 'close', 'tenkan_sen' and 'kijun_sen' are below the cloud
        position_in_cloud = \
            self._whereInCloud(self._input_data['close'].iat[-1],
                               [self._ti_data['senkou_a'].iat[-1],
                                self._ti_data['senkou_b'].iat[-1]]) + \
            self._whereInCloud(self._ti_data['tenkan_sen'].iat[-1],
                               [self._ti_data['senkou_a'].iat[-1],
                                self._ti_data['senkou_b'].iat[-1]]) + \
            self._whereInCloud(self._ti_data['kijun_sen'].iat[-1],
                               [self._ti_data['senkou_a'].iat[-1],
                                self._ti_data['senkou_b'].iat[-1]])

        # A buy signal is reinforced when the Tenkan Sen crosses above the
        # Kijun Sen while the Tenkan Sen, Kijun Sen, and price are all above
        # the cloud
        if self._ti_data['tenkan_sen'].iat[-2] < self._ti_data['kijun_sen']. \
                iat[-2] and \
           self._ti_data['tenkan_sen'].iat[-1] > self._ti_data['kijun_sen']. \
                iat[-1] and \
           position_in_cloud == 3:

            return TRADE_SIGNALS['buy']

        # A sell signal is reinforced when the TenKan Sen crosses below the
        # Kijun Sen while the Tenkan Sen, Kijun Sen, and price are all below
        # the cloud.
        if self._ti_data['tenkan_sen'].iat[-2] > self._ti_data['kijun_sen']. \
                iat[-2] and \
           self._ti_data['tenkan_sen'].iat[-1] < self._ti_data['kijun_sen']. \
                iat[-1] and \
           position_in_cloud == -3:

            return TRADE_SIGNALS['sell']

        return TRADE_SIGNALS['hold']
