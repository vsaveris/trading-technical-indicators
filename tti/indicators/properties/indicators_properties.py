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
  {"OnBalanceVolume":
   {"long_name": "On Balance Volume",
    "short_name": "OBV",
    "required_input_data": ["close", "volume"],
    "graph_input_columns": ["close"],
    "graph_y_label": "Volume | Price",
    "graph_lines_color": ["black", "limegreen"],
    "graph_alpha_values": [None],
    "graph_areas": None,
    "graph_subplots": True
    }
   }
