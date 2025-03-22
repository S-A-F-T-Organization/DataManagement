"""
This module defines the workflow for adding a new symbol to a SAFT database given
the symbol and security type you would like to add
"""

import logging
from decimal import Decimal

import pandas as pd
from ib_insync import IB, BarDataList, Contract, ContractDetails, Forex
from sqlalchemy import Engine, select, text
from sqlalchemy.orm import Session

from saft_data_mgmt.models import (
    AllCoreInfo,
    SecuritiesInfo,
    SecurityExchanges,
    SecurityTypes,
)
from saft_data_mgmt.Utils.helpers import prep_data, setup_dev_engine, setup_prod_engine


class AddCoreInfoWorkflow:
    """
    This represents the workflow for adding a new symbol to the database given the
    symbol and security type. The workflow is as follows:

    1. Initialize: takes in the symbol, security type, whether or not it is in a
    development environment, and the IBKR connection/interface object,
    2. Runs checks on the symbol and security type to ensure it is in the correct format
    3. Initializes the database engine according to the specified environment (dev or prod)
    4. Creates a qualified contract with all of the necessary information
    5. Creates an AllCoreInfo object to store all of the necessary values
    6. Sets the symbol, security type, exchange, and exchange timezone values
    7. Parses and sets the trading hours
    8. Retrieves the exchange ID from the database and sets the exchange_id value
        i. If it already exists in the database, it returns the exchange ID
        ii. If it does not exist in the database, it inserts the exchange info into the database to create
        the exchange ID, then retrieves the newly created ID
    9. Retrieves the security type ID from the database and sets the security_type_id value
        i. If it already exists in the database, it returns the security type ID
        ii. If it does not exist in the database, it inserts the security type into the database to create
        the security type ID, then retrieves the newly created ID
    10. Calculates and sets the to_int value
    11. Maps the values onto an instance of the SecuritiesInfo class
    12. Inserts the values into the database
    """

    def __init__(self, security_type: str, symbol: str, dev_flag: bool, ib: IB):
        self.symbol = symbol.upper()
        self.ib = ib
        self.security_type_lower = security_type.lower()
        self.dev_flag = dev_flag

    @property
    def security_type(self):
        """Sets the security type attribute after normalizing and cleaning the input"""
        try:
            if self.security_type_lower in [
                "stk",
                "stock",
                "stocks",
                "stks",
                "etf",
                "etfs",
            ]:
                return "STK"
            if self.security_type_lower in ["fx", "forex", "cash"]:
                return "CASH"
            if self.security_type_lower in ["fut", "future", "futures"]:
                return "FUT"
            if self.security_type_lower in [
                "fund",
                "mutual fund",
                "mutual_fund",
            ]:
                return "FUND"
            raise ValueError("Invalid Security Type Received")
        except Exception as e:
            print(e)
            raise

    @property
    def db_engine(self) -> Engine:
        """Initializes the correct engine based on dev or prod flag"""
        if self.dev_flag:
            engine = setup_dev_engine()
            return engine
        engine = setup_prod_engine()
        return engine

    def get_qualified_contract(self) -> Contract:
        """Takes in the contract information and returns a qualified contract"""
        new_contract = Contract()
        new_contract.symbol = self.symbol
        new_contract.secType = self.security_type
        if self.security_type != "CASH":
            new_contract.currency = "USD"
        if self.security_type == "CASH":
            new_contract = Forex(pair=self.symbol)
        try:
            contract_list = self.ib.reqContractDetails(contract=new_contract)
            qualified_contract = self.ib.qualifyContracts(contract_list[0].contract)
            if not qualified_contract:
                raise ValueError(f"Could not qualify contract for {self.symbol}")
            qual_contract = qualified_contract[0]
            return qual_contract
        except Exception as e:
            logging.error("Error qualifying contract: %s", e)
            raise

    def insert_exchange_info(self, core_info: AllCoreInfo):
        """
        Inserts exchange information into the SecurityExchanges table.

        Parameters:
            core_info (AllCoreInfo): An object containing exchange details, including:
                - exchange_name: The name of the exchange.
                - exchange_tz: The local timezone of the exchange.

        Raises:
            Exception: Raises any exception that occurs during the insert and rolls back the transaction
        """
        exchange_name = core_info.exchange_name
        exchange_tz = core_info.exchange_tz

        with self.db_engine.connect() as conn:
            transaction = conn.begin()
            try:
                query = text(
                    """
                    INSERT INTO SecurityExchanges 
                    (exchange_name, local_timezone)
                    VALUES (:exchange_name, :exchange_tz)
                    """
                )
                conn.execute(
                    query,
                    {"exchange_name": exchange_name, "exchange_tz": exchange_tz},
                )
                transaction.commit()
            except Exception:
                transaction.rollback()
                raise

    def get_exchange_id(self, core_info: AllCoreInfo) -> int:
        """
        Gets the exchange id of the specified exchange from the SecurityExchanges table.

        If the exchange is not already in the database, then it will attempt toinsert the exchange details and
        select from it again. If this fails it will raise an error

        Parameters:
            core_info (AllCoreInfo): An object containing exchange details, including:
                - exchange_name (str): The name of the exchange.
                - exchange_tz (str): The local timezone of the exchange.
                - rth_start_time_utc (str): The regular trading hours start time (in UTC).
                - rth_end_time_utc (str): The regular trading hours end time (in UTC).

        Returns:
            exchange_id (int): the exchange id of the given exchange

        Raises:
            Exception: Raises any exception that occurs during the insert and rolls back the transaction
        """

        stmt = select(SecurityExchanges).where(SecurityExchanges.exchange_name == core_info.exchange_name)
        with Session(self.db_engine) as session:
            session.begin()
            try:
                result = session.execute(stmt).first()

                if result:  # Check if result exists
                    exchange_id = result[0].exchange_id
                    return exchange_id

                # If no result, insert and try again
                self.insert_exchange_info(core_info=core_info)
                result = session.execute(stmt).first()
                if result:
                    exchange_id = result[0].exchange_id
                    return exchange_id

                raise RuntimeError("Could not insert or retrieve exchange info")
            except Exception as e:
                logging.error("Error inserting exchange info: %s", e)
                raise

    def insert_security_type(self, core_info: AllCoreInfo) -> None:
        """
        Inserts new security type information into the SecurityTypes table

        Params:
            core_info (AllCoreInfo):
                - security_type (str): the name of the security type
        Returns:
            None
        """
        security_type = core_info.security_type
        with self.db_engine.connect() as conn:
            transaction = conn.begin()
            try:
                query = text(
                    """
                    INSERT INTO SecurityTypes
                    (security_type)
                    VALUES (:security_type)
                    """
                )
                conn.execute(query, {"security_type": security_type})
                transaction.commit()
            except Exception as e:
                transaction.rollback()
                logging.error("Error inserting security type: %s", e)
                raise

    def get_sec_type_id(self, core_info: AllCoreInfo) -> int:
        """
        Retrieves the security type info from the SecurityTypes table.

        If no record exists for the specified security_type, this function calls `insert_security_type` to
        add a new record, and then retrieves the inserted record.

        Parameters:
            core_info (AllCoreInfo): An object containing exchange details. It must include:
                - security_type (str): The name of the security type

        Returns:
            sec_type_id (int): The information for the given exchange from the SecurityExchanges table

        Raises:
            Exception: Propagates any database-related exception encountered during the process.
        """
        stmt = select(SecurityTypes).where(
            SecurityTypes.security_type == core_info.security_type
        )
        with Session(self.db_engine) as session:
            try:
                with session.begin():
                    result: list[SecurityTypes] = session.execute(stmt).first()
                    if result:
                        return result[0].security_type_id

                    self.insert_security_type(core_info=core_info)
                    result = session.execute(stmt).first()
                    if result:
                        return result[0].security_type_id

                    raise RuntimeError(
                        "Could not insert or retrieve security type info"
                    )
            except Exception as e:
                logging.error("Error getting security type ID: %s", e)
                raise

    def get_price_data(self, qualified_contract: Contract) -> BarDataList:
        """
        Gets the price data for the last 5 days to find the to_int value

        Args:
        - qualified_contract (Contract): The qualified contract of the security you are adding

        Returns:
        - price_data (DataFrame): A DataFrame of the price data
        """
        bars = self.ib.reqHistoricalData(
            qualified_contract,
            endDateTime="",
            durationStr="5 D",
            barSizeSetting="2 mins",
            whatToShow="TRADES",
            useRTH=False,
        )
        price_data = prep_data(ticker=qualified_contract.symbol, candles=bars)
        return price_data

    def to_int_value_from_price(self, price_data: pd.DataFrame) -> int:
        """
        Determine how many factors of 10 are needed to convert security prices to integer form.
        Scans the 'Open', 'High', 'Low', and 'Close' columns for decimal precision and returns
        the maximum number of decimal places found.

        Args:
            price_data (BarDataList): an ibkr object of the price data

        Returns:
            int: The maximum decimal precision across the four price columns.
        """
        price_columns = ["Open", "High", "Low", "Close"]
        decimal_places_df = price_data[price_columns].map(
            lambda x: max(-Decimal(str(x)).as_tuple().exponent, 0)
        )
        to_int = decimal_places_df.max().max()
        return to_int

    def to_int_from_details(self, details: ContractDetails) -> int:
        """
        Uses the min_tick attribute in the contract details to calculate the to_int value. If there
        are no decimals in the min tick attribute, it returns 1

        Args:
            detail (ContractDetails): _description_
        Returns:
            to_int (int): The powers of base 10 to multiply the price by to get it into an integer
        """
        if details.minTick >= 1.0:
            return 0
        min_tick = str(details.minTick)
        if "." in min_tick:
            decimal_places = min_tick.split(".")[-1]
            to_int = len(decimal_places)
            return to_int
        return 1

    def set_details(self, qualified_contract: Contract) -> AllCoreInfo:
        """Sets all of the core symbol info"""
        core_info = AllCoreInfo()
        details_list = self.ib.reqContractDetails(qualified_contract)
        if details_list:
            details = details_list[0]
            core_info.symbol = self.symbol
            if self.security_type == "CASH":
                core_info.symbol = details.marketName
            core_info.exchange_name = qualified_contract.primaryExchange
            if (
                len(qualified_contract.primaryExchange) == 0
            ):  # If there is no primary exchange listed, .exchange
                core_info.exchange_name = qualified_contract.exchange
            core_info.security_type = self.security_type
            if self.security_type_lower == "etf":
                core_info.security_type = "ETF"
            core_info.exchange_tz = details.timeZoneId
            core_info.exchange_id = self.get_exchange_id(core_info=core_info)
            core_info.sec_type_id = self.get_sec_type_id(core_info=core_info)
            core_info.to_int = self.to_int_from_details(details=details)
            return core_info

    def insert_symbol_info(self, core_info: AllCoreInfo) -> None:
        """Maps the core_info class onto a SecuritiesInfo class and inserts it into the database."""
        sec_info = SecuritiesInfo(
            symbol=core_info.symbol,
            exchange_id=core_info.exchange_id,
            security_type_id=core_info.sec_type_id,
            to_int=core_info.to_int,
        )

        with Session(self.db_engine) as session:
            transaction = session.begin()
            try:
                # Check if symbol already exists
                existing = (
                    session.query(SecuritiesInfo)
                    .filter_by(
                        symbol=core_info.symbol, security_type_id=core_info.sec_type_id
                    )
                    .first()
                )
                if existing:
                    logging.info(
                        "Symbol %s already exists in database, skipping insert",
                        core_info.symbol,
                    )
                    return

                session.add(sec_info)
                session.commit()
                return
            except Exception as e:
                transaction.rollback()
                raise e

    def main(self) -> None:
        """
        Performs the workflow as defined by the class docstrings
        1. creates the qualified contract
        2. sets the core_info values
        3. inserts the values into the database
        """
        qualified_contract = self.get_qualified_contract()
        concrete_info = self.set_details(qualified_contract=qualified_contract)
        self.insert_symbol_info(core_info=concrete_info)
