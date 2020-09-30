"""
Trading-Technical-Indicators (tti) python library

File name: example_on_balance_volume.py
    Example code for the On Balance Volume technical indicator.
"""

import pandas as pd

from tti.indicators import OnBalanceVolume

# Read data from csv file. Set the index to the correct column (dates column)
df = pd.read_csv('./data/sample_data.csv', parse_dates=True, index_col=0)

# Create the On Balance Volume indicator for a part of the input file
obv = OnBalanceVolume(df[df.index >= '2012-01-01'])

# Show the Graph for the calculated Technical Indicator
obv.getTiGraph().show()

# Save the Graph for the calculated Technical Indicator
obv.getTiGraph().savefig('./figures/indicators_obv_example.png')
print('- Graph ../figures/indicators_obv_example.png saved.')

# Get On Balance Volume  calculated data
print('\nOn Balance Volume:\n', obv.getTiData())

# Get On Balance Volume value for a specific date
print('\nOn Balance Volume value at 2012-09-06:', obv.getTiValue('2012-09-06'))

# Get the most recent On Balance Volume value
print('\nOn Balance Volume value at', obv.getTiData().index[-1], ':',
      obv.getTiValue())

# Get signal from On Balance Volume
print('\nSignal:', obv.getTiSignal())
