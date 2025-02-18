"""This module sets up the core scripts according to user preferences."""

import os

from sqlalchemy import Engine

from src.Utils.configurator import ConfigInfo
from src.Utils.helpers import create_table, initalize_db_engine


class CoreTables:
    """Creates the core tables according to users preferenecs."""

    def __init__(self, config_info: ConfigInfo):
        self.config_info = config_info
        self.core_folder = "src/SQLTables/Core"
        self.first_scripts = [
            "security_exchange.sql",
            "security_types.sql"
            ]

    @property
    def db_engine(self) -> Engine:
        """The SQLAlchemy engine for the database."""
        db_engine = initalize_db_engine(self.config_info.db_path, self.config_info.db_dialect)
        return db_engine

    @property
    def sec_info_script(self) -> str:
        """This gets the script to create the SecuritiesInfo table."""
        if self.config_info.to_int_flag:
            return "securities_info_int.sql"
        return "securities_info.sql"

    def create_core_tables(self) -> None:
        """Creates the core tables."""

        for script in self.first_scripts:
            full_path = os.path.join(self.core_folder, script)
            create_table(db_engine=self.db_engine, full_path=full_path)

        full_sec_info = os.path.join(self.core_folder, self.sec_info_script)
        create_table(db_engine=self.db_engine, full_path=full_sec_info)
