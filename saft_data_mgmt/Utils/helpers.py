"""This contains all useful helper functions for code the SAFT data management package"""

import logging
import os
from typing import Type

import pandas as pd
from dotenv import load_dotenv
from ib_insync import IB, BarDataList, Contract, Forex
from sqlalchemy import (
    Engine,
    MetaData,
    UniqueConstraint,
    create_engine,
    inspect,
    select,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Session

from saft_data_mgmt.models import AllCoreInfo, SecuritiesInfo


def setup_log_to_console() -> logging.Logger:
    """Simple function to setup a logger to output important messages to the user"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger


def initalize_db_engine(db_dialect: str, db_path: str, db_name) -> Engine:
    """
    This creates an SQLAlchemy engine to manage the database transactions/connection

    Returns:
    - db_engine (Engine): A SQLAlchemy engine for the specified database instane
    """
    logger = setup_log_to_console()
    try:
        if db_dialect in ("sqlite3", "sqlite") and not db_path.startswith("sqlite:///"):
            engine_path = "sqlite:///" + db_path + "/" + db_name
        elif db_dialect in ("sqlite3", "sqlite") and db_path.startswith("sqlite:///"):
            engine_path = db_path
        else:
            raise ValueError("Invalid database dialect detected: " + db_dialect)
        db_engine = create_engine(engine_path)
        return db_engine
    except Exception:
        logger.error(
            "Error ocurred while initializing the market data engine:", exc_info=True
        )
        raise


def create_table(db_engine: Engine, full_path: str) -> None:
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
            with open(full_path, "r", encoding="utf-8") as f:
                sql_script = f.read()
                conn.execute(text(sql_script))
        except Exception:
            transact.rollback()
            logger.error("Error creating tables", exc_info=True)
            raise
        transact.commit()


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

def setup_dev_engine() -> Engine:
    """Creates and returns an engine connected to the development database"""
    load_dotenv()
    dev_db_path = os.getenv("DEV_DB")
    dev_engine = create_engine(dev_db_path)
    return dev_engine


def setup_prod_engine() -> Engine:
    """Creates and returns an engine connected to the development database"""
    load_dotenv()
    prod_db_path = os.getenv("PROD_DB")
    prod_engine = create_engine(prod_db_path)
    return prod_engine


def truncate_dev_tables(dev_engine: Engine):
    """
    Truncates the development tables, useful for testing

    Args:
        dev_engine (Engine): the engine connected to the development database

    Raises:
        Exception: If an error occurs while truncating tables, it rollsback the transaction
        and raises the error
    """
    meta = MetaData()
    meta.reflect(bind=dev_engine)
    with dev_engine.connect() as conn:
        trans = conn.begin()
        try:
            for table in reversed(meta.sorted_tables):
                try:
                    conn.execute(text(f"DELETE FROM {table.name}"))
                except Exception as e:  # pylint: disable=broad-exception-caught
                    print(f"Skipping table {table.name} due to error: {e}")
            trans.commit()
        except Exception as e:
            trans.rollback()
            raise e

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


def get_qualified_contract(
    symbol: str, security_type: str, exchange: str, ib: IB
) -> Contract:
    """Takes in the contract information and returns a qualified contract"""
    new_contract = Contract()
    new_contract.symbol = symbol
    new_contract.secType = security_type
    new_contract.exchange = exchange
    if security_type == "CASH":
        if '.' in symbol:
            symbol=symbol.replace('.', '')
        new_contract = Forex(pair=symbol)
    contract_list = ib.reqContractDetails(contract=new_contract)
    qualified_contract = ib.qualifyContracts(contract_list[0].contract)
    if not qualified_contract:
        raise ValueError(f"Could not qualify contract for {symbol}")
    qual_contract = qualified_contract[0]
    return qual_contract


def contract_from_sql(
    symbol: str, security_type: str, db_engine: Engine, ib: IB
) -> Contract:
    """
    Generates a contract using a database connection

    Args:
        symbol (str): the symbol of the security you want to generate a contract for
        security_type (str): the security type
        db_engine (Engine): an engine object you want to use to connect to your data base
        ib (IB): an IB object from ib_insync to interact with the IBKR API
    """
    new_contract = Contract()
    symbol_info = AllCoreInfo().from_core_uks(
        symbol=symbol, sec_type=security_type, db_engine=db_engine
    )
    if security_type == "ETF":
        security_type = "STK"
    new_contract.symbol = symbol_info.symbol
    new_contract.secType = symbol_info.security_type
    new_contract.exchange = symbol_info.exchange_name
    if security_type == "CASH":
        new_contract = Forex(pair=symbol)
    contract_list = ib.reqContractDetails(contract=new_contract)
    qualified_contract = ib.qualifyContracts(contract_list[0].contract)
    if not qualified_contract:
        raise ValueError(f"Could not qualify contract for {symbol}")
    qual_contract = qualified_contract[0]
    return qual_contract

def contract_from_all_core_info(
    symbol_info:AllCoreInfo, ib: IB
) -> Contract:
    """
    Generates a contract using an AllCoreInfo instance

    Args:
        symbol_info (AllCoreInfo): instance containing necessary security info
        ib (IB): an IB object from ib_insync to interact with the IBKR API
    """
    new_contract = Contract()
    symbol = symbol_info.symbol
    security_type=symbol_info.security_type
    if security_type == "ETF":
        security_type = "STK"
    new_contract.symbol = symbol_info.symbol
    new_contract.secType = symbol_info.security_type
    new_contract.exchange = symbol_info.exchange_name
    if security_type == "CASH":
        new_contract = Forex(pair=symbol)
    contract_list = ib.reqContractDetails(contract=new_contract)
    qualified_contract = ib.qualifyContracts(contract_list[0].contract)
    if not qualified_contract:
        raise ValueError(f"Could not qualify contract for {symbol}")
    qual_contract = qualified_contract[0]
    return qual_contract

def prep_data(candles: BarDataList, ticker: str) -> pd.DataFrame:
    """
    This method prepares the data retrieved from IBKR, it takes in the bars list from
    ib_insync reqHistoricalData method and cleans it so that it is usable in the trade strategy.

    Args
    - candles (BarDataList): This is a BarDataList object from ib_insync,
    it contains the price data for the day on a 2 minute time interval

    Returns
    - price_data (DataFrame): A DataFrame with the last 120 minutes of OHLCV data in 2 minute intervals
    """
    data = {
        "Timestamp": [candle.date for candle in candles],
        "Open": [candle.open for candle in candles],
        "High": [candle.high for candle in candles],
        "Low": [candle.low for candle in candles],
        "Close": [candle.close for candle in candles],
        "Volume": [candle.volume for candle in candles],
    }

    price_data = pd.DataFrame(data)
    price_data["Timestamp"] = pd.to_datetime(price_data["Timestamp"])
    price_data["Ticker"] = ticker
    price_data["Time"] = price_data["Timestamp"].dt.time
    return price_data


def clean_ohlcv_data_int(candles: BarDataList, core_info: AllCoreInfo):
    """Cleans and inserts OHLCV data into the database"""
    data = {
        "timestamp_utc_ms": [candle.date for candle in candles],
        "open_price": [candle.open for candle in candles],
        "high_price": [candle.high for candle in candles],
        "low_price": [candle.low for candle in candles],
        "close_price": [candle.close for candle in candles],
        "volume": [candle.volume for candle in candles],
    }
    price_data = pd.DataFrame(data)
    # Convert Timestamp to time since epoch (ms)
    price_data["timestamp_utc_ms"] = pd.to_datetime(price_data["timestamp_utc_ms"])
    price_data["timestamp_utc_ms"] = (
        price_data["timestamp_utc_ms"].astype("int64") // 10**6
    )
    price_data["symbol_id"] = core_info.symbol_id

    # Convert Price to an integer
    price_cols = ["open_price", "high_price", "low_price", "close_price"]
    to_int_val = core_info.to_int
    price_data[price_cols] = (
        price_data[price_cols].apply(lambda x: x * (10**to_int_val)).astype(dtype=int)
    )
    price_data["volume"] = price_data["volume"].astype(dtype=int)
    price_data = price_data.iloc[:-2]
    return price_data


def retrieve_ohlcv_data(
    start_date: str, end_date: str, core_info: AllCoreInfo, db_engine: Engine
) -> pd.DataFrame:
    """
    Retrieves OHLCV data from the SQL database for the specified security between given dates.

    The start_date and end_date are provided in "MM/DD/YYYY HH:MM:SS" format in UTC and are
    converted into UTC timestamps in milliseconds.

    Args:
        start_date (str): The start date in "MM/DD/YYYY HH:MM:SS" UTC format.
        end_date (str): The end date in "MM/DD/YYYY HH:MM:SS" UTC format.
        core_info (AllCoreInfo): The AllCoreInfo instance holding security metadata.
        engine (Engine): The SQLAlchemy engine to connect to the database.

    Returns:
        pd.DataFrame: A DataFrame containing OHLCV data with columns:
            - ohlcv_id
            - symbol_id
            - timestamp_utc_ms
            - open_price
            - high_price
            - low_price
            - close_price
            - volume
    """
    # Convert string dates to pandas Timestamps with UTC timezone
    start_ts = pd.to_datetime(start_date, format="%m/%d/%Y %H:%M:%S", utc=True)
    end_ts = pd.to_datetime(end_date, format="%m/%d/%Y %H:%M:%S", utc=True)

    # Convert timestamps to milliseconds since epoch (UTC)
    start_ms = int(start_ts.value // 10**6)
    end_ms = int(end_ts.value // 10**6)

    # Build SQL query. Adjust the table name if needed (here it is "SecurityPrices").
    query = (
        f"SELECT * FROM SecurityPrices "
        f"WHERE symbol_id = {core_info.symbol_id} "
        f"AND timestamp_utc_ms BETWEEN {start_ms} AND {end_ms} "
        f"ORDER BY timestamp_utc_ms ASC"
    )

    # Query the database and return a DataFrame.
    df = pd.read_sql_query(query, db_engine)
    return df

def create_securities_list(db_engine) -> list[AllCoreInfo]:
    """Gets a list of the securities being tracked"""
    stmt = select(SecuritiesInfo)
    with Session(bind=db_engine) as session:
        securities = session.execute(stmt).scalars().all()
    core_info_list = []
    for i in securities:
        core_info = AllCoreInfo().from_sec_info(sec_info=i, db_engine=db_engine)
        core_info_list.append(core_info)
    return core_info_list
