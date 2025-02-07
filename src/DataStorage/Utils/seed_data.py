""" This module will handle inputting any seed data the user configured """
from sqlalchemy import Engine, text
from src.DataStorage.Utils.helpers import DataStorageHelpers as dsh
from src.Utils.helpers import DataMgmtHelpers as dmh
from src.DataStorage.Utils.config_parser import ConfigInfo

class InputSeedData:
    """
    _summary_
    """

    def __init__(self, config_info:ConfigInfo):
        self.logger = dmh.setup_log_to_console()
        self.config_info = config_info
        self.seed_data_base_path = 'core/DataStorage/SeedDataSQL'

    def create_script_list(self) -> list[str]:
        """
        _summary_

        Returns:
            list[str]: _description_
        """
        seed_data_paths = []
        for seed_data in self.config_info.seed_data:
            seed_data = seed_data.lower()
            dsh.create_script_path(self.seed_data_base_path, seed_data, 'metadata')
            seed_data_paths.append(seed_data)
        return seed_data_paths

    def input_seed_data(self, seed_data_paths:list, mkt_data_engine:Engine) -> None:
        """
        _summary_

        Args:
            seed_data_paths (list): _description_
            mkt_data_engine (Engine): _description_
        """
        with mkt_data_engine.connect() as conn:
            transact = conn.begin()
            for seed_data in seed_data_paths:
                try:
                    with open(seed_data, 'r', encoding='utf-8') as f:
                        script = f.read()
                        conn.execute(text(script))
                    transact.commit()
                except Exception:
                    transact.rollback()
                    raise
