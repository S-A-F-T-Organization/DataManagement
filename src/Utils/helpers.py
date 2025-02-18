"""This contains all useful helper functions for code the SAFT data management package"""

import logging
import os
from sqlalchemy import Engine, create_engine, text

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


def initalize_db_engine(db_dialect:str, db_path:str) -> Engine:
    """
    This creates an SQLAlchemy engine to manage the database transactions/connection

    Returns:
    - db_engine (Engine): A SQLAlchemy engine for the specified database instane 
    """
    logger = setup_log_to_console()
    try:
        if db_dialect in ("sqlite3", "sqlite") and not db_path.startswith('sqlite:///'):
            engine_path = 'sqlite:///' + db_path
        elif db_dialect in ("sqlite3", "sqlite") and db_path.startswith('sqlite:///'):
            engine_path = db_path
        else:
            raise ValueError("Invalid database dialect detected")
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
            with open(full_path, 'r', encoding='utf-8') as f:
                sql_script = f.read()
                conn.execute(text(sql_script))
        except Exception:
            transact.rollback()
            logger.error('Error creating the metadata tables for the historical prices', exc_info=True)
            raise
        transact.commit()
    