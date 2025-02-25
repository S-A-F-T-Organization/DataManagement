"""Tests for the CLI Tool module."""

import unittest
from unittest.mock import patch
import warnings
from src.Utils.cli_tool import CLITool
from src.Utils.config_info import ConfigInfo
from src.Utils.cli_checks import check_yes_or_no, check_dialect


class TestCLITool(unittest.TestCase):
    """Tests for the CLITool class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.cli_tool = CLITool()

    def test_init(self):
        """Test initialization of CLITool."""
        self.assertIsInstance(self.cli_tool.config_info, ConfigInfo)

    def test_sql_info_questions(self):
        """Test the sql_info_questions property."""
        questions = self.cli_tool.sql_info_questions

        # Check that we have the right number of questions
        self.assertEqual(len(questions), 3)

        # Check each question has the required fields
        for q in questions:
            self.assertIn("q_text", q)
            self.assertIn("cleaning_func", q)
            self.assertIn("check_func", q)
            self.assertIn("corresponding_attribute", q)

        # Check specific values for the first question
        self.assertEqual(questions[0]["corresponding_attribute"], "db_dialect")
        self.assertEqual(questions[0]["check_func"], check_dialect)

        # Check the cleaning function works as expected
        self.assertEqual(questions[0]["cleaning_func"](" SQLITE "), "sqlite")

    def test_initial_flags_questions(self):
        """Test the initial_flags_questions property."""
        questions = self.cli_tool.initial_flags_questions

        # Check that we have the right number of questions
        self.assertEqual(len(questions), 2)

        # Check each question has the required fields
        for q in questions:
            self.assertIn("q_text", q)
            self.assertIn("cleaning_func", q)
            self.assertIn("check_func", q)
            self.assertIn("corresponding_attribute", q)

        # Check specific values
        self.assertEqual(questions[0]["corresponding_attribute"], "market_data_flag")
        self.assertEqual(questions[0]["check_func"], check_yes_or_no)

        # Check the cleaning function works as expected
        self.assertEqual(questions[0]["cleaning_func"](" Y "), "y")

    def test_mkt_data_q_list(self):
        """Test the mkt_data_q_list property."""
        questions = self.cli_tool.mkt_data_q_list

        # Check that we have the right number of questions
        self.assertEqual(len(questions), 4)

        # Check each question has the required fields
        for q in questions:
            self.assertIn("q_text", q)
            self.assertIn("cleaning_func", q)
            self.assertIn("check_func", q)
            self.assertIn("corresponding_attribute", q)

        # Check specific values
        self.assertEqual(questions[0]["corresponding_attribute"], "to_int_flag")

        # Check the cleaning function works as expected
        self.assertEqual(questions[0]["cleaning_func"](" Y "), "y")

        # Test the securities cleaning function
        securities_cleaning = questions[3]["cleaning_func"]
        self.assertEqual(
            securities_cleaning("Stocks, ETFs, Forex"), ["Stocks", "ETFs", "Forex"]
        )

    def test_quotes_questions(self):
        """Test the quotes_questions property."""
        questions = self.cli_tool.quotes_questions

        # Check that we have the right number of questions
        self.assertEqual(len(questions), 1)

        # Check the question has the required fields
        q = questions[0]
        self.assertIn("q_text", q)
        self.assertIn("cleaning_func", q)
        self.assertIn("check_func", q)
        self.assertIn("corresponding_attribute", q)

        # Check specific values
        self.assertEqual(q["corresponding_attribute"], "full_quotes_flag")

        # Check the cleaning function works as expected
        self.assertEqual(q["cleaning_func"](" Full "), "full")

    def test_get_prev_question_index_valid(self):
        """Test getting the previous question index when a previous question exists."""
        questions = self.cli_tool.sql_info_questions
        current_index = 2

        # When we have a valid previous question
        prev_index, returned_group = self.cli_tool.get_prev_question_index(
            current_index, questions
        )

        self.assertEqual(prev_index, 1)
        self.assertEqual(returned_group, questions)

    def test_get_prev_question_index_first_question(self):
        """Test getting the previous question index when on the first question."""
        questions = self.cli_tool.sql_info_questions
        current_index = 0

        # When we're on the first question, should return the same index
        with patch("builtins.print") as mock_print:
            prev_index, returned_group = self.cli_tool.get_prev_question_index(
                current_index, questions
            )
            mock_print.assert_called_with("There are no other previous questions")

        self.assertEqual(prev_index, 0)
        self.assertEqual(returned_group, questions)

    def test_get_question_info_valid(self):
        """Test getting question info for a valid question."""
        q_group = [
            {
                "q_text": "Test question?",
                "cleaning_func": lambda s: s.strip().lower(),
                "check_func": check_yes_or_no,
                "corresponding_attribute": "test_attr",
            }
        ]

        q_text, cleaning_func, check_func, attr_name = self.cli_tool.get_question_info(
            q_group, 0
        )

        self.assertEqual(q_text, "Test question?")
        self.assertEqual(cleaning_func("  tEst  "), "test")
        self.assertEqual(check_func, check_yes_or_no)
        self.assertEqual(attr_name, "test_attr")

    def test_get_question_info_missing_fields(self):
        """Test getting question info when fields are missing."""
        # Missing cleaning_func field
        q_group = [
            {
                "q_text": "Test question?",
                "check_func": check_yes_or_no,
                "corresponding_attribute": "test_attr",
            }
        ]

        q_text, cleaning_func, check_func, attr_name = self.cli_tool.get_question_info(
            q_group, 0
        )

        self.assertEqual(q_text, "Test question?")
        self.assertIsNone(cleaning_func)
        self.assertEqual(check_func, check_yes_or_no)
        self.assertEqual(attr_name, "test_attr")

    @patch("builtins.input", return_value="sqlite")
    def test_q_builder_success(self, mock_input):  # pylint: disable=unused-argument
        """Test q_builder with successful input."""
        q_group = [
            {
                "q_text": "What SQL dialect?",
                "cleaning_func": lambda s: s.strip(),
                "check_func": lambda x: None,  # Mock check function that always succeeds
                "corresponding_attribute": "db_dialect",
            }
        ]

        new_index, returned_group = self.cli_tool.q_builder(0, q_group)

        # Should increment the index and return the same group
        self.assertEqual(new_index, 1)
        self.assertEqual(returned_group, q_group)
        self.assertEqual(self.cli_tool.config_info.db_dialect, "sqlite")

    @patch("builtins.input", return_value="test_name")
    def test_q_builder_with_warning(self, mock_input):  # pylint: disable=unused-argument
        """Test q_builder when check_func returns a modified value with warning."""

        def mock_check_func(val):
            warnings.warn("Adding .db extension")
            return val + ".db"

        q_group = [
            {
                "q_text": "DB name?",
                "cleaning_func": lambda s: s.strip(),
                "check_func": mock_check_func,
                "corresponding_attribute": "db_name",
            }
        ]

        with warnings.catch_warnings(record=True):
            new_index, returned_group = self.cli_tool.q_builder(0, q_group)

        # Should increment the index and update the value
        self.assertEqual(new_index, 1)
        self.assertEqual(returned_group, q_group)
        self.assertEqual(self.cli_tool.config_info.db_name, "test_name.db")

    @patch("builtins.input", return_value="invalid")
    def test_q_builder_with_error(self, mock_input):  # pylint: disable=unused-argument
        """Test q_builder when check_func raises a ValueError."""

        def mock_check_func(val):
            raise ValueError("Invalid input")

        q_group = [
            {
                "q_text": "Question?",
                "cleaning_func": lambda s: s.strip(),
                "check_func": mock_check_func,
                "corresponding_attribute": "db_dialect",
            }
        ]

        with patch("builtins.print") as mock_print:
            new_index, returned_group = self.cli_tool.q_builder(0, q_group)
            mock_print.assert_called_with("Invalid input")

        # Should not increment the index
        self.assertEqual(new_index, 0)
        self.assertEqual(returned_group, q_group)

    @patch("builtins.input", return_value="^Z")
    def test_q_builder_with_ctrl_z(self, mock_input):  # pylint: disable=unused-argument
        """Test q_builder when user enters Ctrl+Z to go back."""
        q_group = self.cli_tool.sql_info_questions

        # Mock get_prev_question_index to return a specific value
        with patch.object(
            self.cli_tool, "get_prev_question_index", return_value=(0, q_group)
        ) as mock_prev:
            new_index, returned_group = self.cli_tool.q_builder(1, q_group)
            mock_prev.assert_called_once_with(1, q_group)

        # Should return the previous index
        self.assertEqual(new_index, 0)
        self.assertEqual(returned_group, q_group)

    @patch("builtins.input", return_value="invalid")
    def test_q_builder_with_unexpected_error(self, mock_input):  # pylint: disable=unused-argument
        """Test q_builder when check_func raises a ValueError."""

        def mock_check_func(val):
            raise Exception("A random exception")  # pylint: disable=broad-exception-raised

        q_group = [
            {
                "q_text": "Question?",
                "cleaning_func": lambda s: s.strip(),
                "check_func": mock_check_func,
                "corresponding_attribute": "db_dialect",
            }
        ]

        with patch("builtins.print") as mock_print:
            new_index, returned_group = self.cli_tool.q_builder(0, q_group)
            mock_print.assert_called_with(
                "An unexpected error occurred: A random exception"
            )

        # Should not increment the index
        self.assertEqual(new_index, 0)
        self.assertEqual(returned_group, q_group)

    @patch("builtins.input", side_effect=KeyboardInterrupt)
    def test_q_builder_keyboard_interrupt(self, mock_input):  # pylint: disable=unused-argument
        """Test q_builder when a KeyboardInterrupt occurs."""
        q_group = [
            {
                "q_text": "Question?",
                "cleaning_func": lambda s: s.strip(),
                "check_func": lambda x: None,
                "corresponding_attribute": "db_dialect",
            }
        ]

        with patch("builtins.print") as mock_print:
            result = self.cli_tool.q_builder(0, q_group)
            mock_print.assert_called_with(
                "Keyboard interrupt occurred, closing CLI tool..."
            )

        # Should return None when KeyboardInterrupt occurs
        self.assertIsNone(result)

    def test_generate_config_info_basic(self):
        """Test generate_config_info with basic flow."""
        # Set up a sequence of mock inputs
        input_sequence = ["sqlite", "/path/to/db", "test.db", "n", "n"]

        with patch("builtins.input", side_effect=input_sequence):
            # Patch the q_builder method to simply advance the index
            with patch.object(
                self.cli_tool, "q_builder", side_effect=lambda idx, grp: (idx + 1, grp)
            ):
                config = self.cli_tool.generate_config_info()

        # Check that we get a ConfigInfo object back
        self.assertIsInstance(config, ConfigInfo)

    def test_generate_config_info_complete(self):
        """Test generate_config_info with complete flow including market data and quotes."""
        # Create a new CLI Tool instance with fresh config
        self.cli_tool = CLITool()

        # Setup the config values we want to test
        self.cli_tool.config_info.db_dialect = "sqlite"
        self.cli_tool.config_info.db_path = "/path"
        self.cli_tool.config_info.db_name = "test.db"
        self.cli_tool.config_info.market_data_flag = True
        self.cli_tool.config_info.portfolio_data_flag = False
        self.cli_tool.config_info.to_int_flag = True
        self.cli_tool.config_info.ohlcv_flag = True
        self.cli_tool.config_info.quotes_flag = True
        self.cli_tool.config_info.security_types = ["stocks"]
        self.cli_tool.config_info.full_quotes_flag = True

        # Create a simple mock that just returns the next index
        def mock_q_builder(q_index, q_group):
            return q_index + 1, q_group

        # Patch the q_builder method
        with patch.object(self.cli_tool, "q_builder", side_effect=mock_q_builder):
            config = self.cli_tool.generate_config_info()

        # Verify configuration was set correctly
        self.assertEqual(config.db_dialect, "sqlite")
        self.assertEqual(config.db_path, "/path")
        self.assertEqual(config.db_name, "test.db")
        self.assertTrue(config.market_data_flag)
        self.assertFalse(config.portfolio_data_flag)
        self.assertTrue(config.to_int_flag)
        self.assertTrue(config.ohlcv_flag)
        self.assertTrue(config.quotes_flag)
        self.assertTrue(config.full_quotes_flag)
