"""This module contains ETL workflows for SAFT specific tables to help with aggregating data"""
from decimal import Decimal
import pandas as pd
def get_to_int_value(price_data) -> int:
    """
    Determine how many factors of 10 are needed to convert security prices to integer form.
    Scans the 'Open', 'High', 'Low', and 'Close' columns for decimal precision and returns
    the maximum number of decimal places found.

    Args:
        price_data: Any object convertible to a pandas DataFrame (e.g., list of dicts, dict of lists).

    Returns:
        int: The maximum decimal precision across the four price columns.
    """
    df = pd.DataFrame(price_data)
    price_columns = ['Open', 'High', 'Low', 'Close']
    decimal_places_df = df[price_columns].map(
        lambda x: max(-Decimal(str(x)).as_tuple().exponent, 0)
    )
    to_int = decimal_places_df.max().max()
    return to_int

def get_exchange_info():
    """Gets all of the the exchange information"""

def get_core_info(symbol:str, sec_type:str):
    """Finds all of the attributes in the SAFT core tables"""