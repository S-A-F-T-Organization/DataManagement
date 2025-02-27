""" This module contains the data classes for the historical pricess tables """
from dataclasses import dataclass
from typing import Union, List

@dataclass
class DividendHistory:
    """
    Represents the dividend history of a security.
    Supports either single values or lists of values.
    """
    symbol_id: Union[int, List[int]] = None
    datetime: Union[int, List[int]] = None
    div_value: Union[float, List[float]] = None
    div_yield: Union[float, List[float]] = None

@dataclass
class SecurityPricesOHLCV:
    """
    Represents OHLCV (Open, High, Low, Close, Volume) security prices.
    Supports either single values or lists of values.
    """
    symbol_id: Union[int, List[int]] = None
    datetime: Union[int, List[int]] = None
    open_price: Union[float, List[float]] = None
    high_price: Union[float, List[float]] = None
    low_price: Union[float, List[float]] = None
    close_price: Union[float, List[float]] = None
    volume: Union[int, List[int]] = None
