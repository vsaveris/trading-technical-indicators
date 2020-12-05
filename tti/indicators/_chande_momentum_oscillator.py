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

    Args:
        input_data (pandas.DataFrame): The input data. Required input columns
            is``close``. The index is of type ``pandas.DatetimeIndex``.

        period (int, default=5): The past periods to be used for the
            calculation of the indicator.

        fill_missing_values (bool, default=True): If set to True, missing
            values in the input data are being filled.

    Attributes:
        _input_data (pandas.DataFrame): The ``input_data`` after preprocessing.

        _ti_data (pandas.DataFrame): The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains one column, the ``cmo``.

        _properties (dict): Indicator properties.

        _calling_instance (str): The name of the class.

    Raises:
        WrongTypeForInputParameter: Input argument has wrong type.
        WrongValueForInputParameter: Unsupported value for input argument.
        NotEnoughInputData: Not enough data for calculating the indicator.
        TypeError: Type error occurred when validating the ``input_data``.
        ValueError: Value error occurred when validating the ``input_data``.
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

        Returns:
            pandas.DataFrame: The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains one column, the ``cmo``.

        Raises:
            NotEnoughInputData: Not enough data for calculating the indicator.
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
        Calculates and returns the trading signal for the calculated technical
        indicator.

        Returns:
            {('hold', 0), ('buy', -1), ('sell', 1)}: The calculated trading
            signal.
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
