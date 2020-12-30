# trading-technical-indicators (tti)
**Trading Technical Indicators python library, where Traditional Technical Analysis and AI are met. Version 0.2.2 (stable release)**
- Calculate technical indicators (62 indicators supported).
- Produce graphs for any technical indicator.
- Get trading signals for each indicator.
- Trading simulation based on trading signals.
- Machine Learning integration for prices prediction (not included in this release).

*Implementation based on the book 'Technical Analysis from A to Z, Steven B. Achelis'. Validation based on the 'A to Z Companion Spreadsheet, Steven B. Achelis and Jon C. DeBry'*

API documentation and installation instructions can be found in the project's web-site:
[Trading Technical Indicators](https://www.trading-technical-indicators.org/)

**Change Log**

*Stable Releases*
- 0.2.2: Incompatibilities with the latest pandas release 1.2.0 fixed ([#20](https://github.com/vsaveris/trading-technical-indicators/issues/20))
- 0.2.1: Bug fixes, new pandas release causes an exception in some indicators calculation ([#20](https://github.com/vsaveris/trading-technical-indicators/issues/20))
- 0.2.0: First stable release, updates described in the following github issues ([#2](https://github.com/vsaveris/trading-technical-indicators/issues/2), [#3](https://github.com/vsaveris/trading-technical-indicators/issues/3), [#14](https://github.com/vsaveris/trading-technical-indicators/issues/14), [#15](https://github.com/vsaveris/trading-technical-indicators/issues/15))

*Beta Releases*
- 0.1.b3: Updates described in the following github issues ([#11](https://github.com/vsaveris/trading-technical-indicators/issues/11), [#7](https://github.com/vsaveris/trading-technical-indicators/issues/7), [#8](https://github.com/vsaveris/trading-technical-indicators/issues/8))
- 0.1.b2: Bugs fixes ([#1](https://github.com/vsaveris/trading-technical-indicators/issues/1))
- 0.1.b1: Cosmetic changes in package building file applied (setup.py)
- 0.1.b0: First beta release

*Planned Releases*
- 1.0.0: Full featured release, including machine learning related features (*planned for 01.03.2021*).

**Indicators supported**
- Accumulation Distribution Line
- Average True Range
- Bollinger Bands
- Chaikin Money Flow
- Chaikin Oscillator
- Chande Momentum Oscillator
- Commodity Channel Index
- Detrended Price Oscillator
- Directional Movement Index
- Double Exponential Moving Average
- Ease Of Movement
- Envelopes
- Fibonacci Retracement
- Forecast Oscillator
- Ichimoku Cloud
- Intraday Movement Index
- Klinger Oscillator
- Linear Regression Indicator
- Linear Regression Slope
- Market Facilitation Index
- Mass Index
- Median Price
- Momentum
- Exponential Moving Average
- Simple Moving Average
- Time-Series Moving Average
- Triangular Moving Average
- Variable Moving Average
- Moving Average Convergence Divergence
- Negative Volume Index
- On Balance Volume
- Parabolic SAR
- Performance
- Positive Volume Index
- Price And Volume Trend
- Price Channel
- Price Oscillator
- Price Rate Of Change
- Projection Bands
- Projection Oscillator
- Qstick
- Range Indicator
- Relative Momentum Index
- Relative Strength Index
- Relative Volatility Index
- Standard Deviation
- Stochastic Momentum Index
- Fast Stochastic Oscillator
- Slow Stochastic Oscillator
- Swing Index
- Time Series Forecast
- Triple Exponential Moving Average
- Typical Price
- Ultimate Oscillator
- Vertical Horizontal Filter
- Volatility Chaikins
- Volume Oscillator
- Volume Rate Of Change
- Weighted Close
- Wilders Smoothing
- Williams Accumulation Distribution
- Williams %R

### Usage Example

**Code example**
```python
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

# Execute simulation based on trading signals
simulation_data, simulation_statistics, simulation_graph = \
    adl_indicator.getTiSimulation(
        close_values=df[['close']], max_exposure=None,
        short_exposure_factor=1.5)
print('\nSimulation Data:\n', simulation_data)
print('\nSimulation Statistics:\n', simulation_statistics)

# Show the Graph for the executed trading signal simulation
simulation_graph.show()
```

**Output**
```
Technical Indicator data:
                      adl
Date
1998-10-05  5.346066e+05
1998-10-06  9.788753e+05
1998-10-07  1.377338e+06
1998-10-08  1.251994e+06
1998-10-09  1.108012e+06
...                  ...
2020-11-30  1.736986e+07
2020-12-01  1.741746e+07
2020-12-02  1.737860e+07
2020-12-03  1.741683e+07
2020-12-04  1.742771e+07

[5651 rows x 1 columns]

Technical Indicator value at 2012-09-06: [8617026.854250321]

Most recent Technical Indicator value: [17427706.42639293]

Technical Indicator signal: ('buy', -1)

Simulation Data:
            signal open_trading_action  ... earnings  balance
Date                                   ...
1998-10-05   hold                none  ...        0        0
1998-10-06    buy                long  ...        0  385.138
1998-10-07    buy                long  ...   13.264  411.666
1998-10-08    buy                long  ...   13.264  777.644
1998-10-09    buy                long  ...   19.159  795.329
...           ...                 ...  ...      ...      ...
2020-11-30    buy                long  ...  19817.2  37577.2
2020-12-01   hold                none  ...  19817.2  37577.2
2020-12-02    buy                long  ...  19817.2  38019.2
2020-12-03    buy                long  ...  19817.2  38385.1
2020-12-04    buy                long  ...  19817.2  38837.2

[5651 rows x 7 columns]

Simulation Statistics:
 {'number_of_trading_days': 5651, 'number_of_buy_signals': 4767, 'number_of_ignored_buy_signals': 0, 'number_of_sell_signals': 601, 'number_of_ignored_sell_signals': 0, 'last_stock_value': 475.5, 'last_exposure': 22340.73, 'last_open_long_positions': 40, 'last_open_short_positions': 0, 'last_portfolio_value': 19020.0, 'last_earnings': 19817.21, 'final_balance': 38837.21}
```

**Output graphs**

![](./examples/for_docs/figures/example_AccumulationDistributionLine.png?raw=true)

![](./examples/for_docs/figures/simulation_AccumulationDistributionLine.png?raw=true)
