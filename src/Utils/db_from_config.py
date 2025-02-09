"""This module contains all of the functionality to create a new database from a ConfigInfo class"""
from typing import List
import os
from sqlalchemy import text
from src.Utils import helpers
from src.DataStorage.Utils.configurator import ConfigInfo

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
    def __init__(self, config_info:ConfigInfo):
        self.logger = helpers.setup_log_to_console()
        # Get config info
        self.config_info = config_info.clean_config()
        # Base path for SQL scripts
        self.sql_base_path = 'src/DataStorage/SQLTables'
        self.underlying_flag = False
        self.equities_flag = False
        # Set flags for tables shared between multiple security types
        if (
            'STK' in self.config_info.security_types or
            'ETF' in self.config_info.security_types or
            'FUND' in self.config_info.security_types
            ):
            self.equities_flag = True
        if (
            'STK' in self.config_info.security_types or
            'FUT' in self.config_info.security_types
            ):
            self.underlying_flag = True

    def initialize_tables(self, folder_name, file_name_list:List[str]):
        """
        A general method for initializing tables from SQL scripts
        
        Args: file_name_list (List[str]): a list of sql file names to generate the tables
        """
        db_engine = helpers.ORMHelpers(self.config_info.db_path, self.config_info.db_dialect).initalize_db_engine()
        with db_engine.connect() as conn:
            transact = conn.begin()
            for file in file_name_list:
                try:
                    full_path = os.path.join(self.sql_base_path, folder_name, file)
                    with open(full_path, 'r', encoding='utf-8') as f:
                        sql_script = f.read()
                        conn.execute(text(sql_script))
                except Exception:
                    transact.rollback()
                    self.logger.error('Error creating the metadata tables for the historical prices', exc_info=True)
                    raise
            transact.commit()

    def create_historical_prices_list(self) -> List[str]:
        """This aggregates a list of tables from the 'HistoricalPrice' folder to include"""
        historical_prices_list = []
        if self.config_info.ohlcv_flag:
            if self.config_info.to_int_flag:
                historical_prices_list.append('price_history_ohlcv_toint.sql')
            if not self.config_info.to_int_flag:
                historical_prices_list.append('price_history_ohlcv_floats.sql')
        return historical_prices_list

    def create_securities_metadata_list(self) -> List[str]:
        """This creates a list of securities metadata tables to include"""
        securities_metadata_list = []
        if self.equities_flag:
            equities_list = ["dividend_history.sql", "fundamentals_snapshots.sql"]
            securities_metadata_list.extend(equities_list)
        if self.underlying_flag:
            securities_metadata_list.append("underly_assets_table.sql")
        if "STK" in self.config_info.security_types:
            stk_list = ["stock_splits.sql", "stk_table.sql", "earnings_history.sql"]
            securities_metadata_list.extend(stk_list)
        if "FOREX" in self.config_info.security_types:
            securities_metadata_list.append("cash_table.sql")
        if "FUTURES" in self.config_info.security_types:
            securities_metadata_list.append("fut_table.sql")
        if "ETFs" in self.config_info.security_types:
            etfs_list = ["etf_table.sql", "issuers_table.sql"]
            securities_metadata_list.extend(etfs_list)

        return securities_metadata_list

    def initialize_core(self):
        """This method initializes the core tables in the database """
        core_files = os.listdir(f"{self.sql_base_path}/Core")
        self.initialize_tables(folder_name='Core', file_name_list=core_files)

    def initialize_portfolio_analysis(self):
        """Initializes the portfolio analysis tables"""
        portfolio_files = self.create_historical_prices_list()
        self.initialize_tables(folder_name='HistoricalPrices', file_name_list=portfolio_files)

    def initialize_securities_metadata(self):
        """Initializes the securities metadata"""
        securities_metadata = self.create_securities_metadata_list()
        self.initialize_tables(folder_name='SecuritiesMetaData', file_name_list=securities_metadata)

    def initialize_db(self):
        """The main function that initializes the database"""
        self.initialize_core()
        self.initialize_securities_metadata()
        self.initialize_portfolio_analysis()
