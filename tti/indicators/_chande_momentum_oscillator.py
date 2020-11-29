"""
Trading-Technical-Indicators (tti) python library

File name: _chande_momentum_oscillator.py
    Implements the Chande Momentum Oscillator technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class ChandeMomentumOscillator(TechnicalIndicator):
    """
    Chande Momentum Oscillator Technical Indicator class implementation.

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
                It contains one column, the 'cmo'.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._period:
            raise NotEnoughInputData('Chande Momentum Oscillator',
                                     self._period,
                                     len(self._input_data.index))

        cmo = pd.DataFrame(index=self._input_data.index, columns=['cmo'],
                           data=0, dtype='float64')

        # Up movement changes
        up_move_changes = self._input_data.diff(periods=1)
        up_move_changes[up_move_changes < 0.0] = 0.0

        # Calculate the periods sum for the up movement changes
        up_move_changes = up_move_changes.rolling(
            window=self._period, min_periods=self._period).sum()

        # Down movement changes
        down_move_changes = self._input_data.diff(periods=1)
        down_move_changes[down_move_changes > 0.0] = 0.0

        # Calculate the absolute periods sum for the down movement changes
        down_move_changes = down_move_changes.rolling(
            window=self._period, min_periods=self._period).sum().abs()

        cmo['cmo'] = 100 * (up_move_changes - down_move_changes) / \
                           (up_move_changes + down_move_changes)

        return cmo.round(4)

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

        # Not enough data for calculating trading signal
        if len(self._ti_data.index) < 2:
            return TRADE_SIGNALS['hold']

        # Overbought region
        if self._ti_data['cmo'].iat[-2] < 50. < self._ti_data['cmo'].iat[-1]:
            return TRADE_SIGNALS['sell']

        # Oversold region
        if self._ti_data['cmo'].iat[-2] > -50. > self._ti_data['cmo'].iat[-1]:
            return TRADE_SIGNALS['buy']

        return TRADE_SIGNALS['hold']
