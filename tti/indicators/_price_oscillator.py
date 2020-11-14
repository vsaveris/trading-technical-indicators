"""
Trading-Technical-Indicators (tti) python library

File name: _price_oscillator.py
    Implements the Price Oscillator technical indicator.
"""

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class PriceOscillator(TechnicalIndicator):
    """
    Price Oscillator Technical Indicator class implementation.

    Parameters:
        input_data (pandas.DataFrame): The input data.

        long_ma (int, default is 30): The periods to be used for the
            calculation of the Long Moving Average.

        short_ma (int, default is 10): The periods to be used for the
            calculation of the Short Moving Average.

        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        -

    Raises:
        -
    """
    def __init__(self, input_data, long_ma=30, short_ma=10,
                 fill_missing_values=True):

        # Validate and store if needed, the input parameters
        if isinstance(long_ma, int):
            if long_ma > 0:
                self._long_ma = long_ma
            else:
                raise WrongValueForInputParameter(
                    long_ma, 'long_ma', '>0')
        else:
            raise WrongTypeForInputParameter(
                type(long_ma), 'long_ma', 'int')

        if isinstance(short_ma, int):
            if short_ma > 0:
                self._short_ma = short_ma
            else:
                raise WrongValueForInputParameter(
                    short_ma, 'short_ma', '>0')
        else:
            raise WrongTypeForInputParameter(
                type(short_ma), 'short_ma', 'int')

        if short_ma > long_ma:
            raise WrongValueForInputParameter(
                short_ma, 'short_ma', 'long_ma > short_ma')

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
                It contains three columns, the 'posc'.
        """

        # Not enough data
        if len(self._input_data.index) < self._long_ma:
            raise NotEnoughInputData('Price Oscillator', self._long_ma,
                                     len(self._input_data.index))

        # Calculate Long Simple Moving Average
        long_ma = self._input_data.rolling(
            window=self._long_ma, min_periods=self._long_ma, center=False,
            win_type=None, on=None, axis=0, closed=None).mean()

        # Calculate Short Simple Moving Average
        short_ma = self._input_data.rolling(
            window=self._short_ma, min_periods=self._short_ma, center=False,
            win_type=None, on=None, axis=0, closed=None).mean()

        # Calculate MACD
        posc = 100 * (short_ma - long_ma) / long_ma

        posc.columns = ['posc']

        return posc.round(4)

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
        if self._ti_data['posc'].iat[-2] < 0.0 < self._ti_data['posc'].iat[-1]:
            return TRADE_SIGNALS['buy']

        if self._ti_data['posc'].iat[-2] > 0.0 > self._ti_data['posc'].iat[-1]:
            return TRADE_SIGNALS['sell']

        return TRADE_SIGNALS['hold']
