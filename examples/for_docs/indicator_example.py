"""
Trading-Technical-Indicators (tti) python library

File name: indicator_example.py
    Example code for the trading technical indicators, for the docs.

Accumulation Distribution Line indicator and SCMN.SW.csv data file is used.
"""

import pandas as pd
import matplotlib.pyplot as plt
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
print('Graph for the calculated ADL indicator data, saved.')

# Execute simulation based on trading signals
simulation_data, simulation_statistics = adl_indicator.getTiSimulation(
    close_values=df[['close']], max_exposure=None, short_exposure_factor=1.5)
print('\nSimulation Data:\n', simulation_data)
print('\nSimulation Statistics:\n', simulation_statistics)

# Example on how a graph can be created from the simulation data
plt.figure(figsize=(7, 5))

plt.subplot(3, 1, 1)
plt.plot(list(range(1, len(df['close']) + 1)), df['close'], label='close_price',
         color='limegreen')
plt.legend(loc=0)
plt.grid(which='major', axis='y', alpha=0.5)
plt.title('Trading Simulation for AccumulationDistributionLine', fontsize=11,
          fontweight='bold')
plt.gca().axes.get_xaxis().set_visible(False)

plt.subplot(3, 1, 2)
plt.plot(list(range(1, len(simulation_data['exposure']) + 1)),
         simulation_data['exposure'], label='exposure', color='tomato')
plt.legend(loc=0)
plt.grid(which='major', axis='y', alpha=0.5)
plt.gca().axes.get_xaxis().set_visible(False)

plt.subplot(3, 1, 3)
plt.plot(list(range(1, len(simulation_data['balance']) + 1)),
        simulation_data['balance'], label='balance', color='cornflowerblue')
plt.legend(loc=0)
plt.grid(which='major', axis='y', alpha=0.5)

plt.xlabel('Transactions', fontsize=11, fontweight='bold')
plt.gcf().text(0.01, 0.5, 'Balance | Exposure | Price', fontsize=11,
        fontweight='bold', va='center', rotation='vertical')

plt.savefig('./figures/simulation_AccumulationDistributionLine.png')
