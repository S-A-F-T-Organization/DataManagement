"""Tests the database strategies for handling historical prices."""
import time
import shutil
import tempfile
import unittest
from unittest.mock import patch, MagicMock
import os

from sqlalchemy import inspect

from saft_data_mgmt.Utils.db_strategies import (
    HistoricalPricesStrategy,
    ToIntStrategy,
    RealStrategy,
    MetadataStrategies,
    StocksMetadata,
    ETFMetadata,
    ForexMetadata,
    FuturesMetadata,
    CoreTables,
    PortfolioDBTables,
)
from saft_data_mgmt.Utils.helpers import create_table, initalize_db_engine
from saft_data_mgmt.Utils.config_info import ConfigInfo


class TestHistoricalPricesStrategy(unittest.TestCase):
    """Tests the historical prices strategy base class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.config_info = ConfigInfo(
            db_dialect="sqlite",
            db_path=":memory:",
            db_name="test.db",
            security_types=["STK", "OPT"],
            ohlcv_flag=True,
            full_quotes_flag=True,
        )

    def test_historical_prices_strategy_initialization(self):
        """Test that the base class initializes correctly."""

        class ConcreteHistoricalPrices(HistoricalPricesStrategy):
            """Concrete implementation of the HistoricalPricesStrategy for testing."""

            def get_tables(self):
                return []

        strategy = ConcreteHistoricalPrices(self.config_info)
        self.assertEqual(strategy.db_path, ":memory:")
        self.assertEqual(strategy.db_dialect, "sqlite")
        self.assertEqual(strategy.scripts_base, "saft_data_mgmt/SQLTables/HistoricalPrices")
        self.assertEqual(strategy.config_info, self.config_info)
        self.assertEqual(strategy.config_info.db_name, "test.db")

    @patch("saft_data_mgmt.Utils.db_strategies.initalize_db_engine")
    def test_db_engine_property(self, mock_init_engine):
        """Test that the db_engine property initializes correctly."""

        class ConcreteHistoricalPrices(HistoricalPricesStrategy):
            """Concrete implementation of the HistoricalPricesStrategy for testing."""

            def get_tables(self):
                return []

        mock_engine = MagicMock()
        mock_init_engine.return_value = mock_engine

        strategy = ConcreteHistoricalPrices(self.config_info)
        engine = strategy.db_engine

        mock_init_engine.assert_called_once_with("sqlite", ":memory:", "test.db")
        self.assertEqual(engine, mock_engine)


class TestToIntStrategy(unittest.TestCase):
    """Test the ToIntStrategy class for handling historical prices."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.config_info = ConfigInfo(
            db_dialect="sqlite",
            db_path=":memory:",
            security_types=[],
            ohlcv_flag=False,
            quotes_flag=False,
            full_quotes_flag=False,
        )

    def test_get_tables_empty(self):
        """Test that get_tables returns empty list when no flags are set."""
        strategy = ToIntStrategy(self.config_info)
        self.assertEqual(strategy.get_tables(), [])

    def test_get_tables_all_flags(self):
        """Test that get_tables returns all tables when all flags are set."""
        self.config_info.security_types = ["OPT"]
        self.config_info.quotes_flag = True
        self.config_info.ohlcv_flag = True
        self.config_info.full_quotes_flag = True

        strategy = ToIntStrategy(self.config_info)
        expected_tables = [
            "options_ohlcv_int.sql",
            "security_prices_ohlcv_int.sql",
            "security_prices_mbp_full_int.sql",
        ]
        self.assertEqual(strategy.get_tables(), expected_tables)

    def test_only_ohlcv(self):
        """Test that get_tables returns only the securities ohlcv table"""
        self.config_info.security_types = ["STK"]
        self.config_info.quotes_flag = False
        self.config_info.ohlcv_flag = True
        self.config_info.full_quotes_flag = False

        strategy = ToIntStrategy(self.config_info)
        expected_tables = ["security_prices_ohlcv_int.sql"]
        self.assertEqual(strategy.get_tables(), expected_tables)

    def test_only_ohlcv_full_quotes(self):
        """
        Test that get_tables returns only the securities ohlcv table if somehow the full quotes flag is set
        to true while the quotes flag is false
        """
        self.config_info.security_types = ["STK"]
        self.config_info.quotes_flag = False
        self.config_info.ohlcv_flag = True
        self.config_info.full_quotes_flag = True

        strategy = ToIntStrategy(self.config_info)
        expected_tables = ["security_prices_ohlcv_int.sql"]
        self.assertEqual(strategy.get_tables(), expected_tables)

    def test_consolidated_quotes_and_opts(self):
        """
        Test that get_tables returns only the the options ohlcv table and the consolidated quotes table correctly
        """
        self.config_info.security_types = ["OPT"]
        self.config_info.quotes_flag = True
        self.config_info.ohlcv_flag = False
        self.config_info.full_quotes_flag = False

        strategy = ToIntStrategy(self.config_info)
        expected_tables = [
            "options_ohlcv_int.sql",
            "security_prices_mbp_consolidated_int.sql",
        ]
        self.assertEqual(strategy.get_tables(), expected_tables)


class TestRealStrategy(unittest.TestCase):
    """Test the RealStrategy class for handling historical prices."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.config_info = ConfigInfo(
            db_dialect="sqlite",
            db_path=":memory:",
            security_types=[],
            ohlcv_flag=False,
            full_quotes_flag=False,
        )

    def test_get_tables_empty(self):
        """Test that get_tables returns empty list when no flags are set."""
        strategy = RealStrategy(self.config_info)
        self.assertEqual(strategy.get_tables(), [])

    def test_get_tables_all_flags(self):
        """Test that get_tables returns all tables when all flags are set."""
        self.config_info.security_types = ["OPT"]
        self.config_info.ohlcv_flag = True
        self.config_info.quotes_flag = True
        self.config_info.full_quotes_flag = True
        self.config_info.to_int_flag = False

        strategy = RealStrategy(self.config_info)
        expected_tables = [
            "options_ohlcv_float.sql",
            "security_prices_ohlcv_float.sql",
            "security_prices_mbp_full_float.sql",
        ]
        self.assertEqual(strategy.get_tables(), expected_tables)

    @patch("saft_data_mgmt.Utils.db_strategies.create_table")
    @patch("saft_data_mgmt.Utils.db_strategies.initalize_db_engine")
    def test_create_historical_prices_tables(self, mock_init_engine, mock_create_table):
        """Test that create_historical_prices_tables creates tables correctly."""
        self.config_info.security_types = ["OPT"]
        self.config_info.ohlcv_flag = True

        mock_engine = MagicMock()
        mock_init_engine.return_value = mock_engine

        strategy = RealStrategy(self.config_info)
        strategy.create_historical_prices_tables()

        expected_calls = [
            unittest.mock.call(
                db_engine=mock_engine,
                full_path="saft_data_mgmt/SQLTables/HistoricalPrices\\options_ohlcv_float.sql",
            ),
            unittest.mock.call(
                db_engine=mock_engine,
                full_path="saft_data_mgmt/SQLTables/HistoricalPrices\\security_prices_ohlcv_float.sql",
            ),
        ]
        mock_create_table.assert_has_calls(expected_calls)

    def test_only_ohlcv(self):
        """Test that get_tables returns only the securities ohlcv table"""
        self.config_info.security_types = ["STK"]
        self.config_info.quotes_flag = False
        self.config_info.ohlcv_flag = True
        self.config_info.full_quotes_flag = False
        self.config_info.to_int_flag = False

        strategy = RealStrategy(self.config_info)
        expected_tables = ["security_prices_ohlcv_float.sql"]
        self.assertEqual(strategy.get_tables(), expected_tables)

    def test_only_ohlcv_full_quotes(self):
        """
        Test that get_tables returns only the securities ohlcv table if somehow the full quotes flag is set
        to true while the quotes flag is false
        """
        self.config_info.security_types = ["STK"]
        self.config_info.quotes_flag = False
        self.config_info.ohlcv_flag = True
        self.config_info.full_quotes_flag = True

        strategy = RealStrategy(self.config_info)
        expected_tables = ["security_prices_ohlcv_float.sql"]
        self.assertEqual(strategy.get_tables(), expected_tables)

    def test_consolidated_quotes_and_opts(self):
        """
        Test that get_tables returns only the the options ohlcv table and the consolidated quotes table correctly
        """
        self.config_info.security_types = ["OPT"]
        self.config_info.quotes_flag = True
        self.config_info.ohlcv_flag = False
        self.config_info.full_quotes_flag = False

        strategy = RealStrategy(self.config_info)
        expected_tables = [
            "options_ohlcv_float.sql",
            "security_prices_mbp_consolidated_float.sql",
        ]
        self.assertEqual(strategy.get_tables(), expected_tables)


class TestMetadataStrategies(unittest.TestCase):
    """Tests the MetadataStrategies are called and execute correctly."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.config_info = ConfigInfo(
            db_dialect="sqlite", db_path=":memory:", security_types=["STK", "ETF"]
        )

    def test_metadata_strategy_initialization(self):
        """Test that the base class initializes correctly."""

        class ConcreteMetadata(MetadataStrategies):
            """Concrete implementation of the MetadataStrategies for testing."""

            def get_first_scripts(self):
                return []

            def get_main_scripts(self):
                return []

        strategy = ConcreteMetadata(self.config_info)
        self.assertEqual(strategy.db_path, ":memory:")
        self.assertEqual(strategy.db_dialect, "sqlite")
        self.assertEqual(strategy.security_types, ["STK", "ETF"])
        self.assertEqual(strategy.scripts_base, "saft_data_mgmt/SQLTables/SecuritiesMetadata")

    @patch("saft_data_mgmt.Utils.db_strategies.create_table")
    @patch("saft_data_mgmt.Utils.db_strategies.initalize_db_engine")
    def test_create_metadata_tables(self, mock_init_engine, mock_create_table):
        """Test table creation sequence"""
        mock_engine = MagicMock()
        mock_init_engine.return_value = mock_engine

        class TestMetadata(MetadataStrategies):
            """Concrete implementation of the MetadataStrategies for testing."""

            def get_first_scripts(self):
                return ["test1.sql", "test2.sql"]

            def get_main_scripts(self):
                return ["main.sql"]

        strategy = TestMetadata(self.config_info)
        strategy.create_metadata_tables()

        expected_calls = [
            unittest.mock.call(
                db_engine=mock_engine,
                full_path="saft_data_mgmt/SQLTables/SecuritiesMetadata\\test1.sql",
            ),
            unittest.mock.call(
                db_engine=mock_engine,
                full_path="saft_data_mgmt/SQLTables/SecuritiesMetadata\\test2.sql",
            ),
        ]
        mock_create_table.assert_has_calls(expected_calls, any_order=False)


class TestStocksMetadata(unittest.TestCase):
    """Tests the StocksMetadata strategy for handling metadata."""

    def setUp(self):
        self.config_info = ConfigInfo(
            db_dialect="sqlite", db_path=":memory:", security_types=["STK"]
        )
        self.strategy = StocksMetadata(self.config_info)

    def test_get_first_scripts(self):
        """Test first scripts for stocks metadata"""
        expected_scripts = [
            "stock_splits.sql",
            "sector_info.sql",
            "industry_info.sql",
            "fundamentals_snapshots.sql",
        ]
        self.assertEqual(self.strategy.get_first_scripts(), expected_scripts)

    def test_get_main_scripts(self):
        """Test main scripts for stocks metadata"""
        expected_scripts = ["stock_table.sql", "equities_snapshots.sql"]
        self.assertEqual(self.strategy.get_main_scripts(), expected_scripts)


class TestETFMetadata(unittest.TestCase):
    """Test the ETFMetadata class for handling ETFs metadata."""

    def setUp(self):
        self.config_info = ConfigInfo(
            db_dialect="sqlite", db_path=":memory:", security_types=["ETF"]
        )
        self.strategy = ETFMetadata(self.config_info)

    def test_get_first_scripts(self):
        """Test first scripts for ETF metadata"""
        expected_scripts = [
            "issuers.sql",
            "underlying_types.sql",
            "fundamentals_snapshots.sql",
        ]
        self.assertEqual(self.strategy.get_first_scripts(), expected_scripts)

    def test_get_main_scripts(self):
        """Test main scripts for ETF metadata"""
        expected_scripts = ["etf_table.sql", "equities_snapshots.sql"]
        self.assertEqual(self.strategy.get_main_scripts(), expected_scripts)


class TestForexMetadata(unittest.TestCase):
    """Test the ForexMetadata class for handling metadata."""

    def setUp(self):
        self.config_info = ConfigInfo(
            db_dialect="sqlite", db_path=":memory:", security_types=["CASH"]
        )
        self.strategy = ForexMetadata(self.config_info)

    def test_get_first_scripts(self):
        """Test first scripts for Forex metadata"""
        expected_scripts = ["currency_metadata.sql"]
        self.assertEqual(self.strategy.get_first_scripts(), expected_scripts)

    def test_get_main_scripts(self):
        """Test main scripts for Forex metadata"""
        expected_scripts = ["cash_table.sql"]
        self.assertEqual(self.strategy.get_main_scripts(), expected_scripts)


class TestFuturesMetadata(unittest.TestCase):
    """Tests the FuturesMetadata class for handling futures metadata."""

    def setUp(self):
        self.config_info = ConfigInfo(
            db_dialect="sqlite", db_path=":memory:", security_types=["FUT"]
        )
        self.strategy = FuturesMetadata(self.config_info)

    def test_get_first_scripts(self):
        """Test first scripts for Futures metadata"""
        expected_scripts = ["underlying_types.sql"]
        self.assertEqual(self.strategy.get_first_scripts(), expected_scripts)

    def test_get_main_scripts(self):
        """Test main scripts for Futures metadata"""
        expected_scripts = ["fut_table.sql"]
        self.assertEqual(self.strategy.get_main_scripts(), expected_scripts)


class TestCoreTables(unittest.TestCase):
    """Tests the CoreTables class for creating the core database tables."""

    def setUp(self):
        """Set up an in-memory SQLite database for testing."""

        self.config_info = ConfigInfo(
            db_dialect="sqlite",
            db_path=tempfile.mkdtemp(),
            db_name="test.db",
            to_int_flag=False,
        )
        self.core_tables = CoreTables(self.config_info)
        self.engine = initalize_db_engine("sqlite", self.config_info.db_path, "test.db")

    def tearDown(self):
        """Cleanup test database and files after each test."""
        if hasattr(self, 'engine'):
            self.engine.dispose()  # Dispose of the SQLAlchemy engine
        time.sleep(0.5)  # Small delay to allow OS to release the file (optional)
        shutil.rmtree(self.config_info.db_path, ignore_errors=True)


    def test_initialization(self):
        """Test that the CoreTables class is initialized correctly."""
        self.assertEqual(self.core_tables.config_info, self.config_info)
        self.assertEqual(self.core_tables.core_folder, "saft_data_mgmt/SQLTables/Core")
        self.assertEqual(
            self.core_tables.first_scripts,
            ["security_exchange.sql", "security_types.sql", "securities_info.sql"],
        )

    @patch("saft_data_mgmt.Utils.db_strategies.create_table")
    def test_create_core_tables(self, mock_create_table):
        """Test that create_core_tables calls create_table with the correct paths."""
        self.core_tables.create_core_tables()

        expected_calls = [  # noqa: F841 pylint: disable=unused-variable
            unittest.mock.call(
                db_engine=self.engine,
                full_path="saft_data_mgmt/SQLTables/Core\\security_exchange.sql",
            ),
            unittest.mock.call(
                db_engine=self.engine,
                full_path="saft_data_mgmt/SQLTables/Core\\security_types.sql",
            ),
            unittest.mock.call(
                db_engine=self.engine,
                full_path="saft_data_mgmt/SQLTables/Core\\securities_info.sql",
            ),
        ]
        self.assertEqual(mock_create_table.call_count, 3)

    def test_security_types_table_structure(self):
        """Test that the SecurityTypes table is created with the correct structure."""
        # Create the table from the actual SQL file
        sql_path = os.path.join("saft_data_mgmt", "SQLTables", "Core", "security_types.sql")
        create_table(self.engine, sql_path)

        # Use SQLAlchemy inspector to check table structure
        inspector = inspect(self.engine)
        self.assertTrue(
            inspector.has_table("SecurityTypes"), "SecurityTypes table was not created."
        )

        columns = inspector.get_columns("SecurityTypes")
        self.assertEqual(len(columns), 2, "SecurityTypes table should have 2 columns.")

        # Check primary key column
        security_type_id = columns[0]
        self.assertEqual(security_type_id["name"], "security_type_id")
        self.assertTrue(security_type_id["primary_key"])
        self.assertEqual(str(security_type_id["type"]).upper(), "INTEGER")

        # Check security type column
        security_type = columns[1]
        self.assertEqual(security_type["name"], "security_type")
        self.assertFalse(security_type["nullable"])
        self.assertEqual(str(security_type["type"]).upper(), "TEXT")

        # Check unique constraint
        unique_constraints = inspector.get_unique_constraints("SecurityTypes")
        self.assertEqual(len(unique_constraints), 1)
        self.assertEqual(unique_constraints[0]["column_names"], ["security_type"])

    def test_securities_info_table_structure(self):
        """Test that the SecuritiesInfo table is created with the correct structure."""
        sql_path = os.path.join("saft_data_mgmt", "SQLTables", "Core", "securities_info.sql")
        create_table(self.engine, sql_path)

        # Use SQLAlchemy inspector to check table structure
        inspector = inspect(self.engine)
        self.assertTrue(
            inspector.has_table("SecuritiesInfo"),
            "SecuritiesInfo table was not created.",
        )

        columns = inspector.get_columns("SecuritiesInfo")
        self.assertEqual(len(columns), 5, "SecuritiesInfo table should have 5 columns.")

        # Check primary key column
        symbol_id = columns[0]
        self.assertEqual(symbol_id["name"], "symbol_id")
        self.assertTrue(symbol_id["primary_key"])

        # Check foreign key
        fk_info = inspector.get_foreign_keys("SecuritiesInfo")
        self.assertEqual(
            len(fk_info), 2, "SecuritiesInfo table should have 2 foreign keys."
        )

        # Verify symbol_id is unique
        unique_constraints = inspector.get_unique_constraints("SecuritiesInfo")
        self.assertEqual(
            len(unique_constraints), 1, "Expected unique constraint on symbol column."
        )


class TestPortfolioDBTables(unittest.TestCase):
    """Tests the PortfolioDBTables class for creating portfolio database tables."""

    def setUp(self):
        """Set up an in-memory SQLite database for testing."""
        self.config_info = ConfigInfo(
            db_dialect="sqlite",
            db_path=tempfile.mkdtemp(),
            db_name="test.db",
            to_int_flag=False,
            portfolio_data_flag=True,
        )
        self.portfolio_tables = PortfolioDBTables(self.config_info)
        self.engine = initalize_db_engine("sqlite", self.config_info.db_path, "test.db")

        # Create required tables for foreign key references
        self.setup_required_tables()

        self.core_tables = CoreTables(self.config_info)
        self.engine = initalize_db_engine("sqlite", self.config_info.db_path, "test.db")

    def setup_required_tables(self):
        """Create tables needed for foreign key references."""
        # Create SecuritiesInfo table
        create_table(
            self.engine, os.path.join("saft_data_mgmt", "SQLTables", "Core", "securities_info.sql")
        )

    def tearDown(self):
        """Cleanup test database and files after each test."""
        if hasattr(self, 'engine'):
            self.engine.dispose()  # Dispose of the SQLAlchemy engine
        time.sleep(0.5)  # Small delay to allow OS to release the file (optional)
        shutil.rmtree(self.config_info.db_path, ignore_errors=True)

    def test_initialization(self):
        """Test that the PortfolioDBTables class is initialized correctly."""
        self.assertEqual(self.portfolio_tables.config_info, self.config_info)
        self.assertEqual(
            self.portfolio_tables.core_folder, "saft_data_mgmt/SQLTables/PortfolioDB"
        )

    def test_inference_tables_property(self):
        """Test that inference_tables returns the correct list of inference table scripts."""
        expected_tables = [
            "strategies.sql",
            "model_libraries.sql",
            "model_types.sql",
            "models.sql",
            "strategy_modules.sql",
            "inference_steps.sql",
            "sessions.sql",
            "inferences.sql",
            "inference_times.sql",
        ]
        self.assertEqual(self.portfolio_tables.inference_tables, expected_tables)

    def test_transaction_tables_property(self):
        """Test that transaction_tables returns the correct list of transaction table scripts."""
        expected_tables = [
            "account_info.sql",
            "transaction_types.sql",
            "transactions.sql",
            "order_actions.sql",
            "order_types.sql",
            "all_orders.sql",
            "executed_orders.sql",
            "cancelled_orders.sql",
            "conditional_orders.sql",
        ]
        self.assertEqual(self.portfolio_tables.transaction_tables, expected_tables)

    @patch("saft_data_mgmt.Utils.db_strategies.create_table")
    def test_create_portfolio_tables(self, mock_create_table):
        """Test that create_portfolio_tables calls create_table with the correct paths."""
        self.portfolio_tables.create_portfolio_tables()

        expected_calls = []

        # Add inference table calls
        for script in self.portfolio_tables.inference_tables:
            expected_calls.append(
                unittest.mock.call(
                    db_engine=self.engine,
                    full_path=f"saft_data_mgmt/SQLTables/Core/PortfolioDB\\{script}",
                )
            )

        # Add transaction table calls
        for script in self.portfolio_tables.transaction_tables:
            expected_calls.append(
                unittest.mock.call(
                    db_engine=self.engine,
                    full_path=f"saft_data_mgmt/SQLTables/Core/PortfolioDB\\{script}",
                )
            )
        self.assertEqual(
            mock_create_table.call_count,
            len(self.portfolio_tables.inference_tables)
            + len(self.portfolio_tables.transaction_tables),
        )

    def test_strategies_table_structure(self):
        """Test that the strategies table is created with the correct structure."""
        # Create the table from the actual SQL file if it exists
        sql_path = os.path.join("saft_data_mgmt", "SQLTables", "PortfolioDB", "strategies.sql")

        # Skip test if file doesn't exist
        if not os.path.exists(sql_path):
            self.skipTest(f"SQL file {sql_path} not found")

        create_table(self.engine, sql_path)

        # Use SQLAlchemy inspector to check table structure
        inspector = inspect(self.engine)
        self.assertTrue(
            inspector.has_table("Strategies"), "Strategies table was not created."
        )
