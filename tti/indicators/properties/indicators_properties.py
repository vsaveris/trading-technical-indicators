"""
Trading-Technical-Indicators (tti) python library

File name: indicators_properties.py
    Properties definition for each implemented Technical Indicator.

Each indicator has its properties defined in the INDICATORS_PROPERTIES
dictionary. The format for each indicator is:

"<Indicator's Class Name>": {"long_name": <indicator's long name>,
    "short_name": <indicator's short name>,
    "required_input_data": <required input data (list of column names)>,
    "graph_input_columns": <list of column names from input data to be added to
         the graph> or [None],
    "graph_y_label": <label for the y-axis>,
    "graph_lines_color": <color for each line of the graph (list of matplotlib
         colors) or [None]>,
    "graph_alpha_values": <alpha value for each line of the graph or [None]>,
    "graph_areas": <areas (list of dictionaries): Includes the areas to be
         plotted by using the fill_between matplotlib method. Each member of
         the list should be a dictionary with the below keys:
            {'x':, 'y1':, 'y2':, 'color':}, see fill_between matplotlib method
            for more details. or None>
    "graph_subplots": <boolean for splitting input and indicator data in
         subplots (makes sense when graph_input_columns is set)>}
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
    }
   }
