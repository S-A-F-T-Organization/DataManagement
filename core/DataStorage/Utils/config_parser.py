import yaml
from core.DataStorage.Utils.helpers import DataStorageHelpers as dsh
import warnings
from typing import Any, Dict, List

class DBConfigParser:

    """
    This class manages the initialization of the database as specified in the user's config file

    Parameters:
    - config_path(optional[str]): The path to the users config file. If setup correctly it should not be needed so it is optional. If the user runs into problems they can specify the path to their config file.

    Attributes:
    - logger (Logger):
    - market_data_flag (bool):
    - market_data_flag (bool):
    - portfolio_data_flag (bool): 
    - to_int_flag (bool):
    - ohlcv_flag (bool):
    - quotes_flag (bool):  
    - db_dialect (str):
    - mkt_data_db_path (str):
    - portfolio_data_db_path (str):
    - security_types (list[str]):
    - seed_data (list[str]):

    Methods:
    - parsing:
        - parse_schema_info:
        - parse_db_info:
        - parse_list_info:
    - Checks
    """

    def __init__(self, config_path:str='config/my_config.yml'):
        self.logger = dsh.setup_log_to_console()
        # Read in the config file information
        try:
            # Read in YAML config file
            with open(f'{config_path}', 'r') as f:
                self.config_data:dict = yaml.safe_load(f)
            self.get_config_info()
        except FileNotFoundError as fe:
            self.logger.error(f"Could not find configuration file: {config_path}", exc_info=True)
            raise
        except Exception as e:
            self.logger.error(f'Error reading the configuration file {config_path}', exc_info=True)
            raise

    def parse_schema_info(self) -> dict:
        """
        This function parses through the schema section of the configuration file, sets boolean flags for each key in the section, and returns the dictionary containing the schema info

        Returns:
        - schema_info(dict): The dictionary containing the schema information
        """
        schema_info:dict = self.config_data['schemas']
        self.market_data_flag:bool = schema_info['market_data']
        self.portfolio_data_flag = schema_info['market_data']
        self.to_int_flag:bool = schema_info['convert_price_to_int']
        self.ohlcv_flag:bool = schema_info['ohlcv']
        self.quotes_flag:bool = schema_info['quotes']
        return schema_info
    
    def parse_db_info(self):
        """
        This method retrieves the important database info from each of the keys in the database section and returns a dictionary containing the database setup info

        Returns:
        - db_info (dict): A dictionary containing the database info from the database section of the config file
        """
        db_info:dict[str, str] = self.config_data['database']
        self.db_dialect = db_info['dialect']
        self.mkt_data_db_path = db_info['mkt_data_db_path']
        self.portfolio_data_db_path = db_info['portfolio_data_db_path']
        return db_info
    
    def parse_list_info(self) -> None:
        """
        This creates a list for for the security types being setup and the seed data desired
        """
        self.security_types:list[str] = self.config_data['security_types']
        self.seed_data:list[str] = self.config_data['seed_data']

    
    def normalize_sec_types(self) -> None:
        """
        This method normalizes the formatting of the security types values
        """
        clean_sec_types = []
        for sec_type in self.security_types:
            sec_type = sec_type.upper()
            sec_type = sec_type.strip()
            clean_sec_types.append(sec_type)
        self.security_types = clean_sec_types
    
    def normalize_seed_data(self) -> None:
        """
        This method normalizes the formatting of the security types values
        """
        clean_seed_data = []
        for seed_data in self.seed_data:
            seed_data = seed_data.upper()
            seed_data = seed_data.strip()
            clean_seed_data.append(seed_data)
        self.seed_data = clean_seed_data

    def schema_checks(self):
        if self.quotes_flag: warnings.warn(
                "Quote level data is not currently supported, we are hoping to have support for this soon! Setup for this data granularity will be ignored",
                UserWarning,
                stacklevel=2
            )
        if self.to_int_flag: warnings.warn(
                f"{self.to_int_flag} is set to `True`, historical security prices will be stored as integers for precision and storage efficiency",
                UserWarning,
                stacklevel=2
            )

    def db_info_checks(self):
        if self.db_dialect not in ["sqlite", 'sqlite3']: raise ValueError("We currently only offer support for SQLite, with support for PostgreSQL coming soon! If you believe you configured the setup for SQLite but are receiving this error, try either 'sqlite' or 'sqlite3'")
    
    def sec_type_checks(self):
        supported_sec_types = ["STK", "ETF", "CASH", "FUT"]
        sec_type_future = ["OPT", "IND", "FOP", "BOND", "CMDTY", "FUND", "BAG", "WAR", "NEWS"]
        for sec_type in self.security_types:
            if sec_type in sec_type_future:
                raise ValueError(f"We currently do not offer support for the security type {sec_type}, the currently supported security types are: {supported_sec_types}")
            elif sec_type not in supported_sec_types:
                raise ValueError(f"Unrecognized security type in configuration file, the security types currently supported are: {supported_sec_types}")
    
    def seed_data_checks(self):
        pass
    
    def checks(self):
        self.sec_type_checks()
        self.schema_checks()
        self.db_info_checks()
        self.seed_data_checks()
    
    def parse_all(self):
        self.parse_db_info()
        self.parse_list_info()
        self.parse_schema_info()
    
    def norm_all(self):
        self.normalize_sec_types()
        self.normalize_seed_data()
    
    def get_config_info(self):
        self.parse_all()
        self.norm_all()
        self.schema_checks()