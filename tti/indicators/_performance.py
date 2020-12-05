"""
Trading-Technical-Indicators (tti) python library

File name: _performance.py
    Implements the Performance technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import WrongTypeForInputParameter,\
    WrongValueForInputParameter


class Performance(TechnicalIndicator):
    """
    Performance Technical Indicator class implementation.

    Args:
        input_data (pandas.DataFrame): The input data. Required input column
            is ``close``. The index is of type ``pandas.DatetimeIndex``.

        mode (str, default='LONG'): The current position entered at period 0
            (first row in the input data). Possible values are ``LONG`` and
            ``SHORT``.

        target (numeric, default is 0.05): The target percentage movement
            of the price. When mode is ``LONG`` the target is positive, and an
            exit signal is produced when the target is reached. When mode is
            ``SHORT`` the target is negative, and an exit signal is produced
            when the target is reached.

        fill_missing_values (bool, default=True): If set to True, missing
            values in the input data are being filled.

    Attributes:
        _input_data (pandas.DataFrame): The ``input_data`` after preprocessing.

        _ti_data (pandas.DataFrame): The calculated indicator. Index is of type
            ``pandas.DatetimeIndex``. It contains two columns, the ``prf`` and
            the ``target_<mode>``.

        _properties (dict): Indicator properties.

        _calling_instance (str): The name of the class.

    Raises:
        WrongTypeForInputParameter: Input argument has wrong type.
        WrongValueForInputParameter: Unsupported value for input argument.
        NotEnoughInputData: Not enough data for calculating the indicator.
        TypeError: Type error occurred when validating the ``input_data``.
        ValueError: Value error occurred when validating the ``input_data``.
    """
    def __init__(self, input_data, mode='LONG', target=0.05,
                 fill_missing_values=True):

        # Validate and store if needed, the input parameters
        if isinstance(mode, str):
            if mode in ['LONG', 'SHORT']:
                self._mode = mode
            else:
                raise WrongValueForInputParameter(
                    mode, 'mode', '\'LONG\' or \'SHORT\'')
        else:
            raise WrongTypeForInputParameter(type(mode), 'mode', 'str')

        if isinstance(target, (int, float)):
            if ((mode == 'LONG' and target >= 0) or
                    (mode == 'SHORT' and target <= 0)):
                self._target = target
            else:
                raise WrongValueForInputParameter(
                    target, 'target', '>=0 for mode \'LONG\', '
                                      '<=0 for mode \'SHORT\'')

        else:
            raise WrongTypeForInputParameter(
                type(target), 'target', 'int or float')

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
            ``pandas.DatetimeIndex``. It contains two columns, the ``prf`` and
            the ``target_<mode>``.
        """

        prf = pd.DataFrame(index=self._input_data.index,
                           columns=['prf', 'target_' + self._mode],
                           data=None, dtype='float64')

        prf['prf'] = (self._input_data['close'] - self._input_data['close']. \
            iat[0]) / self._input_data['close'].iat[0]

        prf['target_' + self._mode] = self._target

        return prf.round(4)

    def getTiSignal(self):
        """
        Calculates and returns the trading signal for the calculated technical
        indicator.

        Returns:
            {('hold', 0), ('buy', -1), ('sell', 1)}: The calculated trading
            signal.
        """

        # Not enough data for calculating trading signal
        if len(self._ti_data.index) < 1:
            return TRADE_SIGNALS['hold']

        if self._mode == 'LONG' and self._ti_data.iat[-1, 0] >= self._target:
            return TRADE_SIGNALS['sell']

        if self._mode == 'SHORT' and self._ti_data.iat[-1, 0] <= self._target:
            return TRADE_SIGNALS['buy']

        return TRADE_SIGNALS['hold']
