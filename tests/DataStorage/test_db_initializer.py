import unittest
import tempfile
import os
from src.DataStorage.db_builder import DBBuilder
from sqlalchemy import Engine

class TestDBBuilder(unittest.TestCase):
    def test_db_builder_valid_config(self):
        """
        Test to ensure that a mock of a valid config file is being read correctly
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a path to our temporary config file
            config_path = os.path.join(temp_dir, "test_config.yml")
        
            config_content = """
                                database:
                                    driver: sqlite3
                                    host: local
                                    mkt_data_dbpath: D:/sqlite/SAFT/Testing/price_history.db
                                    portfolio_data_dbpath: D:/sqlite/SAFT/Testing/portfolio_warehouse.db
                                schemas:
                                    market_data: true
                                    convert_price_to_int: true
                                    portfolio_data: false
                                security_types:
                                    - stock
                                    - futures
                                seed_data:
                                    - SecTypes
                                    - Exchanges
                            """
            with open(config_path, 'w') as f:
                f.write(config_content)
            try:
                db_init = DBBuilder(config_path=config_path)
            except Exception as e:
                self.fail(f"DBBuilder raised an unexpected exception: {e}")

            ## Assert all sections are being read in
            self.assertIsNotNone(db_init.config_data, "db_info should not be None")
            self.assertIn("database", db_init.config_data, "db_info should contain 'database'")
            self.assertIn("schemas", db_init.config_data, "db_info should contain 'schemas'")
            self.assertIn("security_types", db_init.config_data, "db_info should contain 'security_types'")
            self.assertIn("seed_data", db_init.config_data, "db_info should contain 'user'")
            ## Assert database info is being read in correctly
            self.assertEqual(db_init.db_info['driver'], "sqlite3", "the database drive is not being read as sqlite3")
            self.assertEqual(db_init.db_info['mkt_data_dbpath'], "D:/sqlite/SAFT/Testing/price_history.db", "the database mkt_data_dbpath is being read incorrectly")
            self.assertEqual(db_init.db_info['portfolio_data_dbpath'], "D:/sqlite/SAFT/Testing/portfolio_warehouse.db", "the database portfolio_data_dbpath is being read incorrectly")
            ## Assert schemas is being read in correctly           
            self.assertEqual(db_init.market_data_flag, True)
            self.assertEqual(db_init.to_int_flag, True)
            self.assertEqual(db_init.portfolio_data_flag, False)
            ## Assert security types is being read in correctly
            self.assertIsNotNone(db_init.config_data["security_types"])
            self.assertEqual(len(db_init.config_data["security_types"]), 2)
            ## Assert seed_data is being read in correctly
            self.assertIsNotNone(db_init.config_data["seed_data"])
            self.assertEqual(len(db_init.config_data["seed_data"]), 2)