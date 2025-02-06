""" This module stores dataclass objects for the core tables in the SAFT Core data tables """
from dataclasses import dataclass
from typing import Union, List

@dataclass
class SecuritiesInfo:
    """
    _summary_
    """
    symbol_id:Union[int, List[int]] = None
    symbol:Union[str, List[str]] = None
    security_type_id:Union[int, List[int]] = None
    to_int:Union[int, List[int]] = None
    exchange_id:Union[int, List[int]] = None
    rth_start_time_utc:Union[str, List[str]] = None
    rth_end_time_utc:Union[str, List[str]] = None

@dataclass
class SecurityTypes:
    """
    _summary_
    """
    security_type_id:Union[int, List[int]] = None
    security_type:Union[str, List[str]] = None

@dataclass
class SecurityExchanges:
    """
    _summary_
    """
    exchange_id:Union[int, List[int]] = None
    exchange_name:Union[str, List[str]] = None
    timezone:Union[str, List[str]] = None
