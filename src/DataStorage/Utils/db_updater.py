from src.Utils.helpers import DataMgmtHelpers as dmh


class DBUpdater:

    """
    This class is in charge of updating existing SAFT databases

    - If the table doesn't exist: No issue
    - If the table does exist: Need to find differences, prompt user to update or refuse to
    """
    def __init__(self):
        self.logger = dmh.setup_log_to_console()
    
