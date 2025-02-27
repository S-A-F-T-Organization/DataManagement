"""This module contains the ConfigInfo class, which is used how to setup a SAFT style db"""

from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ConfigInfo:
    """A class representing the configuration info."""

    # DB Attributes
    db_dialect: Optional[str] = None
    db_path: Optional[str] = None
    db_name: Optional[str] = None

    # Data type info
    market_data_flag: bool = False
    portfolio_data_flag: bool = False
    to_int_flag: bool = False
    ohlcv_flag: bool = False
    quotes_flag: bool = False
    full_quotes_flag: bool = False
    trade_quotes_flag: bool = False
    security_types: List[str] = field(default_factory=list)

    # Seed data
    seed_data: List[str] = field(default_factory=list)
