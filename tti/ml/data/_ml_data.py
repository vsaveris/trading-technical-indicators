"""
Trading-Technical-Indicators (tti) python library

File name: _ml_data.py
    Implements a parent class for ML data, implementing a method for computing technical indicators for input dicts.
"""

from abc import ABC

from ...indicators import *


class MLData(ABC):
    @staticmethod
    def _compute_ti(df, ti_name, **kwargs):
        return eval(ti_name)(input_data=df, **kwargs).getTiData()
