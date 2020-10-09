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
  {"BollingerBands":
   {"long_name": "Bollinger Bands",
    "short_name": "BB",
    "required_input_data": ["close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "Price",
    "graph_lines_color": ["black", "cornflowerblue", "limegreen", "tomato"],
    "graph_alpha_values": [0.5, 1.0, 1.0, 1.0],
    "graph_areas": None,
    "graph_subplots": False
    }, "DirectionalMovementIndex":
   {"long_name": "Directional Movement Index",
    "short_name": "DX",
    "required_input_data": ["high", "low", "close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "DMI | Price",
    "graph_lines_color": ["black", "limegreen", "red", "cornflowerblue",
                          "tomato", "orange"],
    "graph_alpha_values": [0.5, 1.0, 1.0, 1.0, 1.0],
    "graph_areas": None,
    "graph_subplots": True
    }, "FibonacciRetracement":
   {"long_name": "Fibonacci Retracement",
    "short_name": "FR",
    "required_input_data": ["close"],
    "graph_input_columns": ["close"],
    "graph_y_label": "Price",
    "graph_lines_color": ["black", "limegreen", "brown", "peru", "orange",
                          "red"],
    "graph_alpha_values": [None],
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
    "graph_alpha_values": [None],
    "graph_areas": [{'x': 'ti_index',
                     'y1': ['ti_data', 'Senkou A'],
                     'y2': ['ti_data', 'Senkou B'],
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
    "graph_lines_color": ["black", "tomato"],
    "graph_alpha_values": [None],
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
