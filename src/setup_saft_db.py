"""This module provides the functionality for implementing a new SAFT DB schema at the users location"""
from src.Utils import cli_tool
from src.Utils import db_from_config

if __name__ == "__main__":
    cli_tool = cli_tool.CLITool()
    config_info = cli_tool.generate_config_info()
    db_creator = db_from_config.DBFromConfig(config_info)
    db_creator.create_config_tables()
