"""
Trading-Technical-Indicators (tti) python library

File name: constants.py
    Library constants defined under the tti.utils package.
"""

# Possible values for the Trading Signal
TRADE_SIGNALS = {"buy": ("buy", -1), "hold": ("hold", 0), "sell": ("sell", 1)}

# Possible values for ML classes (price direction)
ML_CLASSES = {"DOWN": 0, "UP": 1}

# When ``all`` Technical Indicators are used as data features in the ML Data
ALL_TI_FEATURES = [
    {"ti": "AccumulationDistributionLine", "kwargs": {}},
    {"ti": "AverageTrueRange", "kwargs": {}},
    {"ti": "BollingerBands", "kwargs": {}},
    {"ti": "ChaikinMoneyFlow", "kwargs": {}},
    {"ti": "ChaikinOscillator", "kwargs": {}},
    {"ti": "ChandeMomentumOscillator", "kwargs": {}},
    {"ti": "CommodityChannelIndex", "kwargs": {}},
    {"ti": "DetrendedPriceOscillator", "kwargs": {}},
    {"ti": "DirectionalMovementIndex", "kwargs": {}},
    {"ti": "DoubleExponentialMovingAverage", "kwargs": {}},
    {"ti": "EaseOfMovement", "kwargs": {}},
    {"ti": "Envelopes", "kwargs": {}},
    {"ti": "FibonacciRetracement", "kwargs": {}},
    {"ti": "ForecastOscillator", "kwargs": {}},
    {"ti": "IchimokuCloud", "kwargs": {}},
    {"ti": "IntradayMomentumIndex", "kwargs": {}},
    {"ti": "KlingerOscillator", "kwargs": {}},
    {"ti": "LinearRegressionIndicator", "kwargs": {}},
    {"ti": "LinearRegressionSlope", "kwargs": {}},
    {"ti": "MarketFacilitationIndex", "kwargs": {}},
    {"ti": "MassIndex", "kwargs": {}},
    {"ti": "MedianPrice", "kwargs": {}},
    {"ti": "Momentum", "kwargs": {}},
    {"ti": "MovingAverage", "kwargs": {"ma_type": "simple"}},
    {"ti": "MovingAverage", "kwargs": {"ma_type": "exponential"}},
    {"ti": "MovingAverage", "kwargs": {"ma_type": "time_series"}},
    {"ti": "MovingAverage", "kwargs": {"ma_type": "triangular"}},
    {"ti": "MovingAverage", "kwargs": {"ma_type": "variable"}},
    {"ti": "MovingAverageConvergenceDivergence", "kwargs": {}},
    {"ti": "NegativeVolumeIndex", "kwargs": {}},
    {"ti": "OnBalanceVolume", "kwargs": {}},
    {"ti": "ParabolicSAR", "kwargs": {}},
    {"ti": "Performance", "kwargs": {}},
    {"ti": "PositiveVolumeIndex", "kwargs": {}},
    {"ti": "PriceAndVolumeTrend", "kwargs": {}},
    {"ti": "PriceChannel", "kwargs": {}},
    {"ti": "PriceOscillator", "kwargs": {}},
    {"ti": "PriceRateOfChange", "kwargs": {}},
    {"ti": "ProjectionBands", "kwargs": {}},
    {"ti": "ProjectionOscillator", "kwargs": {}},
    {"ti": "Qstick", "kwargs": {}},
    {"ti": "RangeIndicator", "kwargs": {}},
    {"ti": "RelativeMomentumIndex", "kwargs": {}},
    {"ti": "RelativeStrengthIndex", "kwargs": {}},
    {"ti": "RelativeVolatilityIndex", "kwargs": {}},
    {"ti": "StandardDeviation", "kwargs": {}},
    {"ti": "StochasticMomentumIndex", "kwargs": {}},
    {"ti": "StochasticOscillator", "kwargs": {"k_slowing_periods": 1}},
    {"ti": "StochasticOscillator", "kwargs": {"k_slowing_periods": 3}},
    {"ti": "SwingIndex", "kwargs": {}},
    {"ti": "TimeSeriesForecast", "kwargs": {}},
    {"ti": "TripleExponentialMovingAverage", "kwargs": {}},
    {"ti": "TypicalPrice", "kwargs": {}},
    {"ti": "UltimateOscillator", "kwargs": {}},
    {"ti": "VerticalHorizontalFilter", "kwargs": {}},
    {"ti": "VolatilityChaikins", "kwargs": {}},
    {"ti": "VolumeOscillator", "kwargs": {}},
    {"ti": "VolumeRateOfChange", "kwargs": {}},
    {"ti": "WeightedClose", "kwargs": {}},
    {"ti": "WildersSmoothing", "kwargs": {}},
    {"ti": "WilliamsAccumulationDistribution", "kwargs": {}},
    {"ti": "WilliamsR", "kwargs": {}},
]
