"""
Trading-Technical-Indicators (tti) python library

File name: _parabolic_sar.py
    Implements the Parabolic SAR technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData


class ParabolicSAR(TechnicalIndicator):
    """
    Parabolic SAR Technical Indicator class implementation.

    Args:
        input_data (pandas.DataFrame): The input data. Required input columns
            are ``high``, ``low``, ``close``. The index is of type
            ``pandas.DatetimeIndex``.

        fill_missing_values (bool, default=True): If set to True, missing
            values in the input data are being filled.

    Attributes:
        _input_data (pandas.DataFrame): The ``input_data`` after preprocessing.

        _ti_data (pandas.DataFrame): The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains one column, the ``sar``.

        _properties (dict): Indicator properties.

        _calling_instance (str): The name of the class.

    Raises:
        WrongTypeForInputParameter: Input argument has wrong type.
        WrongValueForInputParameter: Unsupported value for input argument.
        NotEnoughInputData: Not enough data for calculating the indicator.
        TypeError: Type error occurred when validating the ``input_data``.
        ValueError: Value error occurred when validating the ``input_data``.
    """

    def __init__(self, input_data, fill_missing_values=True):

        # Indicator parameters, currently constants but expose to user should
        # be considered.
        self._af_increase = 0.02
        self._af_max = 0.2

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
            ``pandas.DatetimeIndex``. It contains one column, the ``sar``.

        Raises:
            NotEnoughInputData: Not enough data for calculating the indicator.
        """

        # Not enough data for calculating SAR
        if len(self._input_data.index) < 2:
            raise NotEnoughInputData('Parabolic SAR', 2,
                                     len(self._input_data.index))

        sar = pd.DataFrame(index=self._input_data.index,
                           columns=['af', 'ep', 'sar', 'position'],
                           data=None)

        position_start_index = 0

        for i in range(len(self._input_data.index)):

            sar.values[i, :], position_start_index = self._calculateSarRow(
                current_index=i, position_start_index=position_start_index,
                previous_sar=sar.values[i-1, :], position_changed=False)

        return sar[['sar']].astype(dtype='float64').round(4)

    def _calculateSarRow(self, current_index, position_start_index,
                         previous_sar=None, position_changed=False):
        """
        Calculate SAR in case we are in a `LONG` position.

        Args:
            current_index (int): The current dataframe index for which the SAR
                calculation is requested.

            position_start_index (int): The dataframe index (starting from 0)
                in which the current position was started.

            previous_sar (numpy.ndarray, default is None): The SAR row for the
                previous period. Is not required when this is the first period
                of the input data (current_index = 0).

            position_changed (boolean, default is False): Indicates if this is
                the first calculation for a new position. Is not required when
                this is the first period of the input data (current_index = 0).

        Returns:
            list (af, ep, sar, position):
                - af (float): Acceleration factor for the current index.
                - ep (float): Extreme price for the current index.
                - sar (float): SAR indicator value for the current index.
                - position (str, one of `LONG`, `SHORT`): The position for
                    the current index.

            int: Current position start index.
        """

        # In case this is for the first period of the input data, calculation
        # is based on an initial position assumption (guess the initial
        #  position by checking the high values direction for the first two
        #  days)
        if current_index == 0:

            af = self._af_increase

            if self._input_data['high'].values[1] > \
                    self._input_data['high'].values[0]:
                position = 'LONG'
                ep = self._input_data['high'].values[0]
                sar = self._input_data['low'].values[0]
            else:
                position = 'SHORT'
                ep = self._input_data['low'].values[0]
                sar = self._input_data['high'].values[0]

            return [af, ep, sar, position], current_index

        # Check if position changed, so to re-initialize the values
        if position_changed:
            af = self._af_increase

            if previous_sar[3] == 'LONG':
                position = 'SHORT'
                ep = self._input_data['low'].values[current_index]
                sar = self._input_data['high'].values[
                      position_start_index:current_index].max()

            else:
                position = 'LONG'
                ep = self._input_data['high'].values[current_index]
                sar = self._input_data['low'].values[
                      position_start_index:current_index].min()

            return [af, ep, sar, position], current_index

        # Calculate Extreme Price, Highest price reached when in current
        # `LONG` position, or Lowest price reached when in current `SHORT`
        # position
        if previous_sar[3] == 'LONG':

            ep = self._input_data['high'].values[
                 position_start_index:current_index+1].max()

        else:

            ep = self._input_data['low'].values[
                 position_start_index:current_index+1].min()

        # Calculate Acceleration Factor, new high is reached when in `LONG` or
        # new low is reached when in `SHORT`
        if previous_sar[3] == 'LONG' and ep > previous_sar[1]:

            af = min(self._af_max,
                     previous_sar[0] + self._af_increase)

        elif previous_sar[3] == 'SHORT' and ep < previous_sar[1]:

            af = min(self._af_max,
                     previous_sar[0] + self._af_increase)

        else:
            af = previous_sar[0]

        # Calculate SAR, when `LONG` not above the two prior lows, when `SHORT`
        # not below the two prior highs
        sar = previous_sar[2] + previous_sar[0] * (
                previous_sar[1] - previous_sar[2])

        if previous_sar[3] == 'LONG':
            sar = min(sar, self._input_data['low'].values[
                           max(0, current_index-2):current_index].min())

        else:
            sar = max(sar, self._input_data['high'].values[
                           max(0, current_index - 2):current_index].max())

        # Check if position changes
        if (previous_sar[3] == 'SHORT' and
            self._input_data['high'].values[current_index] > sar) or \
                (previous_sar[3] == 'LONG' and
                 self._input_data['low'].values[current_index] < sar):

            return self._calculateSarRow(
                current_index=current_index,
                position_start_index=position_start_index,
                previous_sar=previous_sar, position_changed=True)

        else:
            position = previous_sar[3]

        return [af, ep, sar, position], position_start_index

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

        if ((self._input_data['close'].iat[-2] >
                self._ti_data['sar'].iat[-2]) and
                (self._input_data['close'].iat[-1] <
                 self._ti_data['sar'].iat[-1])):
            return TRADE_SIGNALS['buy']

        elif ((self._input_data['close'].iat[-2] <
               self._ti_data['sar'].iat[-2]) and
              (self._input_data['close'].iat[-1] >
               self._ti_data['sar'].iat[-1])):
            return TRADE_SIGNALS['sell']

        else:
            return TRADE_SIGNALS['hold']
