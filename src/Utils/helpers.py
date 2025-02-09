"""This contains all useful helper functions for code the SAFT data management package"""

import logging
import os
from sqlalchemy import Engine, create_engine

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


def setup_log_to_console() -> logging.Logger:
    """Simple function to setup a logger to output important messages to the user"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger

class ORMHelpers:
    """ This class will hold all of the common ORM functions """
    def __init__(self, db_path:str, db_dialect:str):
        self.logger = setup_log_to_console()
        self.db_path = db_path
        self.db_dialect = db_dialect

    def initalize_db_engine(self) -> Engine:
        """
        This creates an SQLAlchemy engine to manage the database transactions/connection

        Returns:
        - db_engine (Engine): A SQLAlchemy engine for the specified database instane 
        """
        try:
            if self.db_dialect in ("sqlite3", "sqlite") and not self.db_path.startswith('sqlite:///'):
                engine_path = 'sqlite:///' + self.db_path
            elif self.db_dialect in ("sqlite3", "sqlite") and self.db_path.startswith('sqlite:///'):
                engine_path = self.db_path
            else:
                raise ValueError("Invalid database dialect detected")
            db_engine = create_engine(engine_path)
            return db_engine
        except Exception:
            self.logger.error("Error ocurred while initializing the market data engine:", exc_info=True)
            raise
    