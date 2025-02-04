from sqlalchemy import create_engine, Engine, text
import os
from core.DataStorage.Utils.helpers import DataStorageHelpers as dsh
from core.DataStorage.Utils.config_parser import DBConfigParser


class DBTableCreation():

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

    @staticmethod
    def create_metadata_path(base_path:str, script_prefix:str) -> str:
        """
        This is a static method to help reduce repeated code when creating the metadata list

        Args:
        - base_path (str): the base path to the sql scripts directory
        - script_prefix (str): the prefix for the sql script
        """
        script_name = f"{script_prefix}_tables.sql"
        script_path = os.path.join(base_path, script_name)
        return script_path
    
    def create_metadata_list(self) -> list[str]:
        """
        This creates a list of file paths to the metadata table scripts to include in database setup

        Returns:
        - metadata_list (list): a list of the file paths to the metadata tables to include in the database
        """
        metadata_list = []
        for sec_type in self.config_info.security_types:
            script_prefix = sec_type.lower()
            metadata_path = self.create_metadata_path(self.sql_base_path, script_prefix=script_prefix)
            metadata_list.append(metadata_path)
        if self.equities_flag:
            metadata_path = self.create_metadata_path(self.sql_base_path, 'equities')
            metadata_list.append(metadata_path)
        if self.underlying_flag:
            metadata_path = self.create_metadata_path(self.sql_base_path, 'underlying_assets')
            metadata_list.append(metadata_path)
        return metadata_list
    
    def initalize_mkt_data_engine(self) -> Engine:
        if self.config_info.market_data_flag:
            try:
                if self.config_info.db_dialect in ("sqlite3", "sqlite") and not self.config_info.mkt_data_db_path.startswith('sqlite:///'):
                    engine_path = 'sqlite:///' + self.config_info.mkt_data_db_path
                mkt_data_engine = create_engine(engine_path)
                return mkt_data_engine
            except Exception as e:
                self.logger.error("Error ocurred while initializing the market data engine:", e)
                raise
        else:
            return None
    
    def create_mkt_data_core(self, mkt_data_engine:Engine):
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
                    raise
    
    def create_mkt_data_metadata(self, mkt_data_engine:Engine):
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
                    raise