from src.Utils.helpers import DataMgmtHelpers as dmh
from sqlalchemy import Engine
class MarketDataAggregation:

    """
    This class contains all of the methods for market data aggregation.

    Workflows:
    - Securities Info
        - Programmatic security discovery w/ symbol and security type
        - 

    """
    def __init__(self, engine:Engine):
        self.logger = dmh.setup_log_to_console()
        self.db_engine = engine
    
    def insert_records(self, table_name:str, ):
        pass

    def update_records(self):
        pass

    def upsert_records(self):
        pass


        
    