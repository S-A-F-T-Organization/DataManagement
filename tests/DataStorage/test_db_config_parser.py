import unittest
import yaml
from unittest.mock import mock_open, patch

# Adjust the import as needed to point to where DBConfigParser is defined.
from core.DataStorage.Utils.config_parser import DBConfigParser


class TestDBConfigParser(unittest.TestCase):
    def setUp(self):
        # A valid YAML configuration that covers all required keys.
        self.valid_yaml = """
schemas:
  market_data: true
  convert_price_to_int: false
  ohlcv: true
  quotes: false
database:
  dialect: sqlite
  mkt_data_db_path: "mkt_data.db"
  portfolio_data_db_path: "portfolio_data.db"
security_types:
  - " stk "
  - " etf"
seed_data:
  - " seed1 "
  - "seed2"
""".strip()

        # Patch the built-in open so that when DBConfigParser reads a file it gets our YAML.
        self.patcher = patch("builtins.open", mock_open(read_data=self.valid_yaml))
        self.mock_open = self.patcher.start()
        self.addCleanup(self.patcher.stop)

        # Create an instance using our “valid” configuration.
        self.config_parser = DBConfigParser("dummy_path.yml")

    def test_valid_config(self):
        # Compare the parsed YAML to what we expect.
        expected_config = yaml.safe_load(self.valid_yaml)
        self.assertEqual(self.config_parser.config_data, expected_config)

        # Test that parse_schema_info sets the expected flags.
        schema_info = self.config_parser.parse_schema_info()
        self.assertEqual(schema_info, expected_config['schemas'])
        self.assertTrue(self.config_parser.market_data_flag)
        self.assertTrue(self.config_parser.portfolio_data_flag)
        self.assertFalse(self.config_parser.to_int_flag)
        self.assertTrue(self.config_parser.ohlcv_flag)
        self.assertFalse(self.config_parser.quotes_flag)

        # Test that parse_db_info sets the expected database attributes.
        db_info = self.config_parser.parse_db_info()
        self.assertEqual(db_info, expected_config['database'])
        self.assertEqual(self.config_parser.db_dialect, expected_config['database']['dialect'])
        self.assertEqual(self.config_parser.mkt_data_db_path, expected_config['database']['mkt_data_db_path'])
        self.assertEqual(self.config_parser.portfolio_data_db_path, expected_config['database']['portfolio_data_db_path'])

        # Test that parse_list_info retrieves the lists as expected.
        self.config_parser.parse_list_info()
        self.assertEqual(self.config_parser.security_types, expected_config['security_types'])
        self.assertEqual(self.config_parser.seed_data, expected_config['seed_data'])

    def test_missing_config(self):
        # Simulate a FileNotFoundError when trying to open a non-existent file.
        with patch("builtins.open", side_effect=FileNotFoundError):
            with self.assertRaises(FileNotFoundError):
                DBConfigParser("non_existent_config.yml")

    def test_parse_schema(self):
        # Use the instance from setUp.
        schema_info = self.config_parser.parse_schema_info()
        expected_schema = yaml.safe_load(self.valid_yaml)['schemas']
        self.assertEqual(schema_info, expected_schema)
        self.assertEqual(self.config_parser.market_data_flag, expected_schema['market_data'])
        self.assertEqual(self.config_parser.portfolio_data_flag, expected_schema['market_data'])
        self.assertEqual(self.config_parser.to_int_flag, expected_schema['convert_price_to_int'])
        self.assertEqual(self.config_parser.ohlcv_flag, expected_schema['ohlcv'])
        self.assertEqual(self.config_parser.quotes_flag, expected_schema['quotes'])

    def test_parse_db_info(self):
        db_info = self.config_parser.parse_db_info()
        expected_db_info = yaml.safe_load(self.valid_yaml)['database']
        self.assertEqual(db_info, expected_db_info)
        self.assertEqual(self.config_parser.db_dialect, expected_db_info['dialect'])
        self.assertEqual(self.config_parser.mkt_data_db_path, expected_db_info['mkt_data_db_path'])
        self.assertEqual(self.config_parser.portfolio_data_db_path, expected_db_info['portfolio_data_db_path'])

    def test_normalize_sec_types(self):
        self.config_parser.parse_list_info()
        # Before normalization, the security types still have extra whitespace.
        self.assertEqual(self.config_parser.security_types, [" stk ", " etf"])
        self.config_parser.normalize_sec_types()
        # After normalization they should be stripped and uppercase.
        self.assertEqual(self.config_parser.security_types, ["STK", "ETF"])

    def test_normalize_seed_data(self):
        self.config_parser.parse_list_info()
        self.assertEqual(self.config_parser.seed_data, [" seed1 ", "seed2"])
        self.config_parser.normalize_seed_data()
        self.assertEqual(self.config_parser.seed_data, ["SEED1", "SEED2"])

    def test_schema_checks(self):
        # First, with our valid configuration the checks should pass (i.e. no warning is raised)
        self.config_parser.parse_schema_info()
        try:
            self.config_parser.schema_checks()
        except UserWarning:
            self.fail("schema_checks raised UserWarning unexpectedly with valid settings")

        # Now simulate a configuration where quotes_flag is True.
        yaml_quotes_true = """
schemas:
  market_data: true
  convert_price_to_int: false
  ohlcv: true
  quotes: true
database:
  dialect: sqlite
  mkt_data_db_path: "mkt_data.db"
  portfolio_data_db_path: "portfolio_data.db"
security_types:
  - "STK"
seed_data:
  - "SEED1"
        """.strip()
        with patch("builtins.open", mock_open(read_data=yaml_quotes_true)):
          parser_q = DBConfigParser("dummy.yml")
          parser_q.parse_schema_info()
          with self.assertWarns(UserWarning) as context:
              parser_q.schema_checks()
          self.assertIn("Quote level data is not currently supported", str(context.warning))


        # Simulate a configuration where convert_price_to_int is True (with quotes False).
        yaml_to_int_true = """
schemas:
  market_data: true
  convert_price_to_int: true
  ohlcv: true
  quotes: false
database:
  dialect: sqlite
  mkt_data_db_path: "mkt_data.db"
  portfolio_data_db_path: "portfolio_data.db"
security_types:
  - "STK"
seed_data:
  - "SEED1"
        """.strip()
        with patch("builtins.open", mock_open(read_data=yaml_to_int_true)):
          parser_q = DBConfigParser("dummy.yml")
          parser_q.parse_schema_info()
          with self.assertWarns(UserWarning) as context:
              parser_q.schema_checks()
          self.assertIn("True is set to `True`", str(context.warning))

    def test_db_checks(self):
        # First, with valid configuration, db_info_checks should not raise.
        self.config_parser.parse_db_info()
        try:
            self.config_parser.db_info_checks()
        except Exception as e:
            self.fail(f"db_info_checks raised an exception unexpectedly: {e}")

        # Now simulate an invalid configuration (dialect not supported).
        yaml_invalid_db = """
schemas:
  market_data: true
  convert_price_to_int: false
  ohlcv: true
  quotes: false
database:
  dialect: postgres
  mkt_data_db_path: "mkt_data.db"
  portfolio_data_db_path: "portfolio_data.db"
security_types:
  - "STK"
seed_data:
  - "SEED1"
        """.strip()
        with patch("builtins.open", mock_open(read_data=yaml_invalid_db)):
            parser_invalid = DBConfigParser("dummy.yml")
            parser_invalid.parse_db_info()
            with self.assertRaises(ValueError) as context:
                parser_invalid.db_info_checks()
            self.assertIn("We currently only offer support for SQLite", str(context.exception))

    def test_sec_type_checks(self):
        # With valid security types (after normalization) the check should pass.
        self.config_parser.parse_list_info()
        self.config_parser.normalize_sec_types()
        try:
            self.config_parser.sec_type_checks()
        except Exception as e:
            self.fail(f"sec_type_checks raised an exception unexpectedly for valid types: {e}")

        # Now simulate a configuration with a security type from the “future” list (e.g. "OPT").
        yaml_future_sec = """
schemas:
  market_data: true
  convert_price_to_int: false
  ohlcv: true
  quotes: false
database:
  dialect: sqlite
  mkt_data_db_path: "mkt_data.db"
  portfolio_data_db_path: "portfolio_data.db"
security_types:
  - "OPT"
seed_data:
  - "SEED1"
        """.strip()
        with patch("builtins.open", mock_open(read_data=yaml_future_sec)):
            parser_future = DBConfigParser("dummy.yml")
            parser_future.parse_list_info()
            parser_future.normalize_sec_types()
            with self.assertRaises(ValueError) as context:
                parser_future.sec_type_checks()
            self.assertIn("do not offer support for the security type", str(context.exception))

        # And simulate a configuration with an unrecognized security type.
        yaml_unrecognized = """
schemas:
  market_data: true
  convert_price_to_int: false
  ohlcv: true
  quotes: false
database:
  dialect: sqlite
  mkt_data_db_path: "mkt_data.db"
  portfolio_data_db_path: "portfolio_data.db"
security_types:
  - "XYZ"
seed_data:
  - "SEED1"
        """.strip()
        with patch("builtins.open", mock_open(read_data=yaml_unrecognized)):
            parser_unrec = DBConfigParser("dummy.yml")
            parser_unrec.parse_list_info()
            parser_unrec.normalize_sec_types()
            with self.assertRaises(ValueError) as context:
                parser_unrec.sec_type_checks()
            self.assertIn("Unrecognized security type", str(context.exception))

    def test_seed_data_checks(self):
        # Since seed_data_checks() is currently a pass (no-op), simply ensure it runs without error.
        try:
            self.config_parser.seed_data_checks()
        except Exception as e:
            self.fail(f"seed_data_checks raised an exception unexpectedly: {e}")


if __name__ == '__main__':
    unittest.main()
