import unittest
import tempfile
import os
from core.DataStorage.db_initializer import DBInitializer
from sqlalchemy import Engine

class TestDBInitializer(unittest.TestCase):
    def test_db_initializer_valid_config(self):
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
                db_init = DBInitializer(config_path=config_path)
            except Exception as e:
                self.fail(f"DBInitializer raised an unexpected exception: {e}")

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

    def test_db_file_not_found(self):
        """
        Test to ensure that the proper error is being raised when the config file cannot be found
        """
        # Create a path to a non-existent config file
        bad_config_path = 'this_file_dne.yml'

        with self.assertRaises(FileNotFoundError):
            DBInitializer(config_path=bad_config_path)
    
    def test_orm_engine_initialization_sqlite(self): 
        db_init = DBInitializer()
        mkt_data_engine = db_init.initialize_mkt_data_engine()
        portfolio_data_engine = db_init.initialize_portfolio_data_engine()
        if mkt_data_engine:
            self.assertIsInstance(mkt_data_engine, Engine, "received incorrect data type for the market data engine")
            self.assertEqual(mkt_data_engine.driver, "pysqlite", f"did not receive the correct driver for mkt_data_engine: {mkt_data_engine.driver}")
        if portfolio_data_engine:
            self.assertIsInstance(portfolio_data_engine, Engine, "received incorrect data type for the portfolio data engine")
            self.assertEqual(portfolio_data_engine.driver, "pysqlite", f"did not receive the correct driver for mkt_data_engine: {mkt_data_engine.driver}")
    
    def test_schema_checks(self):
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
                                    time_granularity: quotes
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
                db_init = DBInitializer(config_path=config_path)
                self.assertWarns(UserWarning)
            except Exception as e:
                self.fail(f"DBInitializer raised an unexpected exception: {e}")
    def test_db_checks(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a path to our temporary config file
            config_path = os.path.join(temp_dir, "test_config.yml")
        
            config_content = """
                                database:
                                    driver: PostgreSQL
                                    host: local
                                    mkt_data_dbpath: D:/sqlite/SAFT/Testing/price_history.db
                                    portfolio_data_dbpath: D:/sqlite/SAFT/Testing/portfolio_warehouse.db
                                schemas:
                                    market_data: true
                                    convert_price_to_int: true
                                    portfolio_data: false
                                    time_granularity: quotes
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
                db_init = DBInitializer(config_path=config_path)
                self.assertRaises(ValueError)
            except Exception as e:
                self.fail(f"DBInitializer raised an unexpected exception: {e}")
    def test_sec_types_checks(self):
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
                                    ohlcv: true
                                    quotes: false 
                                security_types:
                                    - OPT
                                seed_data:
                                    - SecTypes
                                    - Exchanges
                            """
            with open(config_path, 'w') as f:
                f.write(config_content)
            try:
                db_init = DBInitializer(config_path=config_path)
                self.assertRaises(ValueError)
            except Exception as e:
                self.fail(f"DBInitializer raised an unexpected exception: {e}")
            with tempfile.TemporaryDirectory() as temp_dir:
                # Create a path to our temporary config file      
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
                                    ohlcv: true
                                    quotes: false 
                                security_types:
                                    - some
                                seed_data:
                                    - SecTypes
                                    - Exchanges
                            """
            with open(config_path, 'w') as f:
                f.write(config_content)
            try:
                db_init = DBInitializer(config_path=config_path)
                self.assertRaises(ValueError)
            except Exception as e:
                self.fail(f"DBInitializer raised an unexpected exception: {e}")
            
    def test_file_list(self):
        with tempfile.TemporaryDirectory() as temp_dir:
                config_path = os.path.join(temp_dir, "test_config.yml")
                # Create a path to our temporary config file      
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
                                    ohlcv: true
                                    quotes: false 
                                security_types:
                                    - FUT
                                    - STK
                                    - ETF
                                    - CASH
                                seed_data:
                                    - SecTypes
                                    - Exchanges
                            """
                with open(config_path, 'w') as f:
                    f.write(config_content)
                try:
                    db_init = DBInitializer(config_path=config_path)
                    file_list = db_init.create_file_list()
                    self.assertIn(r'core\DataStorage\TableCreationSQL\futures_tables.sql', file_list, "the futures tables were not included in the list properly")
                    self.assertIn(r'core\DataStorage\TableCreationSQL\etf_tables.sql', file_list, "the ETF tables were not included in the list properly")
                    self.assertIn(r'core\DataStorage\TableCreationSQL\fx_tables.sql', file_list, "the FX tables were not included in the list properly")
                    self.assertIn(r'core\DataStorage\TableCreationSQL\stcok_tables.sql', file_list, "the stocks tables were not included in the list properly")
                except Exception as e:
                    raise
    def test_initialize_core_tables(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = os.path.join(temp_dir, "test_config.yml")
            # Create a path to our temporary config file      
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
                                ohlcv: true
                                quotes: false 
                            security_types:
                                - FUT
                                - STK
                                - ETF
                                - CASH
                            seed_data:
                                - SecTypes
                                - Exchanges
                        """
            with open(config_path, 'w') as f:
                f.write(config_content)
            try:
                db_init = DBInitializer(config_path=config_path)
                file_list = db_init.create_file_list()
                self.assertIn(r'core\DataStorage\TableCreationSQL\futures_tables.sql', file_list, "the futures tables were not included in the list properly")
                self.assertIn(r'core\DataStorage\TableCreationSQL\etf_tables.sql', file_list, "the ETF tables were not included in the list properly")
                self.assertIn(r'core\DataStorage\TableCreationSQL\fx_tables.sql', file_list, "the FX tables were not included in the list properly")
                self.assertIn(r'core\DataStorage\TableCreationSQL\stcok_tables.sql', file_list, "the stocks tables were not included in the list properly")
            except Exception as e:
                raise

if __name__ == '__main__':
    unittest.main()