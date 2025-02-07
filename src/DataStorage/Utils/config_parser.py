"""
This module contains the config parser and config data object for initializing the database\
"""

import warnings
from dataclasses import dataclass
import yaml
from src.Utils.helpers import DataMgmtHelpers as dmh

@dataclass
class ConfigInfo:
    """
    _summary_
    """

    market_data_flag: bool = True
    portfolio_data_flag: bool = True
    to_int_flag: bool = False
    ohlcv_flag: bool = True
    quotes_flag: bool = False
    db_dialect: str = None
    db_path: str = None
    security_types: list[str] = None
    seed_data: list[str] = None

class DBConfigParser:
    """
    _summary_
    A class for parsing through the yaml configuration file to setup a dataclass containing the config data
    """
    def __init__(self, config_path: str = "config/my_config.yml"):
        self.logger = dmh.setup_log_to_console()
        # Read config file and initialize an default ConfigInfo instance
        try:
            with open(f"{config_path}", "r", encoding="utf-8") as f:
                self.config_data: dict = yaml.safe_load(f)
            self.config_info = ConfigInfo()
        except FileNotFoundError:
            self.logger.error(
                "Could not find configuration file: %c", config_path, exc_info=True
            )
            raise
        except Exception:
            self.logger.error(
                "Error reading the configuration file %c", config_path, exc_info=True
            )
            raise

    def parse_schema_info(self) -> dict:
        """
        _summary_
        This function parses through the schema section of the configuration file,
        updates all schema flags inf the ConfigInfo class to match the user's config,
        then returns the dictionary containing just the schema info

        Returns:
            schema_info: _description_: dict containing all of ther schema info keys and value
        """
        schema_info: dict = self.config_data["schemas"]
        self.config_info.market_data_flag = schema_info["market_data"]
        self.config_info.portfolio_data_flag = schema_info["market_data"]
        self.config_info.to_int_flag = schema_info["convert_price_to_int"]
        self.config_info.ohlcv_flag = schema_info["ohlcv"]
        self.config_info.quotes_flag = schema_info["quotes"]
        return schema_info

    def parse_db_info(self) -> dict:
        """
        _summary_
        This method retrieves important info from each of the keys in the database section,
        updates all db_info attributes in the ConfigInfo class,
        then returns a dictionary containing the database setup info

        Returns:
            db_info: _description_: A dictionary containing the database info from the config file
        """
        db_info: dict[str, str] = self.config_data["database"]
        self.config_info.db_dialect = db_info["dialect"]
        self.config_info.db_path = db_info["db_path"]
        return db_info

    def parse_list_info(self) -> None:
        """
        _summary_
        This creates a list for for the security types being setup and the seed data desired and
        updates the ConfigInfo class with these attributes
        """
        self.config_info.security_types = self.config_data["security_types"]
        self.config_info.seed_data = self.config_data["seed_data"]

    def normalize_sec_types(self) -> None:
        """
        _summary_
        This method normalizes the formatting of the security types values in the ConfigInfo security_types attribute
        """
        clean_sec_types = []
        for sec_type in self.config_info.security_types:
            sec_type = sec_type.upper()
            sec_type = sec_type.strip()
            clean_sec_types.append(sec_type)
        self.config_info.security_types = clean_sec_types

    def normalize_seed_data(self) -> None:
        """
        _summary_
        This method normalizes the formatting of the seed data values in the ConfigInfo seed_data attribute
        """
        clean_seed_data = []
        for seed_data in self.config_info.seed_data:
            seed_data = seed_data.upper()
            seed_data = seed_data.strip()
            clean_seed_data.append(seed_data)
        self.config_info.seed_data = clean_seed_data

    def schema_checks(self):
        """
        _summary_
        This checks for potential issues in the schema flags of the ConfigInfo attributes and raises relevant warnings
        """
        if self.config_info.quotes_flag:
            warnings.warn(
                "Quote level data is not currently supported, we are hoping support this soon!"
                "Setup for this data granularity will be ignored",
                UserWarning,
                stacklevel=2,
            )
        if self.config_info.to_int_flag:
            warnings.warn(
                f"{self.config_info.to_int_flag} is set to `True`."
                "Security prices will be stored as integers for precision and storage efficiency",
                UserWarning,
                stacklevel=2,
            )

    def db_info_checks(self):
        """
        _summary_
        This checks for issues in the database attributes of the ConfigInfo instance and raises relevant warnings
        Raises:
            ValueError: _description_: unsupported SQL dialect
        """
        if self.config_info.db_dialect not in ["sqlite", "sqlite3"]:
            raise ValueError(
                "We currently only offer support for SQLite with PostgreSQL support coming soon!",
                "If you believe you configured for SQLite but are receiving this error, try either 'sqlite' or 'sqlite3'",
            )

    def sec_type_checks(self):
        """
        _summary_

        Raises:
            ValueError: _description_: unsuported security type listed, with plans to support later
            ValueError: _description_: unsupported security type listed, no plans to support later
        """
        supported_sec_types = ["STK", "ETF", "CASH", "FUT"]
        sec_type_future = [
            "OPT",
            "IND",
            "FOP",
            "BOND",
            "CMDTY",
            "FUND",
            "BAG",
            "WAR",
            "NEWS",
        ]
        for sec_type in self.config_info.security_types:
            if sec_type in sec_type_future:
                raise ValueError(
                    f"We currently do not offer support for the security type {sec_type}",
                    "the currently supported security types are: {supported_sec_types}",
                )
            if sec_type not in supported_sec_types:
                raise ValueError(
                    f"Unrecognized security type in configuration file, we currentl support: {supported_sec_types}"
                )

    def check_all(self):
        """
        _summary_ 
        Runs all of the checks listed above in one function
        """
        self.sec_type_checks()
        self.schema_checks()
        self.db_info_checks()

    def parse_all(self):
        """
        _summary_
        Runs all of the parsing functions listed above in one function
        """
        self.parse_db_info()
        self.parse_list_info()
        self.parse_schema_info()

    def norm_all(self):
        """
        _summary_
        Runs all of the normalization functions listed above in one function
        """
        self.normalize_sec_types()
        self.normalize_seed_data()

    def get_config_info(self) -> ConfigInfo:
        """
        _summary_

        Returns:
            ConfigInfo: _description_
        """
        self.parse_all()
        self.norm_all()
        self.check_all()
        return self.config_info
