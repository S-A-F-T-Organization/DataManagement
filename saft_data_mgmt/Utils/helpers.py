"""This contains all useful helper functions for code the SAFT data management package"""
import pkg_resources
import os
import logging
from sqlalchemy import Engine, create_engine, text

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


def initalize_db_engine(db_dialect:str, db_path:str, db_name) -> Engine:
    """
    This creates an SQLAlchemy engine to manage the database transactions/connection

    Returns:
    - db_engine (Engine): A SQLAlchemy engine for the specified database instane 
    """
    logger = setup_log_to_console()
    try:
        if db_dialect in ("sqlite3", "sqlite") and not db_path.startswith('sqlite:///'):
            engine_path = 'sqlite:///' + db_path + '/' + db_name
        elif db_dialect in ("sqlite3", "sqlite") and db_path.startswith('sqlite:///'):
            engine_path = db_path
        else:
            raise ValueError("Invalid database dialect detected: " + db_dialect)
        db_engine = create_engine(engine_path)
        return db_engine
    except Exception:
        logger.error("Error ocurred while initializing the market data engine:", exc_info=True)
        raise

def create_table(db_engine:Engine, full_path:str) -> None:
    """
    This method creates a table in the database using the provided SQL script

    Args:
    - db_engine (Engine): The SQLAlchemy engine for the database
    - full_path (str): The full path to the SQL script
    """
    logger = setup_log_to_console()
    with db_engine.connect() as conn:
        transact = conn.begin()
        try:
            # Extract the relative path starting from SQLTables
            path_parts = full_path.split(os.sep)
            sql_index = path_parts.index('SQLTables')
            relative_path = os.path.join(*path_parts[sql_index:])
            
            sql_path = pkg_resources.resource_filename('saft_data_mgmt', relative_path)
            
            with open(sql_path, 'r', encoding='utf-8') as f:
                sql_script = f.read()
                conn.execute(text(sql_script))
        except Exception:
            transact.rollback()
            logger.error('Error creating tables', exc_info=True)
            raise
        transact.commit()

import pkg_resources
import os

test_path = "saft_data_mgmt/SQLTables/Core/security_types.sql"
resolved_path = pkg_resources.resource_filename('saft_data_mgmt', test_path)
print(f"Resolved path: {resolved_path}")
print(f"File exists: {os.path.exists(resolved_path)}")