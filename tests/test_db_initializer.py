""" This module tests the db_initializer module """
import unittest
from unittest.mock import patch, mock_open, MagicMock
from src.DataStorage.db_builder import DBBuilder

# The YAML file content you want to mock:
MOCK_YAML = """
database:
  dialect: sqlite3
  db_path: D:/sqlite/SAFT/Testing/saft_data.db

schemas:
  market_data: true
  convert_price_to_int: true
  portfolio_data: false
  ohlcv: true
  quotes: false

security_types:
  - STK
  - ETF
  - CASH
  - FUT

seed_data:
  - SecTypes
  - Exchanges
  - FUT
  - CASH
  - STK
  - ETF
""".strip()

class TestDBBuilder(unittest.TestCase):
    """
    _summary_

    Args:
        unittest (_type_): _description_
    """
    @patch("src.DataStorage.Utils.table_creation.open")
    @patch("src.DataStorage.DBConfigParser.open", new_callable=mock_open, read_data=MOCK_YAML)
    @patch("src.DataStorage.DBBuilder.DBConfigParser")
    @patch("src.DataStorage.DBBuilder.DataTableCreation")
    def test_initialize_new_db_creates_all_tables(
            self, mock_dtc_class, mock_parser_class,
            mock_config_open, mock_table_open):
        """
        _summary_

        Args:
            mock_dtc_class (_type_): _description_
            mock_parser_class (_type_): _description_
            mock_config_open (_type_): _description_
            mock_table_open (_type_): _description_
        """
        
        
        return None

if __name__ == '__main__':
    unittest.main()
