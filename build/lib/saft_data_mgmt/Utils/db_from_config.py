"""This module contains all of the functionality to create a new database from a ConfigInfo class"""

from saft_data_mgmt.Utils import helpers
from saft_data_mgmt.Utils.config_info import ConfigInfo
from saft_data_mgmt.Utils import db_strategies as strats


class DBFromConfig:
    """
    This class manages all steps of creating the tables for the database depending on the users config file

    Args:
        - config_info (ConfigInfo): The dataclas storing the users configuration settings
    Attributes:
        - logger (Logger): logs info and warning to the console
        - config_info (ConfigInfo): see above
        - sql_base_path (str): the base path to the folder where all of the SQL tables are stored
    """

    def __init__(self, config_info: ConfigInfo):
        self.logger = helpers.setup_log_to_console()
        # Get config info
        self.config_info = config_info
        if self.config_info.security_types == ["ALL"]:
            self.config_info.security_types = [
                "STK",
                "ETF",
                "FUT",
                "FOREX",
                "FUND",
                "OPT",
            ]

    @property
    def securities_map(self) -> dict[str, strats.MetadataStrategies]:
        """This method returns the metadata map for the database"""
        securities_map = {
            "STK": strats.StocksMetadata,
            "ETF": strats.ETFMetadata,
            "FUT": strats.FuturesMetadata,
            "FOREX": strats.ForexMetadata,
            "FUND": strats.MutualFundsMetadata,
        }
        return securities_map

    def create_historical_prices(self):
        """This method creates the historical prices tables for the database"""
        self.logger.info("Creating historical prices tables")
        if self.config_info.to_int_flag:
            strats.ToIntStrategy(self.config_info).create_historical_prices_tables()
        else:
            strats.RealStrategy(self.config_info).create_historical_prices_tables()
        self.logger.info("Historical prices tables created")

    def create_metadata_tables(self):
        """This method creates the metadata tables for the database"""
        self.logger.info("Creating metadata tables")
        for sec_type in self.config_info.security_types:
            if sec_type in self.securities_map:
                strategy = self.securities_map[sec_type](self.config_info)
                strategy.create_metadata_tables()
            else:
                self.logger.warning(
                    "Security type %x not found in metadata map. Skipping.", sec_type
                )

    def create_config_tables(self):
        """This method creates all tables for the database"""
        self.logger.info("Creating tables")
        # Create the core tables
        strats.CoreTables(self.config_info).create_core_tables()
        self.logger.info("Core tables created")

        # Create the market data tables
        if self.config_info.market_data_flag:
            self.create_metadata_tables()
            self.create_historical_prices()
            self.logger.info("Market data tables created")

        # Create the portfolio tables
        if self.config_info.portfolio_data_flag:
            strats.PortfolioDBTables(self.config_info).create_portfolio_tables()
            self.logger.info("Portfolio tables created")

        self.logger.info("All tables created")
