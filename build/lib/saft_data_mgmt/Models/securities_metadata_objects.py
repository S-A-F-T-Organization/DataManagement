""" This contains all of the data classes for the security type specific metadata tables """
from dataclasses import dataclass
from typing import Union, List

@dataclass
class StocksMetadata:
    """
    _summary_
    """
    symbol_id:Union[int, List[int]] = None
    full_name:Union[str, List[str]] = None
    sp_component:Union[bool, List[bool]] = None
    nq_component:Union[bool, List[bool]] = None
    rty_component:Union[bool, List[bool]] = None
    djia_component:Union[bool, List[bool]] = None


@dataclass
class FuturesMetadata:
    """
    _summary_
    """
    symbol_id:Union[int, List[int]] = None
    multiplier:Union[float, List[float]] = None
    tick_size:Union[float, List[float]] = None
    tick_value:Union[float, List[float]] = None
    underlying_type_id:Union[int, List[int]] = None

@dataclass
class ETFMetadata:
    """
    _summary_
    """
    symbol_id:Union[int, List[int]] = None
    full_name:Union[str, List[str]] = None
    issuer_id:Union[int, List[int]] = None
    underlying_type_id:Union[int, List[int]] = None
    underlying_name:Union[str, List[str]] = None

@dataclass
class ForexMetadata:
    """
    _summary_
    """
    symbol_id:Union[int, List[int]] = None
    base_currency_id:Union[int, List[int]] = None
    quote_currency_id:Union[int, List[int]] = None

@dataclass
class CurrencyMetadata:
    """
    _summary_
    """
    currency_id:Union[int, List[int]] = None
    currency_abbr:Union[str, List[str]] = None

@dataclass
class SectorInfo:
    """
    _summary_
    """
    sector_id:Union[int, List[int]] = None
    sector_name:Union[str, List[str]] = None

@dataclass
class IndustryInfo:
    """
    _summary_
    """
    industry_id:Union[int, List[int]] = None
    industry_name:Union[str, List[str]] = None

@dataclass
class Issuers:
    """
    _summary_
    """
    issuer_id:Union[int, List[int]] = None
    issuer_name:Union[str, List[str]] = None

@dataclass
class UnderlyingTypes:
    """
    _summary_
    """
    underlying_type_id:Union[int, List[int]] = None
    underlying_name:Union[str, List[str]] = None
