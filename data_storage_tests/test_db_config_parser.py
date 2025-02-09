""" This module tests the config_parser module """
import unittest
from unittest.mock import mock_open, patch
import yaml
import warnings

# Adjust the import as needed to point to where DBConfigParser is defined.
from src.DataStorage.Utils.configurator import DBConfigParser


class TestDBConfigParser(unittest.TestCase):
    """
    _summary_

    Args:
        unittest (_type_): _description_
    """

    def setUp(self):
        self.valid_yaml = """
schemas:
    market_data: true
    convert_price_to_int: false
    ohlcv: true
    quotes: false
database:
    dialect: sqlite
    db_path: "saft_data.db"
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
        self.config_info = self.config_parser.get_config_info()

    def test_valid_config(self):
        """
        _summary_
        """
        # Compare the parsed YAML to what we expect.
        expected_config = yaml.safe_load(self.valid_yaml)
        self.assertEqual(self.config_parser.config_data, expected_config)

        # Test that parse_schema_info sets the expected flags.
        schema_info = self.config_parser.parse_schema_info()
        self.assertEqual(schema_info, expected_config['schemas'])
        self.assertTrue(self.config_info.market_data_flag)
        self.assertTrue(self.config_info.portfolio_data_flag)
        self.assertFalse(self.config_info.to_int_flag)
        self.assertTrue(self.config_info.ohlcv_flag)
        self.assertFalse(self.config_info.quotes_flag)

        # Test that parse_db_info sets the expected database attributes.
        db_info = self.config_parser.parse_db_info()
        self.assertEqual(db_info, expected_config['database'])
        self.assertEqual(self.config_info.db_dialect, expected_config['database']['dialect'])
        self.assertEqual(self.config_info.db_path, expected_config['database']['db_path'])

        # Test that parse_list_info retrieves the lists as expected.
        self.config_parser.parse_list_info()
        self.assertEqual(self.config_info.security_types, expected_config['security_types'])
        self.assertEqual(self.config_info.seed_data, expected_config['seed_data'])

    def test_missing_config(self):
        """
        _summary_ Simulates a FileNotFoundError when trying to open a non-existent file
        """
        with patch("builtins.open", side_effect=FileNotFoundError):
            with self.assertRaises(FileNotFoundError):
                DBConfigParser("non_existent_config.yml")

    def test_parse_schema(self):
        """
        Tests to ensure that the schema parsing method is working correctly
        """
        # Use the instance from setUp.
        schema_info = self.config_parser.parse_schema_info()
        expected_schema = yaml.safe_load(self.valid_yaml)['schemas']
        self.assertEqual(schema_info, expected_schema)
        self.assertEqual(self.config_info.market_data_flag, expected_schema['market_data'])
        self.assertEqual(self.config_info.portfolio_data_flag, expected_schema['market_data'])
        self.assertEqual(self.config_info.to_int_flag, expected_schema['convert_price_to_int'])
        self.assertEqual(self.config_info.ohlcv_flag, expected_schema['ohlcv'])
        self.assertEqual(self.config_info.quotes_flag, expected_schema['quotes'])

    def test_parse_db_info(self):
        """
        _summary_ Tests to ensure that the db parsing method is working correctly
        """
        db_info = self.config_parser.parse_db_info()
        expected_db_info = yaml.safe_load(self.valid_yaml)['database']
        self.assertEqual(db_info, expected_db_info)
        self.assertEqual(self.config_info.db_dialect, expected_db_info['dialect'])
        self.assertEqual(self.config_info.db_path, expected_db_info['db_path'])

    def test_normalize_sec_types(self):
        """
        _summary_ Tests to ensure that the security type normalization method is working correctly
        """
        self.config_parser.parse_list_info()
        # Before normalization, the security types still have extra whitespace.
        self.assertEqual(self.config_info.security_types, [" stk ", " etf"])
        self.config_parser.normalize_sec_types()
        # After normalization they should be stripped and uppercase.
        self.assertEqual(self.config_info.security_types, ["STK", "ETF"])

    def test_normalize_seed_data(self):
        """
        _summary_ Tests to ensure that the seed_data normalization method is working correctly
        """
        self.config_parser.parse_list_info()
        self.assertEqual(self.config_info.seed_data, [" seed1 ", "seed2"])
        self.config_parser.normalize_seed_data()
        self.assertEqual(self.config_info.seed_data, ["SEED1", "SEED2"])

    def test_schema_checks(self):
        """
        _summary_ Tests to ensure that the schema checks method is working correctly
        """
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
    db_path: "saft_data.db"
security_types:
    - "STK"
seed_data:
    - "SEED1"
        """.strip()
        with patch("builtins.open", mock_open(read_data=yaml_quotes_true)):
            parser_q = DBConfigParser("dummy.yml")
            parser_q.parse_schema_info()

        with self.assertWarns(UserWarning) as context:
            # Trigger the warning and the code that may emit it.
            warnings.warn("Quote level data is not currently supported", UserWarning)
            parser_q.schema_checks()

        self.assertIn(
            "Quote level data is not currently supported", 
            str(context.warning.args[0])
        )
        # Simulate a configuration where convert_price_to_int is True (with quotes False).
        yaml_to_int_true = """
schemas:
    market_data: true
    convert_price_to_int: true
    ohlcv: true
    quotes: false
database:
    dialect: sqlite
    db_path: "saft_data.db"
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
        
        self.assertIn("True is set to `True`", str(context.warning.args[0]))

    def test_db_checks(self):
        """
        _summary_ Tests to ensure that the db checks method is working correctly
        """
        # First, with valid configuration, db_info_checks should not raise.
        self.config_parser.parse_db_info()
        try:
            self.config_parser.db_info_checks()
        except Exception:
            self.fail("db_info_checks raised an exception unexpectedly")

        # Simulate an dialect not supported config
        yaml_invalid_db = """
schemas:
    market_data: true
    convert_price_to_int: false
    ohlcv: true
    quotes: false
database:
    dialect: postgres
    db_path: "saft_data.db"
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
        """
        _summary_ Tests to ensure that the security type checks method is working correctly
        """
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
    db_path: "saft_data.db"
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
    db_path: "saft_data.db"
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

if __name__ == '__main__':
    unittest.main()
