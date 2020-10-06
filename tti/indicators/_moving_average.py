"""
Trading-Technical-Indicators (tti) python library

File name: _moving_average.py
    Implements the Moving Average (Simple and Exponential) technical indicator.
"""

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class MovingAverage(TechnicalIndicator):
    """
    Moving Average Technical Indicator class implementation.

    Parameters:
        input_data (pandas.DataFrame): The input data.

        ma_type (string, 'simple' or 'exponential', default is simple): The
            type of the calculated moving average. More types can be supported
            in a future release.

        period (int, default is 200): The past periods to be used for the
            calculation of the moving average. 5-13 days are for Very Short
            Term, 14-25 days are for Short Term, 26-49 days are for Minor
            Intermediate, 50-100 days for Intermediate and 100-200 days are for
            Long Term.

        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        -

    Raises:
        -
    """
    def __init__(self, input_data, ma_type='simple', period=200,
                 fill_missing_values=True):

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

        if isinstance(ma_type, str):
            if ma_type in ['simple', 'exponential']:
                self._ma_type = ma_type
            else:
                raise WrongValueForInputParameter(
                    ma_type, 'ma_type', '\'simple\' or \'exponential\'')
        else:
            raise WrongTypeForInputParameter(type(ma_type), 'ma_type', 'str')

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
                It contains one column, the 'ma'.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._period:
            raise NotEnoughInputData('Moving Average', self._period,
                                     len(self._input_data.index))

        if self._ma_type == 'simple':
            ma = self._input_data.rolling(
                window=self._period, min_periods=self._period, center=False,
                win_type=None,
                on=None, axis=0, closed=None).mean().round(4)
        else:
            ma = self._input_data.ewm(
                span=self._period, min_periods=self._period, adjust=False,
                axis=0).mean().round(4)

        ma.columns = ['ma']

        return ma

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

        # Close price goes below Moving Average
        if self._input_data['close'].iat[-2] > self._ti_data['ma'].iat[-2] and\
           self._input_data['close'].iat[-1] < self._ti_data['ma'].iat[-1]:
            return TRADE_SIGNALS['sell']

        # Close price goes above Moving Average
        if self._input_data['close'].iat[-2] < self._ti_data['ma'].iat[-2] and\
           self._input_data['close'].iat[-1] > self._ti_data['ma'].iat[-1]:
            return TRADE_SIGNALS['buy']

        return TRADE_SIGNALS['hold']
