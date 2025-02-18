"""Strategies for generating the security metadata tables"""

import os
from typing import List
from abc import ABC, abstractmethod

from sqlalchemy import Engine

from src.Utils.configurator import ConfigInfo
from src.Utils.helpers import initalize_db_engine, create_table


class MetadataStrategies(ABC):
    """The abstract baseclass for generating the metadata tables"""

    def __init__(self, config_info: ConfigInfo):
        self.db_path = config_info.db_path
        self.db_dialect = config_info.db_dialect
        self.security_types = config_info.security_types
        self.scripts_base = "src/SQLTables/SecuritiesMetadata"

    @property
    def db_engine(self) -> Engine:
        """The SQLAlchemy engine for the database."""
        db_engine = initalize_db_engine(self.db_path, self.db_dialect)
        return db_engine

    @abstractmethod
    def get_first_scripts(self) -> List[str]:
        """This method returns the first scripts to be run"""

    @abstractmethod
    def get_main_script(self) -> str:
        """This method returns the main table for the metadata of the given security type"""

    def create_metadata_tables(self) -> None:
        """This method creates the metadata tables for the database"""
        first_tables = self.get_first_scripts()
        main_table = self.get_main_script()

        for script in first_tables:
            full_path = os.path.join(self.scripts_base, script)
            create_table(db_engine=self.db_engine, full_path=full_path)

        full_main = os.path.join(self.scripts_base, main_table)
        create_table(db_engine=self.db_engine, full_path=full_main)


class StocksMetadata(MetadataStrategies):
    """This class creates the metadata tables if the user selects stocks"""

    def get_first_scripts(self) -> List[str]:
        """This method returns the first scripts to be run"""
        return ["stock_splits.sql", "sector_info.sql", "industry_info.sql"]

    def get_main_script(self) -> str:
        """This method returns the main table for the metadata of the given security type"""
        return "stk_table.sql"


class ETFMetadata(MetadataStrategies):
    """This class creates the metadata tables if the user selects ETFs"""

    def get_first_scripts(self) -> List[str]:
        """This method returns the first scripts to be run"""
        return ["issuers.sql", "underlying_types.sql"]

    def get_main_script(self) -> str:
        """This method returns the main table for the metadata of the given security type"""
        return "etf_table.sql"


class ForexMetadata(MetadataStrategies):
    """This class creates the metadata tables if the user selects Forex"""
    
    def get_first_scripts(self):
        """This method returns the first scripts to be run"""
        return ["currency_metadata.sql"]
    
    def get_main_table(self):
        """This method returns the main table for the metadata of the given security type"""
        return "cash_table.sql"

class FuturesMetadata(MetadataStrategies):
    """This class creates the metadata tables if the user selects Futures"""
    def get_first_scripts(self) -> List[str]:
        """This method returns the first scripts to be run"""
        return ["underlying_types.sql"]

    def get_main_script(self) -> str:
        """This method returns the main table for the metadata of the given security type"""
        return "futures_table.sql"
