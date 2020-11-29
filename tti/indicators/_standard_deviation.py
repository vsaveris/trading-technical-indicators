"""
Trading-Technical-Indicators (tti) python library

File name: _standard_deviation.py
    Implements the Standard Deviation technical indicator.
"""

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class StandardDeviation(TechnicalIndicator):
    """
    Standard Deviation Technical Indicator class implementation.

    Parameters:
        input_data (pandas.DataFrame): The input data.

        period (int, default is 20): The past periods to be used for the
            calculation of the simple moving average.

        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        -

    Raises:
        WrongTypeForInputParameter
        WrongValueForInputParameter
    """
    def __init__(self, input_data, period=20, fill_missing_values=True):

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
            NotEnoughInputData

        Returns:
            pandas.DataFrame: The calculated indicator. Index is of type date.
                It contains one column, the 'sd'.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._period:
            raise NotEnoughInputData('Standard Deviation', self._period,
                                     len(self._input_data.index))

        # Calculate Upper and Lower Bands
        sd = self._input_data.rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).std(ddof=0).round(4)

        sd.columns = ['sd']

        return sd

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
        if len(self._ti_data.index) < 1:
            return TRADE_SIGNALS['hold']

        # Calculate Simple Moving Average
        sma = self._input_data.rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).mean().round(4)

        # Price above average and volatility is high
        if self._input_data['close'].iat[-1] > sma.iat[-1, 0] and \
                self._ti_data['sd'].iat[-1] > 2:
            return TRADE_SIGNALS['sell']

        # Price below average and volatility is high
        if self._input_data['close'].iat[-1] < sma.iat[-1, 0] and \
                self._ti_data['sd'].iat[-1] > 2:
            return TRADE_SIGNALS['buy']

        return TRADE_SIGNALS['hold']
