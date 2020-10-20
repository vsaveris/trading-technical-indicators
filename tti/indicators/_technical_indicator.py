"""
Trading-Technical-Indicators (tti) python library

File name: _technical_indicator.py
    Parent class for all the technical indicators.
"""

import pandas as pd
from abc import ABC, abstractmethod

from .properties.indicators_properties import INDICATORS_PROPERTIES
from ..utils.plot import linesGraph
from ..utils.data_validation import validateInputData
from ..utils.exceptions import WrongTypeForInputParameter


class TechnicalIndicator(ABC):
    """
    Technical Indicators class implementation. It is used as a parent class for
    each implemented technical indicator. It implements the public API for
    accessing the calculated values, graph and signal of each indicator.

    Parameters:
        calling_instance (str): The name of the calling class.

        input_data (pandas.DataFrame): The input data.

        fill_missing_values (boolean, default is True): If set to True,
            missing values in the input data are being filled.

    Attributes:
        _calling_instance (str): The name of the calling class.

        _properties (dictionary): Indicator properties.

        _input_data (pandas.DataFrame): The input data after preprocessing.

        _ti_data (pandas.DataFrame): Technical Indicator calculated data.

    Raises:
        -
    """

    def __init__(self, calling_instance, input_data, fill_missing_values=True):

        # Validate fill missing values input parameter
        if not isinstance(fill_missing_values, bool):
            raise WrongTypeForInputParameter(
                type(fill_missing_values), 'fill_missing_values', 'bool')

        self._calling_instance = calling_instance

        # Read the properties for the specific Technical Indicator
        self._properties = INDICATORS_PROPERTIES[calling_instance]

        # Input data preprocessing
        self._input_data = \
            validateInputData(input_data,
                              self._properties['required_input_data'],
                              calling_instance,
                              fill_missing_values=fill_missing_values)

        # Calculation of the Technical Indicator
        self._ti_data = self._calculateTi()

    @staticmethod
    def _rolling_pipe(df, window, function):
        """
        Applies a function to a pandas rolling pipe.

        Parameters:
            df (pandas.DataFrame): The input pandas.DataFrame.

            window (int): The size of the rolling window.

            function (function object): The function to be applied.

        Raises:
            -

        Returns:
           pandas.Series: The result of the applied function.
        """

        return pd.Series(
            [df.iloc[i - window: i].pipe(function) if i >= window
             else None for i in range(1, len(df) + 1)],
            index=df.index)

    @abstractmethod
    def _calculateTi(self):
        """
        Calculates the technical indicator for the given input data.

        Parameters:
            -

        Raises:
             -

        Returns:
            pandas.DataFrame: The calculated indicator. Index is of type date.
                It can contain several columns depending the indicator.
        """

        pass

    @abstractmethod
    def getTiSignal(self):
        """
         Calculates and returns the signal of the technical indicator.

         Parameters:
            -

         Raises:
             -

         Returns:
            tuple (string, integer): The Trading signal. Possible values are
                ('hold', 0), ('buy', -1), ('sell', 1). See TRADE_SIGNALS
                constant in the tti.utils package, constants.py module.
         """

        pass

    def getTiData(self):
        """
        Returns the Technical Indicator values for the whole period.

        Parameters:
            -

        Raises:
            -

        Returns:
            pandas.DataFrame: The Technical Indicator values.
        """

        return self._ti_data

    def getTiValue(self,  date=None):
        """
        Returns the Technical Indicator value for a given date. If the date
        is None, it returns the most recent entry.

        Parameters:
            date (string, default is None): A date string.

        Raises:
            -

        Returns:
            float: The value of the Technical Indicator for the given date.
        """

        try:
            if date is None:
                return [round(x, 4) for x in list(self._ti_data.iloc[-1, :])]
            else:
                return [round(x, 4) for x in
                        list(self._ti_data.loc[pd.to_datetime(date), :])]
        except (Exception, ValueError):
            return None

    def getTiGraph(self):
        """
        Generates a plot customized for each Technical Indicator.

        Parameters:
            -

        Raises:
            -

        Returns:
            matplotlib object: The generated plot.
        """

        # Check if split to subplots is required for this Indicator
        if self._properties['graph_subplots']:
            data = [self._input_data[self._properties['graph_input_columns']],
                    self._ti_data]
        else:
            data = pd.concat([self._input_data[
                                  self._properties['graph_input_columns']],
                              self._ti_data], axis=1)

        return linesGraph(data=data, title=self._properties['long_name'],
                          y_label=self._properties['graph_y_label'],
                          lines_color=self._properties['graph_lines_color'],
                          alpha_values=self._properties['graph_alpha_values'],
                          areas=self._properties['graph_areas'])
