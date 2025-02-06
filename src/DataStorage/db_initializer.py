from src.DataStorage.Utils.helpers import DataStorageHelpers as dsh
from src.DataStorage.Utils.config_parser import DBConfigParser
from src.DataStorage.Utils.table_creation import DataTableCreation
class DBInitializer:

    def __init__(self, config_path:str='config/my_config.yml'):
        self.logger = dsh.setup_log_to_console()
        self.logger.info("Beginning database initialization...")
        self.config_info = DBConfigParser()
        self.logger.info("successfully read in config file...")
    
    def initialize_new_db(self):
        dtc = DataTableCreation()
        dtc.create_tables()
        self.logger.info("Finished setting up database!")

