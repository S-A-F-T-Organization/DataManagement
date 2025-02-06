from sqlalchemy import create_engine, Engine, text
import os
from src.DataStorage.Utils.helpers import DataStorageHelpers as dsh
from src.DataStorage.Utils.config_parser import DBConfigParser


class DataTableCreation:
    """
    This class manages all steps of creating the tables for the database depending on the users config file

    Args:
    - feature_info (opt[dict]): An optional input parameter if the user wants to record the values of the features being input into their model

    Attributes:
    """
    def __init__(self):
        self.logger = dsh.setup_log_to_console()
        # Get config info
        self.config_info = DBConfigParser()
        # Base path for SQL scripts
        self.sql_base_path = 'core/DataStorage/TableCreationSQL'
        # Set flags for tables shared between multiple security types
        if ('STK' in self.config_info.security_types or 'ETF' in self.config_info.security_types or 'FUND' in self.config_info.security_types):
            self.equities_flag = True
        if ('STK' in self.config_info.security_types or 'FUT' in self.config_info.security_types):
            self.underlying_flag = True
 
    def create_core_list(self) -> list[str]:
        """
        This creates a list of the core table files to include

        Returns:
        - core_list (list): a list of the file paths to the core tables to include in the database
        """
        core_list = []
        if self.config_info.quotes_flag:
            quotes_core = os.path.join(self.sql_base_path, 'core_market_data_quotes.sql')
            core_list.append(quotes_core)
        if self.config_info.ohlcv_flag:
            quotes_core = os.path.join(self.sql_base_path, 'core_market_data_ohlcv.sql')
            core_list.append(quotes_core)
        return core_list

    def create_metadata_list(self) -> list[str]:
        """
        This creates a list of file paths to the metadata table scripts to include in database setup

        Returns:
        - metadata_list (list): a list of the file paths to the metadata tables to include in the database
        """
        metadata_list = []
        for sec_type in self.config_info.security_types:
            script_prefix = sec_type.lower()
            metadata_path = dsh.create_script_path(self.sql_base_path, script_prefix=script_prefix, script_suffix='tables')
            metadata_list.append(metadata_path)
        if self.equities_flag:
            metadata_path = dsh.create_script_path(self.sql_base_path, 'equities', script_suffix='tables')
            metadata_list.append(metadata_path)
        if self.underlying_flag:
            metadata_path = dsh.create_script_path(self.sql_base_path, 'underlying_assets', script_suffix='tables')
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
                self.logger.error("Error ocurred while initializing the market data engine:", e)
                raise
        else:
            return None
    
    def create_core_tables(self, mkt_data_engine:Engine) -> None:
        """
        Creates the core tables for any SAFT style database

        Args:
        - mkt_data_engine (Engine): A SQLAlchemy engine for the specified database instane, created in the initalize_mkt_data_engine method
        """
        core_list = self.create_core_list()
        with mkt_data_engine.connect() as conn:
            transact = conn.begin()
            for core_file in core_list:
                try:
                    with open(core_file, 'r') as f:
                        script = f.read()
                        conn.execute(text(script))
                    transact.commit()
                except Exception as e:
                    transact.rollback()
                    self.logger.error(f'Error creating the core tables', exc_info=True)
                    raise
        self.logger.info("Successfully initialized core tables...")
            
    
    def create_mkt_data_metadata(self, mkt_data_engine:Engine) -> None:
        """
        This creates the metadata tables for the security types specified by the user

        Args:
        - mkt_data_engine (Engine): A SQLAlchemy engine for the specified database instane, created in the initalize_mkt_data_engine method
        """
        metadata_list = self.create_metadata_list()
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
        ##TODO: Create tests for this method
        with mkt_data_engine.connect() as conn:
            transact = conn.begin()
            try:
                with open('core/DataStorage/TableCreationSQL/portfolio_data_warehouse.sql', 'r') as f:
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
            self.create_mkt_data_metadata(mkt_data_engine)
        if self.config_info.portfolio_data_flag:
            self.create_portfolio_analysis_tables(mkt_data_engine)