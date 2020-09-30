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
    
    Parameters:
        input_data (pandas.DataFrame): The input data.

    Raises:
        TypeError

    Returns:
        pandas.DataFrame: The input data with missing values filled.
    """
    
    if isinstance(input_data, pd.DataFrame):
        # Sort dataframe on index ascending
        input_data.sort_index(ascending=True, inplace=True)
    
        # First fill forward and the backward (order matters)
        input_data.fillna(method='ffill', inplace=True)
        input_data.fillna(method='bfill', inplace=True)

    else:
        raise TypeError('Invalid input_data type. It was expected ' +
                        '`pd.DataFrame` but `' +
                        str(type(input_data).__name__) + '` was found.')
    
    return input_data
