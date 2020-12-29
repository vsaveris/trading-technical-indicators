"""
Trading-Technical-Indicators (tti) python library

File name: indicator_example.py
    Example code for the trading technical indicators, for the docs.

Accumulation Distribution Line indicator and SCMN.SW.csv data file is used.
"""

import pandas as pd
from tti.indicators import AccumulationDistributionLine

# Read data from csv file. Set the index to the correct column
# (dates column)
df = pd.read_csv('./data/SCMN.SW.csv', parse_dates=True, index_col=0)

# Create indicator
adl_indicator = AccumulationDistributionLine(input_data=df)

# Get indicator's calculated data
print('\nTechnical Indicator data:\n', adl_indicator.getTiData())

# Get indicator's value for a specific date
print('\nTechnical Indicator value at 2012-09-06:', adl_indicator.getTiValue('2012-09-06'))

# Get the most recent indicator's value
print('\nMost recent Technical Indicator value:', adl_indicator.getTiValue())

# Get signal from indicator
print('\nTechnical Indicator signal:', adl_indicator.getTiSignal())

# Show the Graph for the calculated Technical Indicator
adl_indicator.getTiGraph().show()

# Save the Graph for the calculated Technical Indicator
adl_indicator.getTiGraph().savefig('./figures/example_AccumulationDistributionLine.png')
print('\nGraph for the calculated ADL indicator data, saved.')

# Execute simulation based on trading signals
simulation_data, simulation_statistics, simulation_graph = \
    adl_indicator.getTiSimulation(
        close_values=df[['close']], max_exposure=None,
        short_exposure_factor=1.5)
print('\nSimulation Data:\n', simulation_data)
print('\nSimulation Statistics:\n', simulation_statistics)

# Save the Graph for the executed trading signal simulation
simulation_graph.savefig('./figures/simulation_AccumulationDistributionLine.png')
print('\nGraph for the executed trading signal simulation, saved.')
