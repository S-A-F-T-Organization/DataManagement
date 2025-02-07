""" This module will handle all of the updating functions if someone has an existing database """
from src.Utils.helpers import DataMgmtHelpers as dmh


class DBUpdater:

    """
    This class is in charge of updating existing SAFT databases

    - If the table doesn't exist: No issue
    - If the table does exist: Need to find differences, prompt user to update or refuse to
    """
    def __init__(self):
        self.logger = dmh.setup_log_to_console()

    def update(self):
        """
        _summary_
        """
        pass

    def more_update(self):
        """
        _summary_
        """
        pass
