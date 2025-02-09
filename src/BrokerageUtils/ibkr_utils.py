""" This module contains useful helper functions for IBKR"""
from ib_insync import IB
from src.Utils.helpers import DataMgmtHelpers as dmh

class IBKRUtils:

    def __init__(self):
        self.logger = dmh.setup_log_to_console()

    @staticmethod
    def ibkr_spinup(host:str = '127.0.0.1', port:int=7487, client_id:int=1):
        ib = IB()
        ib.connect(host=host, port=port, clientId=client_id)
        return ib
