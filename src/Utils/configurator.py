"""This module contains the ConfigInfo class, which is used how to setup a SAFT style"""
from dataclasses import dataclass, field
from typing import List, Optional
import warnings

@dataclass
class ConfigInfo:
    """A class representing the configuration info."""

    market_data_flag: bool = False
    portfolio_data_flag: bool = False
    to_int_flag: bool = False
    ohlcv_flag: bool = False
    quotes_flag: bool = False
    db_dialect: Optional[str] = None
    db_path: Optional[str] = None
    db_name: Optional[str] = None
    security_types: List[str] = field(default_factory=list)
    seed_data: List[str] = field(default_factory=list)

    def normalize_sec_types(self) -> None:
        """Normalize the formatting of security types."""
        clean_sec_types = []
        for sec_type in self.security_types:
            clean_sec_types.append(sec_type.upper().strip())
        self.security_types = clean_sec_types

    def normalize_seed_data(self) -> None:
        """Normalize the formatting of seed data values."""
        clean_seed_data = []
        for sd in self.seed_data:
            clean_seed_data.append(sd.upper().strip())
        self.seed_data = clean_seed_data

    def schema_checks(self):
        """Check for potential issues in the schema flags of the ConfigInfo attributes."""
        if self.quotes_flag:
            warnings.warn(
                "Quote-level data is not currently supported. "
                "Setup for this data granularity will be ignored.",
                UserWarning,
                stacklevel=2
            )
        if self.to_int_flag:
            warnings.warn(
                "Prices will be stored as integers for precision and storage efficiency.",
                UserWarning,
                stacklevel=2
            )

    def db_info_checks(self):
        """Check database attributes and raise warnings or errors if needed."""
        if self.db_dialect not in ["sqlite", "sqlite3"]:
            raise ValueError(
                "We currently only offer support for SQLite (try 'sqlite' or 'sqlite3'). "
                "PostgreSQL support is coming soon!"
            )

    def sec_type_checks(self):
        """
        Check for unsupported or unrecognized security types.
        Raises
            - ValueError:
        """
        supported_sec_types = ['Stocks', 'ETFs', 'Forex', 'Futures']

        for sec_type in self.security_types:
            if sec_type not in supported_sec_types:
                raise ValueError(
                    f"Unrecognized security type '{sec_type}'. Supported types: {supported_sec_types}"
                )


    def clean_config(self) -> "ConfigInfo":
        """
        Normalizes and performs checks on config attributes.

        Returns:
            ConfigInfo: The same instance, updated in place.
        """
        # Run checks
        self.sec_type_checks()
        self.schema_checks()
        self.db_info_checks()
        # Run normalizations
        self.normalize_sec_types()
        self.normalize_seed_data()
        # Return updated instance
        return self
