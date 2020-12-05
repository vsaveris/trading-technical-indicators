"""
Trading-Technical-Indicators (tti) python library

File name: indicators_properties.py
    Properties definition for each implemented Technical Indicator.

Each indicator has its properties defined in the INDICATORS_PROPERTIES
dictionary. The format for each indicator is:

"<Indicator's Class Name>": {
"long_name": <indicator's long name>,
"short_name": <indicator's short name>,
"required_input_data": <required input data (list of column names)>,
"graph_input_columns": <list of column names from input data to be added to
the graph> or [None],
"graph_y_label": <label for the y-axis>,
"graph_lines_color": <color for each line of the graph (list of
matplotlib.colors) or [None]>,
"graph_alpha_values": <alpha value for each line of the graph or [None]>,
"graph_areas": <areas (list of dictionaries): Includes the areas to be
plotted by using the fill_between matplotlib method. Each member of the list
should be a dictionary with the below keys: {'x':, 'y1':, 'y2':, 'color':},
see fill_between matplotlib method for more details. or None>
"graph_subplots": <boolean for splitting input and indicator data in subplots
(makes sense when graph_input_columns is set)>
}
"""

INDICATORS_PROPERTIES = \
  {"AccumulationDistributionLine":
   {"long_name": "Accumulation Distribution Line",
    "short_name": "ADL",
    "required_input_data": ["close", "volume", "high", "low"],
    "graph_input_columns": ["close"],
    "graph_y_label": "ADL | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "AverageTrueRange":
   {"long_name": "Average True Range",
    "short_name": "ATR",
    "required_input_data": ["high", "low", "close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "ATR | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "BollingerBands":
   {"long_name": "Bollinger Bands",
    "short_name": "BB",
    "required_input_data": ["close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "Price",
    "graph_lines_color": ["black", "cornflowerblue", "limegreen", "tomato"],
    "graph_alpha_values": [0.5, 1.0, 1.0, 1.0],
    "graph_areas": None,
    "graph_subplots": False
    }, "ChaikinMoneyFlow":
   {"long_name": "Chaikin Money Flow",
    "short_name": "CMF",
    "required_input_data": ["close", "volume", "high", "low"],
    "graph_input_columns": ["close"],
    "graph_y_label": "CMF | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "ChaikinOscillator":
   {"long_name": "Chaikin Oscillator",
    "short_name": "CO",
    "required_input_data": ["close", "volume", "high", "low"],
    "graph_input_columns": ["close"],
    "graph_y_label": "CO | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "ChandeMomentumOscillator":
   {"long_name": "Chande Momentum Oscillator",
    "short_name": "CMO",
    "required_input_data": ["close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "CMO | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "CommodityChannelIndex":
   {"long_name": "Commodity Channel Index",
    "short_name": "CCI",
    "required_input_data": ["high", "low", "close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "CCI | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "DetrendedPriceOscillator":
   {"long_name": "Detrended Price Oscillator",
    "short_name": "DPO",
    "required_input_data": ["close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "DPO | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "DirectionalMovementIndex":
   {"long_name": "Directional Movement Index",
    "short_name": "DMI",
    "required_input_data": ["high", "low", "close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "DMI | Price",
    "graph_lines_color": ["black", "limegreen", "red", "cornflowerblue",
                          "tomato", "orange"],
    "graph_alpha_values": [0.5, 1.0, 1.0, 1.0, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "DoubleExponentialMovingAverage":
   {"long_name": "Double Exponential Moving Average",
    "short_name": "DEMA",
    "required_input_data": ["close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": False
    }, "EaseOfMovement":
   {"long_name": "Ease Of Movement",
    "short_name": "EMV",
    "required_input_data": ["high", "low", "volume"],
    "graph_input_columns": [],
    "graph_y_label": "EMV",
    "graph_lines_color": ["limegreen", "tomato"],
    "graph_alpha_values": [1.0, 1.0],
    "graph_areas": None,
    "graph_subplots": False
    }, "Envelopes":
   {"long_name": "Envelopes (Trading Bands)",
    "short_name": "ENV",
    "required_input_data": ["close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "Price",
    "graph_lines_color": ["black", "limegreen", "tomato"],
    "graph_alpha_values": [0.5, 1.0, 1.0],
    "graph_areas": None,
    "graph_subplots": False
    }, "FibonacciRetracement":
   {"long_name": "Fibonacci Retracement",
    "short_name": "FR",
    "required_input_data": ["close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "Price",
    "graph_lines_color": ["black", "limegreen", "peru", "cornflowerblue",
                          "tomato", "orange", "brown"],
    "graph_alpha_values": [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    "graph_areas": None,
    "graph_subplots": False
    }, "ForecastOscillator":
   {"long_name": "Forecast Oscillator",
    "short_name": "FOSC",
    "required_input_data": ["close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "FOSC | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "IchimokuCloud":
   {"long_name": "Ichimoku Cloud",
    "short_name": "IC",
    "required_input_data": ["high", "low", "close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "Price",
    "graph_lines_color": ["black", "cornflowerblue", "tomato", "limegreen",
                          "orange", "purple"],
    "graph_alpha_values": [0.5, 1.0, 1.0, 1.0, 1.0, 1.0],
    "graph_areas": [{'x': 'ti_index',
                     'y1': [0, 'ti_data', 'senkou_a'],
                     'y2': [0, 'ti_data', 'senkou_b'],
                     'color': 'lightblue'}],
    "graph_subplots": False
    }, "IntradayMovementIndex":
   {"long_name": "Intraday Movement Index",
    "short_name": "IMI",
    "required_input_data": ["open", "close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "IMI | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "KlingerOscillator":
   {"long_name": "Klinger Oscillator",
    "short_name": "KO",
    "required_input_data": ["high", "low", "close", "volume"],
    "graph_input_columns": ["close"],
    "graph_y_label": "KO | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "LinearRegressionIndicator":
   {"long_name": "Linear Regression Indicator",
    "short_name": "LRI",
    "required_input_data": ["close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": False
    }, "LinearRegressionSlope":
   {"long_name": "Linear Regression Slope",
    "short_name": "LRS",
    "required_input_data": ["close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "LRS | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "MarketFacilitationIndex":
   {"long_name": "Market Facilitation Index",
    "short_name": "MFI",
    "required_input_data": ["high", "low", "volume"],
    "graph_input_columns": ["volume"],
    "graph_y_label": "MFI | Volume",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "MassIndex":
   {"long_name": "Mass Index",
    "short_name": "MI",
    "required_input_data": ["high", "low", "close"],
    "graph_input_columns": ["close", "9_ema"],
    "graph_y_label": "MI | Price",
    "graph_lines_color": ["black", "tomato", "limegreen"],
    "graph_alpha_values": [0.5, 0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "MedianPrice":
   {"long_name": "Median Price",
    "short_name": "MP",
    "required_input_data": ["high", "low", "close"],
    "graph_input_columns": ["close_ema"],
    "graph_y_label": "Price",
    "graph_lines_color": ["red", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": False
    }, "Momentum":
   {"long_name": "Momentum",
    "short_name": "MOM",
    "required_input_data": ["close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "MOM | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "MovingAverage":
   {"long_name": "Moving Average",
    "short_name": "MA",
    "required_input_data": ["close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": False
    }, "MovingAverageConvergenceDivergence":
   {"long_name": "Moving Average Convergence Divergence",
    "short_name": "MACD",
    "required_input_data": ["close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "MACD | Price",
    "graph_lines_color": ["black", "cornflowerblue", "tomato"],
    "graph_alpha_values": [0.5, 1.0, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "NegativeVolumeIndex":
   {"long_name": "Negative Volume Index",
    "short_name": "NVI",
    "required_input_data": ["close", "volume"],
    "graph_input_columns": ["close"],
    "graph_y_label": "NVI | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "OnBalanceVolume":
   {"long_name": "On Balance Volume",
    "short_name": "OBV",
    "required_input_data": ["close", "volume"],
    "graph_input_columns": ["close"],
    "graph_y_label": "Volume | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "ParabolicSAR":
   {"long_name": "Parabolic SAR",
    "short_name": "PSAR",
    "required_input_data": ["high", "low", "close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "PSAR",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": False
    }, "Performance":
   {"long_name": "Performance",
    "short_name": "PERF",
    "required_input_data": ["close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "PERF | Price",
    "graph_lines_color": ["black", "limegreen", "tomato"],
    "graph_alpha_values": [0.5, 1.0, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "PositiveVolumeIndex":
   {"long_name": "Positive Volume Index",
    "short_name": "PVI",
    "required_input_data": ["close", "volume"],
    "graph_input_columns": ["close"],
    "graph_y_label": "PVI | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "PriceAndVolumeTrend":
   {"long_name": "Price And Volume Trend",
    "short_name": "PVT",
    "required_input_data": ["close", "volume"],
    "graph_input_columns": ["close"],
    "graph_y_label": "PVT | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "PriceChannel":
   {"long_name": "Price Channel",
    "short_name": "PCH",
    "required_input_data": ["high", "low", "close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "PCH",
    "graph_lines_color": ["black", "limegreen", "tomato"],
    "graph_alpha_values": [0.5, 1.0, 1.0],
    "graph_areas": None,
    "graph_subplots": False
    }, "PriceOscillator":
   {"long_name": "Price Oscillator",
    "short_name": "POSC",
    "required_input_data": ["close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "POSC | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "PriceRateOfChange":
   {"long_name": "Price Rate Of Change",
    "short_name": "PRC",
    "required_input_data": ["close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "PRC | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "ProjectionBands":
   {"long_name": "Projection Bands",
    "short_name": "PBS",
    "required_input_data": ["high", "low", "close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "PBS",
    "graph_lines_color": ["black", "limegreen", "tomato"],
    "graph_alpha_values": [0.5, 1.0, 1.0],
    "graph_areas": None,
    "graph_subplots": False
    }, "ProjectionOscillator":
   {"long_name": "Projection Oscillator",
    "short_name": "POSC",
    "required_input_data": ["high", "low", "close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "POSC | Price",
    "graph_lines_color": ["black", "limegreen", "tomato"],
    "graph_alpha_values": [0.5, 1.0, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "Qstick":
   {"long_name": "Qstick",
    "short_name": "QST",
    "required_input_data": ["open", "close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "QST | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "RangeIndicator":
   {"long_name": "Range Indicator",
    "short_name": "RI",
    "required_input_data": ["high", "low", "close", "volume"],
    "graph_input_columns": ["close"],
    "graph_y_label": "RI | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "RelativeMomentumIndex":
   {"long_name": "Relative Momentum Index",
    "short_name": "RMI",
    "required_input_data": ["close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "RMI | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "RelativeStrengthIndex":
   {"long_name": "Relative Strength Index",
    "short_name": "RSI",
    "required_input_data": ["close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "RSI | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "RelativeVolatilityIndex":
   {"long_name": "Relative Volatility Index",
    "short_name": "RVI",
    "required_input_data": ["high", "low"],
    "graph_input_columns": ["high", "low"],
    "graph_y_label": "RVI | Price",
    "graph_lines_color": ["limegreen", "tomato", "limegreen"],
    "graph_alpha_values": [0.5, 0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "StandardDeviation":
   {"long_name": "Standard Deviation",
    "short_name": "SD",
    "required_input_data": ["close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "SD | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "StochasticMomentumIndex":
   {"long_name": "Stochastic Momentum Index",
    "short_name": "SMI",
    "required_input_data": ["high", "low", "close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "SMI | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "StochasticOscillator":
   {"long_name": "Stochastic Oscillator",
    "short_name": "SO",
    "required_input_data": ["high", "low", "close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "Percentage | Price",
    "graph_lines_color": ["black", "cornflowerblue", "tomato"],
    "graph_alpha_values": [0.5, 1.0, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "SwingIndex":
   {"long_name": "Swing Index",
    "short_name": "SWI",
    "required_input_data": ["open", "high", "low", "close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "SWI | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "TimeSeriesForecast":
   {"long_name": "Time Series Forecast",
    "short_name": "TSF",
    "required_input_data": ["close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": False
    }, "TripleExponentialMovingAverage":
   {"long_name": "Triple Exponential Moving Average",
    "short_name": "TEMA",
    "required_input_data": ["close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": False
    }, "TypicalPrice":
   {"long_name": "TypicalPrice",
    "short_name": "TP",
    "required_input_data": ["high", "low", "close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": False
    }, "UltimateOscillator":
   {"long_name": "Ultimate Oscillator",
    "short_name": "UOSC",
    "required_input_data": ["high", "low", "close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "UOSC | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "VerticalHorizontalFilter":
   {"long_name": "Vertical Horizontal Filter",
    "short_name": "VHF",
    "required_input_data": ["close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "VHF | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "VolatilityChaikins":
   {"long_name": "Volatility Chaikins",
    "short_name": "VCH",
    "required_input_data": ["high", "low"],
    "graph_input_columns": [],
    "graph_y_label": "VCH",
    "graph_lines_color": ["limegreen"],
    "graph_alpha_values": [1.0],
    "graph_areas": None,
    "graph_subplots": False
    }, "VolumeOscillator":
   {"long_name": "Volume Oscillator",
    "short_name": "VOSC",
    "required_input_data": ["volume"],
    "graph_input_columns": ["volume"],
    "graph_y_label": "VOSC | Volume",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "VolumeRateOfChange":
   {"long_name": "Volume Rate Of Change",
    "short_name": "VROC",
    "required_input_data": ["volume"],
    "graph_input_columns": ["volume"],
    "graph_y_label": "VROC | Volume",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "WeightedClose":
   {"long_name": "WeightedClose",
    "short_name": "WC",
    "required_input_data": ["high", "low", "close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": False
    }, "WildersSmoothing":
   {"long_name": "Wilders Smoothing",
    "short_name": "WS",
    "required_input_data": ["close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": False
    }, "WilliamsAccumulationDistribution":
   {"long_name": "Williams Accumulation Distribution",
    "short_name": "WAD",
    "required_input_data": ["high", "low", "close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "WAD | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "WilliamsR":
   {"long_name": "Williams %R",
    "short_name": "WR",
    "required_input_data": ["high", "low", "close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "WR | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [0.5, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }
   }
