"""
Trading-Technical-Indicators (tti) python library

File name: <_indicator_name.py>
    Implements the <Indicator Name> technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData


class KlingerOscillator(TechnicalIndicator):
    """
    <Indicator Name> Technical Indicator class implementation.

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
                It contains one column, the 'ko'.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < 55:
            raise NotEnoughInputData('Klinger Oscillator', 55,
                                     len(self._input_data.index))

        ko = pd.DataFrame(index=self._input_data.index, columns=['ko'],
                          data=None, dtype='float64')

        # Trend Direction
        t = self._input_data[['high', 'low', 'close']].sum(axis=1) - \
            self._input_data[['high', 'low', 'close']].sum(axis=1).shift(1)
        t[t > 0.0] = 1.0
        t[t <= 0.0] = -1.0

        # Daily Measurement
        dm = self._input_data['high'] - self._input_data['low']

        # Cumulative Measurement
        cm = [0.0]
        for i in range(1, len(self._input_data)):
            if t[i] == t[i - 1]:
                cm.append(cm[i - 1] + dm[i])
            else:
                cm.append(dm[i - 1] + dm[i])

        volume_force = \
            self._input_data['volume'] * abs(2 * (dm / cm) - 1) * t * 100

        ko['ko'] = volume_force.ewm(
            span=34, min_periods=34, adjust=False, axis=0
        ).mean() - volume_force.ewm(
            span=55, min_periods=55, adjust=False, axis=0
        ).mean()

        return ko.round(4)

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

        # Signal based on crossovers with zero line
        if self._ti_data['ko'].iat[-2] < 0.0 < self._ti_data['ko'].iat[-1]:
            return TRADE_SIGNALS['sell']

        if self._ti_data['ko'].iat[-2] > 0.0 > self._ti_data['ko'].iat[-1]:
            return TRADE_SIGNALS['buy']

        return TRADE_SIGNALS['hold']
