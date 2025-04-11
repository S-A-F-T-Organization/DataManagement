"""Helper functions for getting observations from the SQL database"""

import logging
from typing import Type

from sqlalchemy import Engine, UniqueConstraint, inspect, select
from sqlalchemy.orm import DeclarativeBase, Session


def get_obs_uk(
    db_engine: Engine, cls: Type[DeclarativeBase], **kwargs
) -> DeclarativeBase:
    """
    Gets an observation from a table using unique key constraint(s)

    Args:
        db_engine (Engine): the database engine to use to connect to the database
        cls (Type[DeclarativeBase]): The class representing the table you want to select from
        **kwargs: Dictionary of column names and values that make up the unique constraint(s)
                 Example: symbol="AAPL", security_type_id=1

    Returns:
        Type[DeclarativeBase]: A fully set instance of the same type as the `cls` argument

    Raises:
        RuntimeError: If no record found matching the unique constraint
    """

    # Get provided column names from kwargs
    provided_columns = set(kwargs.keys())

    # Build where clause using all constraint columns
    where_conditions = [getattr(cls, col) == kwargs[col] for col in provided_columns]
    stmt = select(cls).where(*where_conditions)

    with Session(bind=db_engine) as session:
        session.begin()
        try:
            result = session.execute(stmt).first()
            if result:
                return result[0]

            raise RuntimeError(
                f"No record found in {cls.__tablename__} matching unique constraint "
                f"values: {kwargs}"
            )
        except RuntimeError:
            logging.error(
                "Could not find record in %s matching %s", cls.__tablename__, kwargs
            )
            raise
        except Exception:
            logging.error(
                "Unknown exception querying %s with constraints %s",
                cls.__tablename__,
                kwargs,
                exc_info=True,
            )
            raise


def check_obs_exists_uk(db_engine: Engine, cls: DeclarativeBase) -> bool:
    """
    Checks if an observation exists in the table using the unique keys

    Args:
        db_engine (Engine): the database engine to use to connect to the database
        cls (Type[DeclarativeBase]): An instance of the class representing the observation you want check

    Returns:
        exists_flag (bool): A flag indicating whether or not an observation exists
    """
    unique_keys = [
        col.name
        for constraint in cls.__table__.constraints
        if isinstance(constraint, UniqueConstraint)
        for col in constraint.columns
    ]

    # Build where conditions comparing instance values to table columns
    where_conditions = [
        getattr(cls.__class__, col_name) == getattr(cls, col_name)
        for col_name in unique_keys
    ]

    # Create select statement
    stmt = select(cls.__class__).where(*where_conditions)
    with Session(db_engine) as session:
        try:
            result = session.execute(stmt).first()
            if result:
                return True
            return False
        except Exception:
            logging.error(
                "Unknown exception querying %s with constraints %s",
                cls.__tablename__,
                unique_keys,
                exc_info=True,
            )
            raise


def get_obs_pk(
    db_engine: Engine, cls: Type[DeclarativeBase], pk: int
) -> DeclarativeBase:
    """
    Gets an observation from a table using the primary key

    Args:
        db_engine (Engine): the database engine to use to connect to the database
        cls (DeclarativeBase): An instance of the class representing the table you want to select from
        pk (int): the primary key value of the observation you want retrieve

    Returns:
        Type[DeclarativeBase]: a fully set instance of the same type as the `cls` agrument
    """
    inspector = inspect(cls)
    primary_key_names = [key.name for key in inspector.primary_key]
    primary_key_name = primary_key_names[0]
    stmt = select(cls).where(getattr(cls, primary_key_name) == pk)
    with Session(bind=db_engine) as session:
        session.begin()
        try:
            result = session.execute(stmt).first()
            if result:  # Check if result exists
                obs = result[0]
                return obs
            raise RuntimeError
        except RuntimeError:
            logging.error(
                "Could not find observation fo `%x` in the %a",
                pk,
                cls.__tablename__,
            )
            raise
        except Exception:
            logging.error(
                "Unknown exception trying to find `%x` in the %a table",
                pk,
                cls.__tablename__,
                exc_info=True,
            )
            raise
    return cls

def insert_new_instance(db_engine: Engine, cls: DeclarativeBase) -> str:
    """
    Inserts an observation of the given instance into the associated table

    Args:
        db_engine (Engine): the database engine to use to connect to the database
        cls (Type[DeclarativeBase]): An instance of the class representing the observation you want to insert

    Returns:
        str: Status message indicating if record was added or not
    """
    exists_flag = check_obs_exists_uk(db_engine=db_engine, cls=cls)
    if not exists_flag:
        with Session(db_engine) as session:
            try:
                # Add the instance directly to the session
                session.add(cls)
                session.commit()
                return "Added"
            except Exception:
                session.rollback()
                logging.error(
                    "Unknown exception inserting %s with unique constraints",
                    cls.__tablename__,
                    exc_info=True,
                )
                raise
    return "Not added"