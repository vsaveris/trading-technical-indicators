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

    Parameters:
        input_data (pandas.DataFrame): The input data.

        mode (string, 'LONG' or 'SHORT', default is 'LONG'): The current
            position entered at period 0 (first row in the input data).

        target (int or float, default is 0.05): The target percentage movement
            of the price. When mode is `LONG` the target is positive, and an
            exit signal is produced when the target is reached. When mode is
            `SHORT` the target is negative, and an exit signal is produced when
            the target is reached.

        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        -

    Raises:
        -
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

        Parameters:
            -

        Raises:
            -

        Returns:
            pandas.DataFrame: The calculated indicator. Index is of type date.
                It contains two columns, the 'prf' and the 'target <mode>'.
        """

        prf = pd.DataFrame(index=self._input_data.index,
                           columns=['prf', 'target ' + self._mode],
                           data=None, dtype='float64')

        prf['prf'] = (
            self._input_data['close'] - self._input_data['close'].iat[0]
                     ) / self._input_data['close'].iat[0]

        prf['target ' + self._mode] = self._target

        return prf.round(4)

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

        if self._mode == 'LONG' and self._ti_data.iat[-1, 0] >= self._target:
            return TRADE_SIGNALS['sell']

        if self._mode == 'SHORT' and self._ti_data.iat[-1, 0] <= self._target:
            return TRADE_SIGNALS['buy']

        return TRADE_SIGNALS['hold']
