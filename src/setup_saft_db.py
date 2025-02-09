"""This module provides the functionality for implementing a new SAFT DB schema at the users location"""
from src.Utils import cli_tool
from src.Utils import db_from_config

def setup_saft_db():
    """Creates a new database using a SAFT schema through the CLI"""
    config_file = cli_tool.generate_config()
    db_from_config.DBFromConfig(config_file).initialize_db()

if __name__ == "__main__":
    setup_saft_db()
