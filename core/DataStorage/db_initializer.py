from sqlalchemy import create_engine, Engine, text
import yaml
import logging
import os

class DBInitializer:
    """
    This class manages the initialization of the database as specified in the user's config file

    Parameters:
    - config_path(optional[str]): The path to the users config file. If setup correctly it should not be needed so it is optional. If the user runs into problems they can specify the path to their config file.
    """

    def __init__(self, config_path:str='config/my_config.yml'):
        # Setup logger/stream handler
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(messages)s'
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        # Read in the config file information
        try:
            # Read in YAML configuration files
            with open(f'{config_path}', 'r') as f:
                self.config_data:dict = yaml.safe_load(f)
                self.db_info:dict[str, str] = self.config_data['database']
                self.market_data_flag:bool = self.config_data['schemas']['market_data']
                self.portfolio_data_flag:bool = self.config_data['schemas']['portfolio_data']
                self.to_int_flag:bool = self.config_data['schemas']['convert_price_to_int']
                self.security_types:list = self.config_data['security_types']
                self.seed_data:list[str] = self.config_data['seed_data']
        except FileNotFoundError as fe:
            self.logger.error(f"Could not find configuration file: {config_path}", fe)
            raise
        except Exception as e:
            self.logger.error(f'Error reading the configuration file {config_path}', e)
            raise
    
    def normalize_config(self):
        """
        This method will normalize config file inputs such as ensuring all are lower case
        """
        pass

    def config_checks(self):
        # Schema checks
        if self.config_data['schemas']['quotes']: raise UserWarning("Quote level data is not currently supported, we are hoping to have support for this soon! Setup for this data granularity will be ignored")
        if self.portfolio_data_flag: raise UserWarning("We our portfolio data warehouse is not currently stable, expect an update soon to use this function!")
        if self.to_int_flag: raise UserWarning(f"{self.to_int_flag} is set to `True`, historical security prices will be stored as integers for precision and storage efficiency")
        # Database checks
        if self.db_info['driver'] not in ["sqlite", 'sqlite3']: raise ValueError("We currently only offer support for SQLite, with support for PostgreSQL coming soon! If you believe you configured the setup for SQLite but are receiving this error, try either 'sqlite' or 'sqlite3'")
        # Security type checks
        supported_sec_types = ["STK", "ETF", "CASH", "FUT"]
        sec_type_future = ["OPT", "IND", "FOP", "BOND", "CMDTY", "FUND", "BAG", "WAR", "NEWS"]
        for sec_type in self.security_types:
            if sec_type not in supported_sec_types and sec_type not in sec_type_future:
                raise ValueError(f"There seems be an unrecognized security type in the configuration file, the currently supported security types are: {supported_sec_types}")
            elif sec_type in sec_type_future:
                raise ValueError(f"We currently do not offer support for the security type {sec_type}, the currently supported security types are: {supported_sec_types}")
        # Seed Data checks
    def initialize_mkt_data_engine(self) -> Engine:
        if self.market_data_flag:
            try:
                if self.db_info['driver'] == "sqlite3" and not self.db_info['mkt_data_dbpath'].startswith('sqlite:///'):
                    engine_path = 'sqlite:///' + self.db_info['mkt_data_dbpath']
                mkt_datat_engine = create_engine(engine_path)
                return mkt_datat_engine
            except Exception as e:
                self.logger.error("Error ocurred while initializing the market data engine:", e)
                raise
        else:
            return None
    
    def initialize_portfolio_data_engine(self) -> Engine:
        if self.portfolio_data_flag:
            try:
                if self.db_info['driver'] == "sqlite3" and not self.db_info['portfolio_data_dbpath'].startswith('sqlite:///'):
                    engine_path = 'sqlite:///' + self.db_info['portfolio_data_dbpath']
                portfolio_data_engine = create_engine(engine_path)
                return portfolio_data_engine
            except Exception as e:
                self.logger.error("Error ocurred while initializing the portfolio data engine:", e)
                raise
        else:
            return None
    
    def create_file_list(self) -> list[str]:
        files_list = []
        table_base_path = 'core\DataStorage\TableCreationSQL'
        if self.market_data_flag:
            
        return
    def initalize_mkt_data_db(self, mkt_data_engine:Engine):
        pass
    def initialize_mkt_data_core_ohlcv(self, mkt_data_engine:Engine):
        file_path = 'core\DataStorage\TableCreationSQL\core_market_data_ohlcv.sql'
        with mkt_data_engine.connect() as conn:
            transact = conn.begin()
            try:
                with open(file_path, 'r') as f:
                    script = f.read()
                    conn.execute(text(script))
                transact.commit()

            except Exception as e:
                transact.rollback()
                raise
    
    def db_init_main():
        pass
