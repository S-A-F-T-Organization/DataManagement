from ib_insync import IB
from src.Utils.helpers import DataMgmtHelpers as dmh

class IBKRUtils:

    def __init__(self):
        self.logger = dmh.setup_log_to_console()

    def ibkr_spinup(self, host:str = '127.0.0.1', port:int=7487, client_id:int=1):
        try:
            ib = IB()
            ib.connect(host=host, port=port, clientId=client_id)
            return ib
        except Exception as e:
            self.logger.error("Encountered error while connecting to IBKR instance: ", exc_info=True)

    def parse_trading_hours(trading_hours_str, date_str=None):
        """
        Parse an IBKR trading hours string (e.g., '20250205:0930-1600;20250206:0930-1600').
        Returns a dictionary mapping each date (YYYYMMDD) to a tuple (start_time, end_time).
        If a specific date_str is provided, returns the tuple for that date.
        """
        sessions = {}
        if not trading_hours_str:
            return sessions
        sessions_list = trading_hours_str.split(';')
        for session in sessions_list:
            try:
                date_part, hours_part = session.split(':')
                start_time, end_time = hours_part.split('-')
                sessions[date_part] = (start_time, end_time)
            except Exception as e:
                # In case the format is unexpected, skip this session
                continue
        if date_str:
            return sessions.get(date_str)
        return sessions
    
    def get_contract_details(ib, symbol, security_type):
        """
        Given a symbol and security type, create a minimal contract and request
        contract details from IBKR.
        """
        # Create a contract based on security type.
        # (Here we only handle stocks; extend this for futures, options, etc.)
        if security_type.upper() == 'STK':
            # For stocks, we assume the default exchange ("SMART") and currency ("USD").
            contract = Stock(symbol, 'SMART', 'USD')
        elif security_type.upper() == 'FUT':
            # Example for futures – note that a proper future contract would require
            # additional information like the expiry month.
            contract = Future(symbol, '202502', 'GLOBEX')
        elif security_type.upper() == 'OPT':
            # Options require strike, expiry, and option right (call/put) information.
            raise ValueError("Insufficient information to create an option contract.")
        else:
            raise ValueError(f"Unsupported security type: {security_type}")
        
    def contract_creation(self, symbol:str, sec_type:str):
        ib = self.ibkr_spinup()
        contract_details = self.get_contract_details(ib, symbol, security_type)