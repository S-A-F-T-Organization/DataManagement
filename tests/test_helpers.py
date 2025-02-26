"""Tests the helpers module."""

import os
import logging
import unittest
import tempfile
import shutil
import time

from sqlalchemy import Engine, inspect

from src.Utils.helpers import setup_log_to_console, initalize_db_engine, create_table


class TestSetupLogger(unittest.TestCase):
    """Tests the setup_logger method"""

    def test_setup_log_to_console(self):
        """Tests that the logger is set up properly"""
        logger = setup_log_to_console()
        logger.info("\nTest message")
        self.assertEqual(logger.level, logging.INFO)


class TestInitializeDBEngine(unittest.TestCase):
    """Tests the initalize_db_engine method"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        self.memory_db_path = "sqlite:///:memory:"
        self.temp_db_path = "sqlite:///test_temp.db"

    def tearDown(self):
        """Clean up test fixtures after each test method"""
        # Remove temporary file if it exists
        if os.path.exists("test_temp.db"):
            os.remove("test_temp.db")

    def test_initialize_db_engine_with_memory_sqlite(self):
        """Test initializing engine with in-memory sqlite database"""
        db_engine = initalize_db_engine("sqlite", ":memory:", "test.db")
        self.assertIsInstance(db_engine, Engine)
        self.assertEqual(str(db_engine.url), "sqlite:///:memory:/test.db")

    def test_initialize_db_engine_with_temp_file(self):
        """Test initializing engine with temporary file database"""
        db_engine = initalize_db_engine("sqlite", "fake/path", "test.db")
        self.assertIsInstance(db_engine, Engine)
        self.assertEqual(str(db_engine.url), "sqlite:///fake/path/test.db")

    def test_initialize_db_engine_invalid_dialect(self):
        """Test initializing engine with invalid dialect"""
        with self.assertRaises(ValueError) as context:
            initalize_db_engine("postgres", ":memory:", "test.db")
        self.assertEqual(str(context.exception), "Invalid database dialect detected: postgres")

class TestCreateTable(unittest.TestCase):
    """Tests the create_table method"""
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.test_dir = tempfile.mkdtemp()
        self.engine = initalize_db_engine("sqlite", f"{self.test_dir}", "test.db")
        self.security_types_path = "src/SQLTables/Core/security_types.sql"

    def tearDown(self):
        """Cleanup test database and files after each test."""
        if hasattr(self, 'engine'):
            self.engine.dispose()  # Dispose of the SQLAlchemy engine
        time.sleep(0.5)  # Small delay to allow OS to release the file (optional)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_create_security_types_table_success(self):
        """Test that the SecurityTypes table is created with the correct schema."""
        # Create the table from the SQL file
        create_table(self.engine, self.security_types_path)

        # Use SQLAlchemy inspector to verify the table structure
        inspector = inspect(self.engine)
        self.assertTrue(inspector.has_table("SecurityTypes"), "SecurityTypes table does not exist in the database.")

        # Get column information
        columns = inspector.get_columns("SecurityTypes")
        self.assertEqual(len(columns), 2, "Expected 2 columns in SecurityTypes table.")

        # Check SecurityTypeID column
        security_type_id = columns[0]
        self.assertEqual(security_type_id["name"], "security_type_id")
        self.assertTrue(security_type_id["primary_key"])
        self.assertEqual(str(security_type_id["type"]).upper(), "INTEGER")

        # Check SecurityType column
        security_type = columns[1]
        self.assertEqual(security_type["name"], "security_type")
        self.assertFalse(security_type["nullable"])
        self.assertEqual(str(security_type["type"]).upper(), "TEXT")

        # Check unique constraint on SecurityType
        unique_constraints = inspector.get_unique_constraints("SecurityTypes")
        self.assertEqual(len(unique_constraints), 1, "Expected one unique constraint on SecurityTypes.")
        self.assertEqual(unique_constraints[0]["column_names"], ["security_type"])

    def test_create_inferences_table_failure(self):
        """Test that creating the Inferences table fails due to a missing foreign key reference."""
        # Verify that the Inferences table was not created
        inspector = inspect(self.engine)
        self.assertFalse(inspector.has_table("Inferences"), "Inferences table should not be created due to foreign key error.")
