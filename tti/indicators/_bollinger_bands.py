"""
Trading-Technical-Indicators (tti) python library

File name: _bollinger_bands.py
    Implements the Bollinger Bands technical indicator.
"""

import pandas as pd

from ._technical_indicator import TechnicalIndicator
from ..utils.constants import TRADE_SIGNALS
from ..utils.exceptions import NotEnoughInputData, WrongTypeForInputParameter,\
    WrongValueForInputParameter


class BollingerBands(TechnicalIndicator):
    """
    Bollinger Bands Technical Indicator class implementation.

    Parameters:
        input_data (pandas.DataFrame): The input data.

        period (int, default is 20): The past periods to be used for the
            calculation of the middle band (simple moving average).

        std_number (int, default is 2): The number of standard deviations to
            be used for calculating the upper and lower bands.

        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        -

    Raises:
        -
    """
    def __init__(self, input_data, period=20, std_number=2,
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

        if isinstance(std_number, (int,float)):
            if std_number > 0.0:
                self._std_number = std_number
            else:
                raise WrongValueForInputParameter(
                    std_number, 'std_number', '>0')
        else:
            raise WrongTypeForInputParameter(
                type(std_number), 'std_number', 'int or float')

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
                It contains three columns, the 'middle_band', 'upper_band' and
                'lower_band'.
        """

        # Not enough data for the requested period
        if len(self._input_data.index) < self._period:
            raise NotEnoughInputData('Bollinger Bands', self._period,
                                     len(self._input_data.index))

        # Calculate the Middle Band using Simple Moving Average
        bb = self._input_data.rolling(
            window=self._period, min_periods=self._period, center=False,
            win_type=None, on=None, axis=0, closed=None).mean().round(4)

        # Calculate Upper and Lower Bands
        standard_deviation = self._input_data.std(axis=0)
        bb = pd.concat([bb,
                        bb + standard_deviation * self._std_number,
                        bb - standard_deviation * self._std_number], axis=1)

        bb.columns = ['middle_band', 'upper_band', 'lower_band']

        return bb

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

        # Price goes above upper band
        if self._input_data['close'].iat[-1] > \
                self._ti_data['upper_band'].iat[-1]:
            return TRADE_SIGNALS['sell']

        # Price goes below lower band
        elif self._input_data['close'].iat[-1] < \
                self._ti_data['lower_band'].iat[-1]:
            return TRADE_SIGNALS['buy']

        else:
            return TRADE_SIGNALS['hold']
