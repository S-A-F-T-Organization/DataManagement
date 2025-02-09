"""
Module: get_core_info.py

This module uses ib_insync to connect to Interactive Brokers,
qualify a contract based on a given symbol and security type,
retrieve the contract details (including trading hours),
and return a SecuritiesInfo dataclass instance containing
the gathered information.

The associated dataclasses and SQL table columns are:
    - SecuritiesInfo
    - SecurityTypes
    - SecurityExchanges:
"""
from typing import Tuple, Optional
import logging
from ib_insync import Contract
from src.DataObjects.core_objects import SecuritiesInfo
from src.BrokerageUtils.ibkr_utils import IBKRUtils as ibu

# Enable logging if needed
logging.basicConfig(level=logging.INFO)

class GetCoreInfo:
    """
    _summary_
    This module uses ib_insync to connect to Interactive Brokers,
    qualify a contract based on a given symbol and security type,
    retrieve the contract details (including trading hours),
    and return a SecuritiesInfo dataclass instance containing
    the gathered information.
    """

    def __init__(self, symbol:str, sec_type:str):
        self.sec_type = sec_type
        self.symbol = symbol
        self.ib = ibu.ibkr_spinup()
        logging.info("Connected to IB for symbol %x of type %r.", self.symbol, self.sec_type)


    def get_contract(self) -> Contract:
        """Given a symbol and security type, create an appropriate IB contract."""
        sec_type_upper = self.sec_type.upper()
        contract = Contract()
        contract.symbol = self.symbol
        contract.secType = sec_type_upper
        return contract


    def parse_trading_hours(self, trading_hours:str) -> Tuple[Optional[str], Optional[str]]:
        """
        Parse the tradingHours string returned by IB to extract the RTH start and end times.
        
        IB usually returns a string like:
        
            "20250206:0930-1600;20250207:0930-1600;..."
        
        This function takes the first segment and extracts the start and end times.
        
        Returns a tuple (rth_start_time_utc, rth_end_time_utc) as strings (or (None, None) if parsing fails).
        """
        if not trading_hours:
            return None, None

        segment = trading_hours.split(';')[0]
        try:
            # Expect a format like "YYYYMMDD:HHMM-HHMM"
            _, times = segment.split(':')
            start_time_str, end_time_str = times.split('-')
            return start_time_str, end_time_str
        except Exception:
            logging.error("Error parsing trading hours %x", trading_hours, exc_info=True)
            return None, None


    def get_security_info(self, contract) -> SecuritiesInfo:
        """
        Connect to IB, qualify a contract for the given symbol and security type,
        retrieve its contract details (including trading hours), and return a
        SecuritiesInfo dataclass with the gathered data.
        
        Note:
        - security_type_id and exchange_id are populated with the security type and exchange
            strings returned by IB. Mapping these to integer IDs (as in your SQL tables)
            is assumed to be handled elsewhere.
        - The "to_int" field is ignored.
        """
        qualified_contracts = self.ib.qualifyContracts(contract)
        # TODO: Change this to a warning and continue
        if not qualified_contracts:
            raise ValueError(f"Could not qualify contract for symbol {self.symbol} with type {self.sec_type}.")
        qualified_contract = qualified_contracts[0]
        logging.info("Qualified contract: %x", qualified_contract)

        # Request contract details (to get trading hours, etc.)
        details_list = self.ib.reqContractDetails(qualified_contract)
        if details_list:
            details = details_list[0]
            trading_hours = details.tradingHours
            rth_start, rth_end = self.parse_trading_hours(trading_hours)
            logging.info("Parsed trading hours: start=%x, end=%r", rth_start, rth_end)
        else:
            rth_start, rth_end = None, None
            logging.warning("No contract details found for %x of security type %r.", self.symbol, self.sec_type)

        # Build and return the SecuritiesInfo dataclass.
        # TODO: For now, security_type_id and exchange_id are stored as the raw values (strings).
        sec_info = SecuritiesInfo(
            symbol=self.symbol,
            security_type_id=self.sec_type,
            exchange_id=qualified_contract.exchange,
            rth_start_time_utc=rth_start,
            rth_end_time_utc=rth_end
        )
        return sec_info

    def get_exchange_timezone(self, contract) -> str:
        contract = Contract(self.symbol, self.sec_type)
        qualified_contracts = self.ib.qualifyContracts(contract)
        if not qualified_contracts:
            raise ValueError(f"Could not qualify contract for {self.symbol}")

        # Get the first qualified contract
        qualified_contract = qualified_contracts[0]

        # Request the contract details
        contract_details = self.ib.reqContractDetails(qualified_contract)
        if not contract_details:
            raise ValueError(f"No contract details found for {self.symbol}")

        # timeZoneId is the attribute that shows the exchange's timezone
        timezone = contract_details[0].timeZoneId
        return timezone

    def sec_info_main(self):
        contract = self.get_contract()
        sec_info = self.get_security_info(contract=contract)
        time_zone = self.get_exchange_timezone(contract=contract)
        return sec_info, time_zone
