"""
Module: saft_db
Description: Provides the classes and methods for easy setup of a SAFT-style SQL database,
easy database manipulation, and easy integration of common workflows/ETLs
"""
from typing import List
from dataclasses import dataclass
from sqlalchemy import MetaData
from src.Utils.db_table import SaftTable
from src.Utils import helpers

@dataclass
class DBInfo:
    """A dataclass object for important metadata of your database"""
    db_file_path:str = None
    sql_dialect:str = None
    db_name:str = None
    db_tables:List[SaftTable] = None

class SaftDB:
    """A genereric class that represents the metadata of your database"""
    def __init__(self, db_file_path:str):
        self.db_info = DBInfo()
        self.db_info.db_file_path = db_file_path
    def drop_table(self):
        """Drops a table from the database"""
        return None
    def add_table(self):
        """Adds a table to the database"""
        return None
    def alter_table(self):
        """Alters a table in the database"""
        return None
    def migrate_db_location(self, new_location:str):
        """Migrates a database to a new location with the same SQL dialect"""
        new_info = self.db_info
        new_info.db_file_path = new_location
        return None
    def migrate_sql_dialects(self, new_location:str, new_dialect:str):
        """Migrates an existing database to a new location with a new SQL dialect"""
        new_info = self.db_info
        new_info.db_file_path = new_location
        new_info.sql_dialect = new_dialect
        return None

def db_from_sql(file_path: str) -> SaftDB:
    """
    Initializes a SaftDB instance from an existing SQL database.

    This function uses SQLAlchemy to:
      1. Reflect the database metadata to discover all tables.
      2. Build SaftTable objects for each table found.
      3. Populate and return a SaftDB instance with the gathered metadata.

    Args:
        file_path (str): The database connection string or file path.

    Returns:
        SaftDB: A new SaftDB instance populated with metadata from the existing database.
    """
    # Create a SQLAlchemy engine from the file path.
    engine = helpers.ORMHelpers.initalize_db_engine(file_path)

    # Reflect the existing database schema using SQLAlchemy's MetaData.
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Instantiate a new SaftDB and update its DBInfo.
    db_instance = SaftDB(db_file_path=file_path)
    db_instance.db_info.sql_dialect = engine.dialect.name

    # For many dialects (e.g. PostgreSQL), the database name is available in engine.url.database.
    db_instance.db_info.db_name = engine.url.database if engine.url.database else "Unknown"

    # Build a list of SaftTable objects from the reflected metadata.
    tables = []
    for _, table in metadata.tables.items():
        # saft_table = SaftTable.from_db(table)
        tables.append(saft_table)

    db_instance.db_info.db_tables = tables

    return db_instance
