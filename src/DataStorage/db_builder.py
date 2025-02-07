""" This module manages the bulding of the SAFT databases """
from src.Utils.helpers import DataMgmtHelpers as dmh
from src.DataStorage.Utils.config_parser import DBConfigParser
from src.DataStorage.Utils.table_creation import DataTableCreation
class DBBuilder:
    """
    _summary_
    """
    def __init__(self, config_path:str='config/my_config.yml'):
        self.logger = dmh.setup_log_to_console()
        self.logger.info("Beginning database build process...")
        parser = DBConfigParser(config_path=config_path)
        self.config_info = parser.get_config_info()
        self.logger.info("successfully read in config file...")

    def initialize_new_db(self):
        """
        _summary_
        """
        self.logger.info("Building new database...")
        dtc = DataTableCreation(config_info=self.config_info)
        dtc.create_tables()
        self.logger.info("Finished setting up database!")
