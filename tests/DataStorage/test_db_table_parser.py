import os
import unittest
from sqlalchemy import text, TextClause
from sqlalchemy.engine import Engine
from unittest.mock import patch, mock_open, MagicMock, ANY

from src.DataStorage.Utils.table_creation import DataTableCreation
from src.DataStorage.Utils.helpers import DataStorageHelpers as dsh
from src.DataStorage.Utils.config_parser import DBConfigParser

class TestDBTableCreation(unittest.TestCase):
    def setUp(self):
        # Create an instance of DBTableCreation without loading a config file
        self.dbtable = DataTableCreation.__new__(DataTableCreation)
        
        # Manually set all attributes created during initialization
        self.dbtable.config_info = DBConfigParser()
        self.dbtable.config_info.security_types = ['STK', 'ETF', 'FUT', 'CASH'] 
        self.dbtable.config_info.quotes_flag = True
        self.dbtable.config_info.ohlcv_flag = True
        self.dbtable.config_info.market_data_flag = True
        self.dbtable.config_info.db_dialect = 'sqlite'
        self.dbtable.config_info.db_path = ':memory:'
        self.dbtable.sql_base_path = 'core/DataStorage/TableCreationSQL'
        self.dbtable.logger = dsh.setup_log_to_console()
        self.dbtable.equities_flag = True
        self.dbtable.underlying_flag = True
    
    def test_create_core_list_both(self):
        """
        Test that create_core_list returns the expected list of file paths when both quotes_flag and ohlcv_flag are True.
        """
        core_list = self.dbtable.create_core_list()
        expected_quotes = os.path.join(self.dbtable.sql_base_path, 'core_market_data_quotes.sql')
        expected_ohlcv = os.path.join(self.dbtable.sql_base_path, 'core_market_data_ohlcv.sql')
        self.assertIn(expected_quotes, core_list)
        self.assertIn(expected_ohlcv, core_list)
        self.assertEqual(len(core_list), 2)
    
    def test_create_core_list_only_ohlcv(self):
        """
        Test that create_core_list returns the expected list of file paths when only ohlcv_flag is True.
        """
        self.dbtable.config_info.quotes_flag = False
        self.dbtable.config_info.ohlcv_flag = True
        core_list = self.dbtable.create_core_list()
        expected_quotes = os.path.join(self.dbtable.sql_base_path, 'core_market_data_quotes.sql')
        expected_ohlcv = os.path.join(self.dbtable.sql_base_path, 'core_market_data_ohlcv.sql')
        self.assertNotIn(expected_quotes, core_list)
        self.assertIn(expected_ohlcv, core_list)
        self.assertEqual(len(core_list), 1)
        # Reset to both true
        self.dbtable.config_info.quotes_flag = True
        self.dbtable.config_info.ohlcv_flag = True

    def test_create_core_list_only_quotes(self):
        """
        Test that create_core_list returns the expected list of file paths when only quotes_flag is True.
        """
        self.dbtable.config_info.quotes_flag = True
        self.dbtable.config_info.ohlcv_flag = False
        core_list = self.dbtable.create_core_list()
        expected_quotes = os.path.join(self.dbtable.sql_base_path, 'core_market_data_quotes.sql')
        expected_ohlcv = os.path.join(self.dbtable.sql_base_path, 'core_market_data_ohlcv.sql')
        self.assertIn(expected_quotes, core_list)
        self.assertNotIn(expected_ohlcv, core_list)
        self.assertEqual(len(core_list), 1)
        # Reset to both true
        self.dbtable.config_info.quotes_flag = True
        self.dbtable.config_info.ohlcv_flag = True
    
    def test_create_metadata_path(self):
        """
        Test the static method create_metadata_path produces the correct file path.
        """
        base_path = "some/base/path"
        script_prefix = "testprefix"
        expected = os.path.join(base_path, "testprefix_tables.sql")
        result = dsh.create_script_path(base_path, script_prefix, 'tables')
        self.assertEqual(result, expected)
    
    def test_create_metadata_list_all_sec_types(self):
        """
        Test that create_metadata_list returns the correct list of metadata file paths. With security_types = ['STK', 'ETF', 'CASH', 'FUT'] and both equities_flag and underlying_flag set,
        we expect two paths from the loop plus two extra.
        """
        metadata_list = self.dbtable.create_metadata_list()
        # Expect 4 (from security_types) + 1 (for equities) + 1 (for underlying) = 6 files.

        self.assertEqual(len(metadata_list), 6)
        expected_stk = os.path.join(self.dbtable.sql_base_path, 'stk_tables.sql')
        expected_etf = os.path.join(self.dbtable.sql_base_path, 'etf_tables.sql')
        expected_equities = os.path.join(self.dbtable.sql_base_path, 'equities_tables.sql')
        expected_underlying = os.path.join(self.dbtable.sql_base_path, 'underlying_assets_tables.sql')
        self.assertIn(expected_stk, metadata_list)
        self.assertIn(expected_etf, metadata_list)
        self.assertIn(expected_equities, metadata_list)
        self.assertIn(expected_underlying, metadata_list)

    def test_initalize_db_engine(self):
        """
        Test that initalize_mkt_data_db returns a valid SQLAlchemy Engine when market_data_flag is True.
        """
        engine = self.dbtable.initalize_db_engine()
        self.assertIsInstance(engine, Engine)
        # With db_path = ':memory:' and db_dialect = 'sqlite', the engine URL should start with "sqlite:///".
        self.assertTrue(engine.url.drivername.startswith('sqlite'))

    @patch("builtins.open", new_callable=mock_open, read_data="SELECT 1;")
    def test_create_core(self, mock_file):
        """
        Test that create_mkt_data_core reads the SQL script file(s) and calls execute on the connection.
        """
        # Create a fake connection and transaction
        fake_transact = MagicMock()
        fake_conn = MagicMock()
        fake_conn.begin.return_value = fake_transact

        # Create a context manager that returns fake_conn
        fake_context = MagicMock()
        fake_context.__enter__.return_value = fake_conn
        fake_context.__exit__.return_value = None
        fake_engine = MagicMock()
        fake_engine.connect.return_value = fake_context

        # Simulate core_list returning one dummy file path.
        dummy_file = os.path.join(self.dbtable.sql_base_path, 'core_market_data_quotes.sql')
        self.dbtable.create_core_list = MagicMock(return_value=[dummy_file])
        self.dbtable.create_core_tables(fake_engine)

        # Check that the file was opened.
        mock_file.assert_called_with(dummy_file, 'r')
        # Check that the SQL script was executed.
        fake_conn.execute.assert_called_with(ANY)
        # Ensure that commit was called.
        fake_transact.commit.assert_called()
    
    @patch("builtins.open", new_callable=mock_open, read_data="SELECT 1;")
    def test_create_mkt_data_metadata(self, mock_file):
        """
        Test that create_mkt_data_metadata reads the metadata script file(s) and calls execute on the connection.
        """
        # Create a fake connection and transaction.
        fake_transact = MagicMock()
        fake_conn = MagicMock()
        fake_conn.begin.return_value = fake_transact

        # Create a context manager that returns fake_conn.
        fake_context = MagicMock()
        fake_context.__enter__.return_value = fake_conn
        fake_context.__exit__.return_value = None
        fake_engine = MagicMock()
        fake_engine.connect.return_value = fake_context

        # Simulate create_metadata_list() returning one dummy file path.
        dummy_file = os.path.join(self.dbtable.sql_base_path, 'core_market_data_quotes.sql')
        self.dbtable.create_metadata_list = MagicMock(return_value=[dummy_file])
        self.dbtable.create_mkt_data_metadata(fake_engine)

        # Check that the file was opened.
        mock_file.assert_called_with(dummy_file, 'r')
        # Check that the SQL script was executed.
        fake_conn.execute.assert_called_with(ANY)
        # Ensure that commit was called.
        fake_transact.commit.assert_called()
    
    @patch("core.DataStorage.Utils.table_creation.open", new_callable=mock_open, read_data="CREATE TABLE foo (id INTEGER);")
    def test_successful_creation(self, mock_file):
        # Create a fake transaction object
        fake_transact = MagicMock()
        # Create a fake connection object
        fake_conn = MagicMock()
        fake_conn.begin.return_value = fake_transact
        fake_context_manager = MagicMock()
        fake_context_manager.__enter__.return_value = fake_conn
        fake_context_manager.__exit__.return_value = False

        # Create a fake engine
        fake_engine = MagicMock(spec=Engine)
        fake_engine.connect.return_value = fake_context_manager

        instance = DataTableCreation()
        instance.create_portfolio_analysis_tables(fake_engine)

        # --- Assertions ---
        # SQL script was opened with the expected file path and contents were read.
        mock_file.assert_called_once_with('core/DataStorage/TableCreationSQL/portfolio_data_warehouse.sql', 'r')
        handle = mock_file()
        handle.read.assert_called_once()
        # The connection.execute method was called with a text clause containing the script.
        fake_conn.execute.assert_called_once()

        # Ensure clause was read in correctly
        executed_arg = fake_conn.execute.call_args[0][0]
        self.assertIsInstance(executed_arg, TextClause)
        self.assertEqual(executed_arg.text, "CREATE TABLE foo (id INTEGER);")
        
        # Ensure transaction’s commit method was called.
        fake_transact.commit.assert_called_once()
    
    @patch("core.DataStorage.Utils.table_creation.open", new_callable=mock_open, read_data="CREATE TABLE foo (id INTEGER);")
    def test_error_during_execution(self, mock_file):
        # Set up a fake connection and transaction
        fake_transact = MagicMock()
        fake_conn = MagicMock()
        fake_conn.begin.return_value = fake_transact

        # Simulate an exception when executing the SQL script.
        fake_conn.execute.side_effect = Exception("SQL Error")
        fake_context_manager = MagicMock()
        fake_context_manager.__enter__.return_value = fake_conn
        fake_context_manager.__exit__.return_value = False
        fake_engine = MagicMock(spec=Engine)
        fake_engine.connect.return_value = fake_context_manager

        # Prepare an instance with a fake logger
        instance = DataTableCreation()
        instance.logger = MagicMock()  # Patch the logger so we can verify logging

        # Call the method and verify it raises an exception
        with self.assertRaises(Exception) as context:
            instance.create_portfolio_analysis_tables(fake_engine)
        self.assertEqual(str(context.exception), "SQL Error")

        # --- Assertions ---
        # Verify that the transaction rollback was called.
        fake_transact.rollback.assert_called_once()
        # Verify that the logger.error was called.
        instance.logger.error.assert_called_once()


if __name__ == '__main__':
    unittest.main()