"""Unit tests for the cli_checks module."""

import unittest
import warnings
from src.Utils.cli_checks import (
    check_dialect,
    check_db_path,
    check_db_name,
    check_yes_or_no,
    check_security_types,
    check_quotes_type,
)


class TestCheckDialect(unittest.TestCase):
    """Tests for check_dialect function."""

    def test_valid_sqlite(self):
        """Test with valid 'sqlite' dialect."""
        # Should not raise an exception
        check_dialect("sqlite")

    def test_valid_sqlite3(self):
        """Test with valid 'sqlite3' dialect."""
        # Should not raise an exception
        check_dialect("sqlite3")

    def test_invalid_dialect(self):
        """Test with invalid dialects."""
        invalid_dialects = ["postgresql", "mysql", "", None, 123]

        for dialect in invalid_dialects:
            with self.subTest(dialect=dialect):
                with self.assertRaises(ValueError) as context:
                    check_dialect(dialect)
                self.assertIn("Invalid SQL dialect", str(context.exception))


class TestCheckDbPath(unittest.TestCase):
    """Tests for check_db_path function."""

    def test_valid_path(self):
        """Test with valid database paths."""
        valid_paths = ["/path/to/db", "C:\\Users\\data", "."]

        for path in valid_paths:
            with self.subTest(path=path):
                # Should not raise an exception
                check_db_path(path)

    def test_empty_path(self):
        """Test with empty path."""
        with self.assertRaises(ValueError) as context:
            check_db_path("")
        self.assertIn("Invalid database path", str(context.exception))

    def test_none_path(self):
        """Test with None path."""
        with self.assertRaises(ValueError) as context:
            check_db_path(None)
        self.assertIn("Invalid database path", str(context.exception))

    def test_path_ending_with_db(self):
        """Test with path ending in .db."""
        with self.assertRaises(ValueError) as context:
            check_db_path("/path/to/database.db")
        self.assertIn("path should not end in .db", str(context.exception))

    def test_path_ending_with_slash(self):
        """Test with path ending in slash."""
        with self.assertRaises(ValueError) as context:
            check_db_path("/path/to/directory/")
        self.assertIn("path should not end in a slash", str(context.exception))

    def test_non_string_path(self):
        """Test with non-string path."""
        with self.assertRaises(ValueError) as context:
            check_db_path(123)
        self.assertIn(
            "expected a string but received response of type <class 'int'>",
            str(context.exception),
        )


class TestCheckDbName(unittest.TestCase):
    """Tests for check_db_name function."""

    def test_valid_db_name(self):
        """Test with valid database name ending with .db."""
        # Should not modify the name and return None
        self.assertIsNone(check_db_name("database.db"))

    def test_db_name_without_extension(self):
        """Test with database name without .db extension."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = check_db_name("database")
            self.assertEqual(result, "database.db")
            self.assertEqual(len(w), 1)
            self.assertIn("automatically appended", str(w[0].message))

    def test_empty_db_name(self):
        """Test with empty database name."""
        with self.assertRaises(ValueError) as context:
            check_db_name("")
        self.assertIn("Invalid database name", str(context.exception))

    def test_none_db_name(self):
        """Test with None database name."""
        with self.assertRaises(ValueError) as context:
            check_db_name(None)
        self.assertIn("Invalid database name", str(context.exception))

    def test_non_string_db_name(self):
        """Test with non-string database name."""
        with self.assertRaises(ValueError) as context:
            check_db_name(123)
        self.assertIn(
            "expected a string but received response of type <class 'int'>",
            str(context.exception),
        )


class TestCheckYesOrNo(unittest.TestCase):
    """Tests for check_yes_or_no function."""

    def test_valid_yes_uppercase(self):
        """Test with valid 'Y' response."""
        # Should not raise an exception
        check_yes_or_no("Y")

    def test_valid_yes_lowercase(self):
        """Test with valid 'y' response."""
        # Should not raise an exception
        check_yes_or_no("y")

    def test_valid_no_uppercase(self):
        """Test with valid 'N' response."""
        # Should not raise an exception
        check_yes_or_no("N")

    def test_valid_no_lowercase(self):
        """Test with valid 'n' response."""
        # Should not raise an exception
        check_yes_or_no("n")

    def test_invalid_response(self):
        """Test with invalid responses."""
        invalid_responses = ["yes", "no", "", "maybe", None, 123]

        for response in invalid_responses:
            with self.subTest(response=response):
                with self.assertRaises(ValueError) as context:
                    check_yes_or_no(response)
                self.assertEqual(
                    "Invalid response. Please enter 'Y' or 'N'.", str(context.exception)
                )


class TestCheckSecurityTypes(unittest.TestCase):
    """Tests for check_security_types function."""

    def test_valid_single_security_type(self):
        """Test with a single valid security type."""
        valid_types = ["stocks", "etfs", "forex", "futures", "fund", "all"]

        for security_type in valid_types:
            with self.subTest(security_type=security_type):
                # Should not raise an exception
                check_security_types([security_type])

    def test_valid_multiple_security_types(self):
        """Test with multiple valid security types."""
        # Should not raise an exception
        check_security_types(["stocks", "etfs", "forex"])

    def test_invalid_security_type(self):
        """Test with invalid security types."""
        invalid_types = ["bonds", "options", "", None, 123]

        for security_type in invalid_types:
            with self.subTest(security_type=security_type):
                with self.assertRaises(ValueError) as context:
                    check_security_types(["stocks", security_type])
                self.assertIn(
                    f"Unrecognized security type '{security_type}'",
                    str(context.exception),
                )

    def test_empty_security_types(self):
        """Test with empty list of security types."""
        # Should not raise an exception (empty list means no security types)
        check_security_types([])


class TestCheckQuotesType(unittest.TestCase):
    """Tests for check_quotes_type function."""

    def test_valid_full_quotes(self):
        """Test with valid 'full' quotes type."""
        # Should not raise an exception
        check_quotes_type("full")

    def test_valid_consolidated_quotes(self):
        """Test with valid 'consolidated' quotes type."""
        # Should not raise an exception
        check_quotes_type("consolidated")

    def test_invalid_quotes_type(self):
        """Test with invalid quotes types."""
        invalid_types = ["quotes", "market_depth", "", None, 123]

        for quotes_type in invalid_types:
            with self.subTest(quotes_type=quotes_type):
                with self.assertRaises(ValueError) as context:
                    check_quotes_type(quotes_type)
                self.assertIn(
                    f"Unrecognized quotes type '{quotes_type}'", str(context.exception)
                )


if __name__ == "__main__":
    unittest.main()
