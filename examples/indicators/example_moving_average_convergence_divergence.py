"""
Trading-Technical-Indicators (tti) python library

File name: example_moving_average_convergence_divergence.py
    Example code for the Moving Average Convergence Divergence technical
    indicator.
"""

import re
import pandas as pd

from tti.indicators import MovingAverageConvergenceDivergence

# Read data from csv file. Set the index to the correct column (dates column)
df = pd.read_csv('./data/sample_data.csv', parse_dates=True, index_col=0)

# Create the indicator for a part of the input file
ti = MovingAverageConvergenceDivergence(df[df.index >= '2012-01-01'])

# Show the Graph for the calculated Technical Indicator
ti.getTiGraph().show()

# Save the Graph for the calculated Technical Indicator
name = '_'.join(x.lower() for x in re.findall('[A-Z][^A-Z]*',
                                              ti.__class__.__name__))

ti.getTiGraph().savefig('./figures/indicators_' + name + '_example.png')
print('- Graph ../figures/indicators_' + name + '_example.png saved.')

# Get indicator's calculated data
print('\nTechnical Indicator data:\n', ti.getTiData())

# Get indicator's value for a specific date
print('\nTechnical Indicator value at 2012-09-06:',
      ti.getTiValue('2012-09-06'))

# Get the most recent indicator's value
print('\nTechnical Indicator value at', ti.getTiData().index[-1], ':',
      ti.getTiValue())

# Get signal from indicator
print('\nTechnical Indicator signal:', ti.getTiSignal())
