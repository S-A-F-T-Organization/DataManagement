"""This module provides the functionality for implementing a new SAFT DB schema at the users location"""
from saft_data_mgmt.Utils import cli_tool
from saft_data_mgmt.Utils import db_from_config

def main():
    """Main function to set up the SAFT database."""
    new_cli_tool = cli_tool.CLITool()
    config_info = new_cli_tool.generate_config_info()
    print(config_info)
    db_creator = db_from_config.DBFromConfig(config_info)
    db_creator.create_config_tables()
