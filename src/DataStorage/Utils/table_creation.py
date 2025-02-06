from sqlalchemy import create_engine, Engine, text
import os
from src.DataStorage.Utils.helpers import DataStorageHelpers as dsh
from src.Utils.helpers import DataMgmtHelpers as dmh
from src.DataStorage.Utils.config_parser import DBConfigParser


class DataTableCreation:
    """
    This class manages all steps of creating the tables for the database depending on the users config file

    Args:
    - feature_info (opt[dict]): An optional input parameter if the user wants to record the values of the features being input into their model

    Attributes:
    """
    def __init__(self):
        self.logger = dmh.setup_log_to_console()
        # Get config info
        self.config_info = DBConfigParser()
        # Base path for SQL scripts
        self.sql_base_path = 'src/DataStorage/SQLTables'
        # Set flags for tables shared between multiple security types
        if ('STK' in self.config_info.security_types or 'ETF' in self.config_info.security_types or 'FUND' in self.config_info.security_types):
            self.equities_flag = True
        if ('STK' in self.config_info.security_types or 'FUT' in self.config_info.security_types):
            self.underlying_flag = True
 
    def get_price_history_table(self) -> str:
        """
        This creates a list of the core price history table files to include

        Returns:
        - price_history_path (str): a string of the file path to the chosen price history table schema
        """
        if self.config_info.to_int_flag:
            price_history_path = os.path.join(self.sql_base_path, 'HistoricalPrice/price_history_ohlcv_toint.sql')
        else:
            price_history_path = os.path.join(self.sql_base_path, 'HistoricalPrice/price_history_ohlcv_float.sql')
        return price_history_path

    def create_securities_metadata_list(self) -> list[str]:
        """
        This creates a list of file paths to the metadata table scripts to include in database setup

        Returns:
        - metadata_list (list): a list of the file paths to the metadata tables to include in the database
        """
        metadata_list = []
        for sec_type in self.config_info.security_types:
            script_prefix = f'SecuritiesMetadata/{sec_type.lower()}'
            metadata_path = dsh.create_script_path(self.sql_base_path, script_prefix=script_prefix, script_suffix='tables')
            metadata_list.append(metadata_path)
        if self.equities_flag:
            metadata_path = dsh.create_script_path(self.sql_base_path, 'SecuritiesMetadata/equities', script_suffix='tables')
            metadata_list.append(metadata_path)
        if self.underlying_flag:
            metadata_path = dsh.create_script_path(self.sql_base_path, 'SecuritiesMetadata/underlying_assets', script_suffix='tables')
            metadata_list.append(metadata_path)
        return metadata_list
    
    def initalize_db_engine(self) -> Engine:
        """
        This creates an SQLAlchemy engine to manage the database transactions/connection

        Returns:
        - mkt_data_engine (Engine): A SQLAlchemy engine for the specified database instane 
        """
        if self.config_info.market_data_flag:
            try:
                if self.config_info.db_dialect in ("sqlite3", "sqlite") and not self.config_info.db_path.startswith('sqlite:///'):
                    engine_path = 'sqlite:///' + self.config_info.db_path
                mkt_data_engine = create_engine(engine_path)
                return mkt_data_engine
            except Exception as e:
                self.logger.error("Error ocurred while initializing the market data engine:", exc_info=True)
                raise
        else:
            return None
    
    def create_core_tables(self, mkt_data_engine:Engine) -> None:
        """
        Creates the core tables for any SAFT style database

        Args:
        - mkt_data_engine (Engine): A SQLAlchemy engine for the specified database instane, created in the initalize_mkt_data_engine method
        """
        core_tables = 'src/DataStorage/SQLTables/Core/core_tables.sql'
        with mkt_data_engine.connect() as conn:
            transact = conn.begin()
            try:
                with open(core_tables, 'r') as f:
                    script = f.read()
                    conn.execute(text(script))
                transact.commit()
            except Exception as e:
                transact.rollback()
                self.logger.error(f'Error creating the core tables', exc_info=True)
                raise
        self.logger.info("Successfully initialized core tables...")

    def create_price_history_table(self, mkt_data_engine:Engine) -> None:
        """
        Creates the price history table for market data database

        Args:
        - mkt_data_engine (Engine): A SQLAlchemy engine for the specified database instane, created in the initalize_mkt_data_engine method
        """
        price_history_table = self.get_price_history_table()
        with mkt_data_engine.connect() as conn:
            transact = conn.begin()
            try:
                with open(price_history_table, 'r') as f:
                    script = f.read()
                    conn.execute(text(script))
                transact.commit()
            except Exception as e:
                transact.rollback()
                self.logger.error(f'Error creating the core tables', exc_info=True)
                raise
        self.logger.info("Successfully initialized the chosen price history table...")
            
    
    def create_mkt_data_metadata(self, mkt_data_engine:Engine) -> None:
        """
        This creates the metadata tables for the security types specified by the user

        Args:
        - mkt_data_engine (Engine): A SQLAlchemy engine for the specified database instane, created in the initalize_mkt_data_engine method
        """
        metadata_list = self.create_securities_metadata_list()
        with mkt_data_engine.connect() as conn:
            transact = conn.begin()
            for metadata_file in metadata_list:
                try:
                    with open(metadata_file, 'r') as f:
                        script = f.read()
                        conn.execute(text(script))
                    transact.commit()
                except Exception as e:
                    transact.rollback()
                    self.logger.error(f'Error creating the metadata tables for the historical prices', exc_info=True)
                    raise
        self.logger.info("Successfully initialized metadata tables...")
        
    
    def create_portfolio_analysis_tables(self, mkt_data_engine:Engine) -> None:
        """
        Creates all necessary tables for the portfolio analysis schema

        Args:
        - mkt_data_engine (Engine): A SQLAlchemy engine for the specified database instane, created in the initalize_mkt_data_engine method
        """
        with mkt_data_engine.connect() as conn:
            transact = conn.begin()
            try:
                with open('core/DataStorage/TableCreationSQL/PortfolioAnalysis/portfolio_data_warehouse.sql', 'r') as f:
                    script = f.read()
                    conn.execute(text(script))
                transact.commit()
            except Exception as e:
                transact.rollback()
                self.logger.error(f'Error creating the portfolio analysis tables', exc_info=True)
                raise
        self.logger.info("Successfully initialized portfolio analysis tables...")
        

    def create_tables(self) -> None:
        """
        This is the main function for creating the tables desired
        """
        mkt_data_engine = self.initalize_db_engine()
        self.create_core_tables(mkt_data_engine)
        if self.config_info.market_data_flag:
            self.create_price_history_table(mkt_data_engine)
            self.create_mkt_data_metadata(mkt_data_engine)
        if self.config_info.portfolio_data_flag:
            self.create_portfolio_analysis_tables(mkt_data_engine)