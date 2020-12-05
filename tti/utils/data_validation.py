"""
Trading-Technical-Indicators (tti) python library

File name: data_validation.py
    Input data validation methods implementation, defined under the
    tti.utils package.
"""

import pandas as pd
import pandas.api.types as pdtypes
from .data_preprocessing import fillMissingValues
from .exceptions import WrongTypeForInputParameter


def validateInputData(input_data, required_columns, indicator_name,
                      fill_missing_values=True):
    """
    Validates that the data parameter is a pandas.DataFrame, that its index
    is of type date, that it is not empty and that it contains the required
    columns (required_columns parameters) with the proper data type. It returns
    the DataFrame with only the required columns, sorted on the date index and
    with missing values filled (if related parameter is set to True). It raises
    an exception in case the validation fails.

    Args:
        input_data (pandas.DataFrame): The input data. The index is of type
            ``pandas.DatetimeIndex``.
        
        required_columns ([str,]): The columns which should be contained in the
            dataframe for the specific indicator.
            
        indicator_name (str): The name of the indicator. To be used in case
            an exception is raised.

        fill_missing_values (bool, default=True): If True, missing values are
            filled as described in the data_preprocessing.py module.

    Returns:
        pandas.DataFrame: The input data frame containing only the required
        columns, sorted and with missing values filled (if requested). The
        dataframe is ready to be used for calculating the Technical Indicator
        without any further processing.

    Raises:
        WrongTypeForInputParameter: Input argument has wrong type.
        TypeError: Type error occurred when validating the ``input_data``.
        ValueError: Value error occurred when validating the ``input_data``.
    """

    # Validate that the input_data parameter is a pandas.DataFrame object
    if not isinstance(input_data, pd.DataFrame):
        raise WrongTypeForInputParameter(
            type(input_data), 'input_data', 'pd.DataFrame')

    # Validate that the index of the pandas.DataFrame is of type date
    if not isinstance(input_data.index, pd.DatetimeIndex):
        raise TypeError('Invalid input_data index type. It was expected ' +
                        '`pd.DatetimeIndex` but `' +
                        str(type(input_data.index).__name__) + '` was found.')

    # Validate that the data frame is not empty
    if input_data.empty:
        raise ValueError('The input_data cannot be an empty pandas.DataFrame.')

    # Make columns case insensitive
    input_data.columns = [c.lower() for c in input_data.columns]

    # Validate that the data frame holds columns of numeric type and that all
    # the required columns are contained.
    for column in required_columns:
        if column not in input_data.columns:
            raise ValueError('Required column `' + column + '` for the ' +
                             'technical indicator `' + indicator_name +
                             '` does not exist in the input_data  ' +
                             'pandas.DataFrame.')

        if not pdtypes.is_numeric_dtype(input_data[column]):
            raise ValueError('The input_data pandas.DataFrame must hold ' +
                             'columns of numeric type, but column `' +
                             column + '` is of type `' +
                             str(input_data[column].dtype) + '`.')

    # Remove not required columns, if any
    for column in input_data.columns:
        if column not in required_columns:
            input_data = input_data.drop(columns=column, inplace=False)

    # Sort dataframe on index ascending
    input_data = input_data.sort_index(ascending=True, inplace=False)

    if fill_missing_values:
        input_data = fillMissingValues(input_data)

    return input_data
