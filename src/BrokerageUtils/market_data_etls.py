""" This module contains general data ETLs """
from decimal import Decimal
from sqlalchemy import Engine
import pandas as pd
from src.Utils.helpers import DataMgmtHelpers as dmh

class GetToInt:
    def __init__(self, data_dict:dict):
        self.data = data_dict

    @staticmethod
    def count_decimal_places(x):
        """Counts the number of decimal places in a float."""
        x_decimal = Decimal(str(x))
        return max(-x_decimal.as_tuple().exponent, 0)

    def find_to_int_val(self) -> int:
        """Finds how many factors of 10 needed to convert a security price to an int"""
        df = pd.DataFrame(self.data)

        # Calculate the max multiplier
        price_columns = ['Open', 'High', 'Low', 'Close']
        to_int = df[price_columns].map(self.count_decimal_places).max().max()
        return to_int

class MarketDataAggregation:
    """This class contains all of the methods for market data aggregation"""
    def __init__(self, engine:Engine):
        self.logger = dmh.setup_log_to_console()
        self.db_engine = engine

    def insert_records(self, table_name:str):
        pass

    def update_records(self):
        pass

    def upsert_records(self):
        pass
    