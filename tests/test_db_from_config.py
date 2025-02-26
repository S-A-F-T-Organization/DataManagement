"""Tests for the DBFromConfig class."""

import unittest
from unittest.mock import patch, MagicMock, call
import logging
from saft_data_mgmt.Utils.db_from_config import DBFromConfig
from saft_data_mgmt.Utils.config_info import ConfigInfo
from saft_data_mgmt.Utils import db_strategies as strats


class TestDBFromConfig(unittest.TestCase):
    """Tests for the DBFromConfig class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.config_info = ConfigInfo()
        self.config_info.db_dialect = "sqlite"
        self.config_info.db_path = "/path/to/db"
        self.config_info.db_name = "test.db"
        self.config_info.market_data_flag = True
        self.config_info.portfolio_data_flag = True
        self.config_info.to_int_flag = True
        self.config_info.ohlcv_flag = True
        self.config_info.quotes_flag = False
        self.config_info.security_types = ["STK", "ETF"]

        # Create the DBFromConfig instance
        with patch("saft_data_mgmt.Utils.helpers.setup_log_to_console") as mock_setup_log:
            mock_setup_log.return_value = MagicMock(spec=logging.Logger)
            self.db_from_config = DBFromConfig(self.config_info)
            self.mock_logger = self.db_from_config.logger

    def test_init_with_specific_security_types(self):
        """Test initialization with specific security types."""
        self.assertEqual(self.db_from_config.config_info.security_types, ["STK", "ETF"])

    def test_init_with_all_security_types(self):
        """Test initialization with 'ALL' as security types."""
        self.config_info.security_types = ["ALL"]

        with patch("saft_data_mgmt.Utils.helpers.setup_log_to_console"):
            db_from_config = DBFromConfig(self.config_info)

        expected_types = ["STK", "ETF", "FUT", "FOREX", "FUND", "OPT"]
        self.assertEqual(db_from_config.config_info.security_types, expected_types)

    def test_init_with_empty_security_types(self):
        """Test initialization with empty security types list."""
        self.config_info.security_types = []

        with patch("saft_data_mgmt.Utils.helpers.setup_log_to_console"):
            db_from_config = DBFromConfig(self.config_info)

        self.assertEqual(db_from_config.config_info.security_types, [])

    def test_securities_map_property(self):
        """Test the securities_map property returns the correct mapping."""
        securities_map = self.db_from_config.securities_map

        # Check the keys
        self.assertIn("STK", securities_map)
        self.assertIn("ETF", securities_map)
        self.assertIn("FUT", securities_map)
        self.assertIn("FOREX", securities_map)
        self.assertIn("FUND", securities_map)

        # Check the values are the correct strategy classes
        self.assertEqual(securities_map["STK"], strats.StocksMetadata)
        self.assertEqual(securities_map["ETF"], strats.ETFMetadata)
        self.assertEqual(securities_map["FUT"], strats.FuturesMetadata)
        self.assertEqual(securities_map["FOREX"], strats.ForexMetadata)
        self.assertEqual(securities_map["FUND"], strats.MutualFundsMetadata)

    @patch("saft_data_mgmt.Utils.db_strategies.ToIntStrategy")
    def test_create_historical_prices_to_int(self, mock_to_int_strategy):
        """Test creating historical prices tables with to_int_flag=True."""
        # Setup mock
        mock_strategy_instance = MagicMock()
        mock_to_int_strategy.return_value = mock_strategy_instance

        # Call the method
        self.db_from_config.create_historical_prices()

        # Verify the correct strategy was used
        mock_to_int_strategy.assert_called_once_with(self.config_info)
        mock_strategy_instance.create_historical_prices_tables.assert_called_once()

        # Verify logs
        self.mock_logger.info.assert_has_calls(
            [
                call("Creating historical prices tables"),
                call("Historical prices tables created"),
            ]
        )

    @patch("saft_data_mgmt.Utils.db_strategies.RealStrategy")
    def test_create_historical_prices_real(self, mock_real_strategy):
        """Test creating historical prices tables with to_int_flag=False."""
        # Change config
        self.config_info.to_int_flag = False

        # Setup mock
        mock_strategy_instance = MagicMock()
        mock_real_strategy.return_value = mock_strategy_instance

        # Call the method
        self.db_from_config.create_historical_prices()

        # Verify the correct strategy was used
        mock_real_strategy.assert_called_once_with(self.config_info)
        mock_strategy_instance.create_historical_prices_tables.assert_called_once()

    @patch("saft_data_mgmt.Utils.db_strategies.CoreTables")
    @patch("saft_data_mgmt.Utils.db_strategies.PortfolioDBTables")
    def test_create_config_tables_all_flags(
        self, mock_portfolio_tables, mock_core_tables
    ):
        """Test create_config_tables with all flags enabled."""
        # Setup mocks
        mock_core_instance = MagicMock()
        mock_portfolio_instance = MagicMock()
        mock_core_tables.return_value = mock_core_instance
        mock_portfolio_tables.return_value = mock_portfolio_instance

        # Setup mock for create_metadata_tables and create_historical_prices
        with (
            patch.object(
                self.db_from_config, "create_metadata_tables"
            ) as mock_create_metadata,
            patch.object(
                self.db_from_config, "create_historical_prices"
            ) as mock_create_historical,
        ):
            # Call the method
            self.db_from_config.create_config_tables()

        # Verify correct methods were called
        mock_core_tables.assert_called_once_with(self.config_info)
        mock_core_instance.create_core_tables.assert_called_once()
        mock_create_metadata.assert_called_once()
        mock_create_historical.assert_called_once()
        mock_portfolio_tables.assert_called_once_with(self.config_info)
        mock_portfolio_instance.create_portfolio_tables.assert_called_once()

        # Verify logs
        self.mock_logger.info.assert_has_calls(
            [
                call("Creating tables"),
                call("Core tables created"),
                call("Market data tables created"),
                call("Portfolio tables created"),
                call("All tables created"),
            ]
        )

    @patch("saft_data_mgmt.Utils.db_strategies.CoreTables")
    def test_create_config_tables_no_market_data(self, mock_core_tables):
        """Test create_config_tables with market_data_flag disabled."""
        # Change config
        self.config_info.market_data_flag = False

        # Setup mocks
        mock_core_instance = MagicMock()
        mock_core_tables.return_value = mock_core_instance

        # Setup mock for create_metadata_tables and create_historical_prices
        with (
            patch.object(
                self.db_from_config, "create_metadata_tables"
            ) as mock_create_metadata,
            patch.object(
                self.db_from_config, "create_historical_prices"
            ) as mock_create_historical,
            patch("saft_data_mgmt.Utils.db_strategies.PortfolioDBTables") as mock_portfolio_tables,
        ):
            mock_portfolio_instance = MagicMock()
            mock_portfolio_tables.return_value = mock_portfolio_instance

            # Call the method
            self.db_from_config.create_config_tables()

        # Verify correct methods were called
        mock_create_metadata.assert_not_called()
        mock_create_historical.assert_not_called()
        mock_portfolio_tables.assert_called_once()

        # Verify logs don't include market data logs
        self.mock_logger.info.assert_has_calls(
            [
                call("Creating tables"),
                call("Core tables created"),
                call("Portfolio tables created"),
                call("All tables created"),
            ]
        )

    @patch("saft_data_mgmt.Utils.db_strategies.CoreTables")
    def test_create_config_tables_no_portfolio_data(self, mock_core_tables):
        """Test create_config_tables with portfolio_data_flag disabled."""
        # Change config
        self.config_info.portfolio_data_flag = False

        # Setup mocks
        mock_core_instance = MagicMock()
        mock_core_tables.return_value = mock_core_instance

        # Setup mock for create_metadata_tables and create_historical_prices
        with (
            patch.object(
                self.db_from_config, "create_metadata_tables"
            ) as mock_create_metadata, #pylint: disable=unused-variable  # noqa: F841
            patch.object(
                self.db_from_config, "create_historical_prices"
            ) as mock_create_historical, #pylint: disable=unused-variable  # noqa: F841
            patch("saft_data_mgmt.Utils.db_strategies.PortfolioDBTables") as mock_portfolio_tables,
        ):
            # Call the method
            self.db_from_config.create_config_tables()

        # Verify portfolio tables not created
        mock_portfolio_tables.assert_not_called()

        # Verify logs don't include portfolio data logs
        self.mock_logger.info.assert_has_calls(
            [
                call("Creating tables"),
                call("Core tables created"),
                call("Market data tables created"),
                call("All tables created"),
            ]
        )
