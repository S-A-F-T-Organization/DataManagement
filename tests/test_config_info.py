"""Tests that the ConfigInfo class is initialized correctly."""

import unittest
from src.Utils.config_info import ConfigInfo

class TestConfigInfo(unittest.TestCase):
    """Tests the ConfigInfo class."""
    def test_default_values(self):
        """Test that the ConfigInfo class initializes with the correct default values."""
        config_info = ConfigInfo()
        self.assertIsNone(config_info.db_dialect)
        self.assertIsNone(config_info.db_path)
        self.assertIsNone(config_info.db_name)
        self.assertFalse(config_info.market_data_flag)
        self.assertFalse(config_info.portfolio_data_flag)
        self.assertFalse(config_info.to_int_flag)
        self.assertFalse(config_info.ohlcv_flag)
        self.assertFalse(config_info.quotes_flag)
        self.assertFalse(config_info.full_quotes_flag)
        self.assertEqual(config_info.security_types, [])
        self.assertEqual(config_info.seed_data, [])

    def test_custom_values(self):
        """Test that the ConfigInfo class can be initialized with custom values."""
        config_info = ConfigInfo(
            db_dialect="sqlite",
            db_path="test.db",
            db_name="test_db.db",
            market_data_flag=True,
            portfolio_data_flag=True,
            to_int_flag=True,
            ohlcv_flag=True,
            quotes_flag=True,
            full_quotes_flag=True,
            security_types=["stock", "etf"],
            seed_data=["security_types", "exchanges"]
        )
        self.assertEqual(config_info.db_dialect, "sqlite")
        self.assertEqual(config_info.db_path, "test.db")
        self.assertEqual(config_info.db_name, "test_db.db")
        self.assertTrue(config_info.market_data_flag)
        self.assertTrue(config_info.portfolio_data_flag)
        self.assertTrue(config_info.to_int_flag)
        self.assertTrue(config_info.ohlcv_flag)
        self.assertTrue(config_info.quotes_flag)
        self.assertTrue(config_info.full_quotes_flag)
        self.assertEqual(config_info.security_types, ["stock", "etf"])
        self.assertEqual(config_info.seed_data, ["security_types", "exchanges"])
