"""
Trading-Technical-Indicators (tti) python library

File name: data_preprocessing.py
    Data preprocessing methods defined under the tti.utils package.
"""

import pandas as pd


def fillMissingValues(input_data):
    """
    Fills the missing values of a dataframe by executing first a forward pass
    and then a backward pass.
    
    Args:
        input_data (pandas.DataFrame): The input data. The index is of type
            ``pandas.DatetimeIndex``.

    Returns:
        pandas.DataFrame: The input data with missing values filled.

    Raises:
        TypeError: Type error occurred when validating the ``input_data``.
    """
    
    if isinstance(input_data, pd.DataFrame):
        # Sort dataframe on index ascending, use a copy of the original df
        data = input_data.sort_index(ascending=True)
    
        # First fill forward and the backward (order matters)
        data.fillna(method='ffill', inplace=True)
        data.fillna(method='bfill', inplace=True)

    else:
        raise TypeError('Invalid input_data type. It was expected ' +
                        '`pd.DataFrame` but `' +
                        str(type(input_data).__name__) + '` was found.')
    
    return data
