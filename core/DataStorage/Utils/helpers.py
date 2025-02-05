import logging
import os

class DataStorageHelpers:

    def __init__(self):
        pass
    
    @staticmethod
    def setup_log_to_console() -> logging.Logger:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        return logger
    
    @staticmethod
    def create_script_path(base_path:str, script_prefix:str, script_suffix:str) -> str:
        """
        This is a static method to help reduce repeated code when creating the metadata list

        Args:
        - base_path (str): the base path to the sql scripts directory
        - script_prefix (str): the prefix for the sql script
        """
        script_name = f"{script_prefix}_{script_suffix}.sql"
        script_path = os.path.join(base_path, script_name)
        return script_path