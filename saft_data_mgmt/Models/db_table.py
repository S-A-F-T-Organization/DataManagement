"""
Module: saft_db
Description: Provides the classes and methods for an abstracted version of a SQL database
table, along with methods for common functionalities
"""

from typing import List, Optional
from dataclasses import dataclass
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Engine
from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


Base = declarative_base()
class SaftTable:
    """
    Mixin for SQLAlchemy declarative models representing database tables.
    
    Provides common CRUD operations and utility methods.
    """

    @classmethod
    def from_db(cls, engine:Engine, table_name: str):
        """
        Reflect an existing SQL table in a database and create a mapped class dynamically.
        
        Args:
            engine: SQLAlchemy engine instance.
            table_name (str): The name of the table to reflect.
        
        Returns:
            A new SQLAlchemy model class mapped to the existing table.
        
        Raises:
            ValueError: If the table is not found in the database.
        """
        metadata = MetaData()
        metadata.reflect(bind=engine, only=[table_name])
        table = metadata.tables.get(table_name)
        if table is None:
            raise ValueError(f"Table {table_name} does not exist in the database.")

        attrs = {'__table__': table}
        return type(table_name.capitalize(), (Base, SaftTable), attrs)

    @classmethod
    def from_sql_script(cls, engine:Engine, sql_script: str, table_name: str):
        """
        Create a new SQLAlchemy model class from a SQL script.
        
        This method executes the provided SQL script to create the table in the database,
        reflects the created table from the engine's metadata, and dynamically creates a 
        new model class that maps to the table.
        
        Args:
            engine: SQLAlchemy engine instance.
            sql_script (str): The SQL script containing the CREATE TABLE statement.
            table_name (str): The name of the table that is created by the script.
        
        Returns:
            A new SQLAlchemy model class representing the created table.
        
        Raises:
            ValueError: If the table cannot be found after executing the SQL script.
        """
        # Execute the SQL script to create the table.
        with engine.begin() as connection:
            connection.execute(sql_script)

        # Reflect the newly created table.
        metadata = MetaData()
        metadata.reflect(bind=engine, only=[table_name])
        table = metadata.tables.get(table_name)
        if table is None:
            raise ValueError(f"Table '{table_name}' was not created successfully by the provided script.")

        # Dynamically create a new model class using the reflected table.
        model_name = table_name.capitalize()
        return type(model_name, (Base, cls), {'__table__': table})

    def to_sql_script(self, engine) -> str:
        """
        Generate the SQL 'CREATE TABLE' statement for this table.
        
        Args:
            engine: SQLAlchemy engine instance.
            
        Returns:
            str: The SQL DDL statement for the table.
        """
        return str(CreateTable(self.__table__).compile(engine))

    @classmethod
    def insert_records(cls, session: Session, records: list[dict]) -> None:
        """
        Insert records into the table.
        
        Args:
            session (Session): SQLAlchemy session.
            records (list[dict]): A list of dictionaries representing records to insert.
        
        Raises:
            SQLAlchemyError: If the insert operation fails.
        """
        try:
            objects = [cls(**record) for record in records]
            session.add_all(objects)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e

    @classmethod
    def update_records(cls, session: Session, criteria: dict, updates: dict) -> None:
        """
        Update records in the table matching the given criteria.
        
        Args:
            session (Session): SQLAlchemy session.
            criteria (dict): Dictionary of conditions to filter records (e.g., {"id": 1}).
            updates (dict): Dictionary of field updates to apply.
        
        Raises:
            SQLAlchemyError: If the update operation fails.
        """
        try:
            session.query(cls).filter_by(**criteria).update(updates)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e

    @classmethod
    def upsert_records(cls, session: Session, records: list[dict]) -> None:
        """
        Upsert (update or insert) records into the table.
        
        For simplicity, this example assumes that the table has a primary key named 'id'.
        In a production scenario, you may want to generalize this or integrate with a
        more sophisticated upsert mechanism.
        
        Args:
            session (Session): SQLAlchemy session.
            records (list[dict]): A list of records for upsert operations.
        
        Raises:
            SQLAlchemyError: If the upsert operation fails.
        """
        try:
            for record in records:
                # Assume primary key is 'id'
                pk_value = record.get('id')
                if pk_value is None:
                    raise ValueError("Record must contain an 'id' key for upsert operations.")
                instance = session.query(cls).filter_by(id=pk_value).first()
                if instance:
                    for key, value in record.items():
                        setattr(instance, key, value)
                else:
                    instance = cls(**record)
                    session.add(instance)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e

    @classmethod
    def delete_records(cls, session: Session, criteria: dict) -> None:
        """
        Delete records from the table based on specified criteria.
        
        Args:
            session (Session): SQLAlchemy session.
            criteria (dict): Conditions to identify records to delete.
        
        Raises:
            SQLAlchemyError: If the deletion fails.
        """
        try:
            session.query(cls).filter_by(**criteria).delete()
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e

    @classmethod
    def retrieve_records(cls, session: Session, criteria: dict = None) -> list:
        """
        Retrieve records from the table, optionally filtered by criteria.
        
        Args:
            session (Session): SQLAlchemy session.
            criteria (dict, optional): Filter conditions for selecting records.
        
        Returns:
            list: A list of model instances matching the query.
        """
        query = session.query(cls)
        if criteria:
            query = query.filter_by(**criteria)
        return query.all()

    @classmethod
    def modify_table(cls, session: Session, modifications: dict) -> None:
        """
        Modify the table's schema (e.g., rename the table, change column definitions).
        
        **Note:** In SQLAlchemy, schema modifications are typically handled via migration
        tools (e.g., Alembic) rather than dynamically at runtime.
        
        Args:
            session (Session): SQLAlchemy session.
            modifications (dict): A dictionary describing the desired schema modifications.
        
        Raises:
            NotImplementedError: Always, as runtime schema modification is not supported.
        """
        raise NotImplementedError("Schema modifications should be performed via migrations.")
    
@dataclass
class TableInfo:
    """A dataclass for the important table metadata"""
    table_name:str = None
    pk:str=None
    fks:Optional[List[str]] = None


