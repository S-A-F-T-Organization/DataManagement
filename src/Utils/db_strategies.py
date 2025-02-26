"""Strategy classes for setting up the databases"""
import os
from abc import ABC, abstractmethod
from typing import List

from sqlalchemy import Engine

from src.Utils.config_info import ConfigInfo
from src.Utils.helpers import initalize_db_engine, create_table


## Strategy Base Classes ##
class HistoricalPricesStrategy(ABC):
    """The base class for creating the historical prices tables"""

    def __init__(self, config_info: ConfigInfo):
        self.db_path = config_info.db_path
        self.db_dialect = config_info.db_dialect
        self.scripts_base = "src/SQLTables/HistoricalPrices"
        self.config_info = config_info

    @property
    def db_engine(self) -> Engine:
        """The SQLAlchemy engine for the database."""
        db_engine = initalize_db_engine(
            self.db_dialect, 
            self.db_path, 
            self.config_info.db_name
        )
        return db_engine

    @abstractmethod
    def get_tables(self) -> List[str]:
        """This method returns a list of all tables in the database"""

    def create_historical_prices_tables(self) -> None:
        """This method creates the historical prices tables for the database"""
        tables = self.get_tables()

        for script in tables:
            full_path = os.path.join(self.scripts_base, script)
            create_table(db_engine=self.db_engine, full_path=full_path)


class MetadataStrategies(ABC):
    """The abstract baseclass for generating the metadata tables"""

    def __init__(self, config_info: ConfigInfo):
        self.db_path = config_info.db_path
        self.db_dialect = config_info.db_dialect
        self.security_types = config_info.security_types
        self.scripts_base = "src/SQLTables/SecuritiesMetadata"
        self.config_info = config_info

    @property
    def db_engine(self) -> Engine:
        """The SQLAlchemy engine for the database."""
        db_engine = initalize_db_engine(
            self.db_path, self.db_dialect, self.config_info.db_name
        )
        return db_engine

    @abstractmethod
    def get_first_scripts(self) -> List[str]:
        """This method returns the first scripts to be run"""

    @abstractmethod
    def get_main_scripts(self) -> List[str]:
        """This method returns the main table for the metadata of the given security type"""

    def create_metadata_tables(self) -> None:
        """This method creates the metadata tables for the database"""
        first_tables = self.get_first_scripts()
        main_tables = self.get_main_scripts()

        for script in first_tables:
            full_path = os.path.join(self.scripts_base, script)
            create_table(db_engine=self.db_engine, full_path=full_path)

        for script in main_tables:
            full_main = os.path.join(self.scripts_base, script)
            create_table(db_engine=self.db_engine, full_path=full_main)


## Concrete Implementations of Strategies ##
class ToIntStrategy(HistoricalPricesStrategy):
    """This strategy creates the historical prices tables for the database"""

    def get_tables(self) -> List[str]:
        tables = []
        if "OPT" in self.config_info.security_types:
            tables.append("options_ohlcv_int.sql")
        if self.config_info.ohlcv_flag:
            tables.append("security_prices_ohlcv_int.sql")
        if self.config_info.quotes_flag:
            if self.config_info.full_quotes_flag:
                tables.append("security_prices_mbp_full_int.sql")
            else:
                tables.append("security_prices_mbp_consolidated_int.sql")
        return tables


class RealStrategy(HistoricalPricesStrategy):
    """This strategy creates the historical prices tables for the database"""

    def get_tables(self) -> List[str]:
        tables = []
        if "OPT" in self.config_info.security_types:
            tables.append("options_ohlcv_float.sql")
        if self.config_info.ohlcv_flag:
            tables.append("security_prices_ohlcv_float.sql")
        if self.config_info.quotes_flag:
            if self.config_info.full_quotes_flag:
                tables.append("security_prices_mbp_full_float.sql")
            else:
                tables.append("security_prices_mbp_consolidated_float.sql")
        return tables


class StocksMetadata(MetadataStrategies):
    """This class creates the metadata tables if the user selects stocks"""

    def get_first_scripts(self) -> List[str]:
        """This method returns the first scripts to be run"""
        return [
            "stock_splits.sql",
            "sector_info.sql",
            "industry_info.sql",
            "fundamentals_snapshots.sql",
        ]

    def get_main_scripts(self) -> str:
        """This method returns the main tables for the metadata of the given security type"""
        return ["stock_table.sql", "equities_snapshots.sql"]


class ETFMetadata(MetadataStrategies):
    """This class creates the metadata tables if the user selects ETFs"""

    def get_first_scripts(self) -> List[str]:
        """This method returns the first scripts to be run"""
        return ["issuers.sql", "underlying_types.sql", "fundamentals_snapshots.sql"]

    def get_main_scripts(self) -> List[str]:
        """This method returns the main table for the metadata of the given security type"""
        return ["etf_table.sql", "equities_snapshots.sql"]


class MutualFundsMetadata(MetadataStrategies):
    """This class creates the metadata tables if the user selects Mutual Funds"""

    def get_first_scripts(self) -> List[str]:
        """This method returns the first scripts to be run"""
        return ["issuers.sql", "fundamentals_snapshots.sql"]

    def get_main_scripts(self) -> List[str]:
        """This method returns the main table for the metadata of the given security type"""
        return ["mutual_funds_table.sql", "mutual_fund_snapshots.sql"]


class ForexMetadata(MetadataStrategies):
    """This class creates the metadata tables if the user selects Forex"""

    def get_first_scripts(self) -> List[str]:
        """This method returns the first scripts to be run"""
        return ["currency_metadata.sql"]

    def get_main_scripts(self) -> List[str]:
        """This method returns the main table for the metadata of the given security type"""
        return ["cash_table.sql"]


class FuturesMetadata(MetadataStrategies):
    """This class creates the metadata tables if the user selects Futures"""

    def get_first_scripts(self) -> List[str]:
        """This method returns the first scripts to be run"""
        return ["underlying_types.sql"]

    def get_main_scripts(self) -> List[str]:
        """This method returns the main table for the metadata of the given security type"""
        return ["fut_table.sql"]


class CoreTables:
    """Creates the core tables according to users preferenecs."""

    def __init__(self, config_info: ConfigInfo):
        self.config_info = config_info
        self.core_folder = "src/SQLTables/Core"
        self.first_scripts = ["security_exchange.sql", "security_types.sql", "securities_info.sql"]

    @property
    def db_engine(self) -> Engine:
        """The SQLAlchemy engine for the database."""
        db_engine = initalize_db_engine(
            self.config_info.db_dialect,
            self.config_info.db_path,
            self.config_info.db_name,
        )
        return db_engine

    def create_core_tables(self) -> None:
        """Creates the core tables."""

        for script in self.first_scripts:
            full_path = os.path.join(self.core_folder, script)
            create_table(db_engine=self.db_engine, full_path=full_path)


class PortfolioDBTables:
    """Creates the portfolio database tables according to users preferences."""

    def __init__(self, config_info: ConfigInfo):
        self.config_info = config_info
        self.core_folder = "src/SQLTables/PortfolioDB"

    @property
    def db_engine(self) -> Engine:
        """The SQLAlchemy engine for the database."""
        db_engine = initalize_db_engine(
            self.config_info.db_dialect,
            self.config_info.db_path,
            self.config_info.db_name,
        )
        return db_engine

    @property
    def inference_tables(self) -> list[str]:
        """This method returns the inference tables for the portfolio database"""
        return [
            "strategies.sql",
            "model_libraries.sql",
            "model_types.sql",
            "models.sql",
            "strategy_modules.sql",
            "inference_steps.sql",
            "sessions.sql",
            "inferences.sql",
            "inference_times.sql",
        ]

    @property
    def transaction_tables(self) -> list[str]:
        """This method returns the transaction tables for the portfolio database"""
        return [
            "account_info.sql",
            "transaction_types.sql",
            "transactions.sql",
            "order_actions.sql",
            "order_types.sql",
            "all_orders.sql",
            "executed_orders.sql",
            "cancelled_orders.sql",
            "conditional_orders.sql",
        ]

    def create_portfolio_tables(self) -> None:
        """This method creates the portfolio tables for the database"""
        # create the inference tables
        for script in self.inference_tables:
            full_path = os.path.join(self.core_folder, script)
            create_table(db_engine=self.db_engine, full_path=full_path)
        # create the transaction tables
        for script in self.transaction_tables:
            full_path = os.path.join(self.core_folder, script)
            create_table(db_engine=self.db_engine, full_path=full_path)
