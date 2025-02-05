from core.DataStorage.Utils.helpers import DataStorageHelpers as dsh
from core.DataStorage.Utils.config_parser import DBConfigParser
from core.DataStorage.Utils.table_creation import DataTableCreation
class DBInitializer:

    def __init__(self, config_path:str='config/my_config.yml'):
        self.logger = dsh.setup_log_to_console()
        
