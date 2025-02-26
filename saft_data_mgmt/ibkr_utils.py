""" This module contains useful helper functions for IBKR"""
from typing import Callable, Any
from ib_insync import IB

def ibkr_conn_manager(host: str, port: int, client_id: int) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator factory for IBKR connection management through ib_insync.

    It takes IB connection parameters (host, port, clientID) and returns
    a decorator that wraps any function with IB connect/disconnect logic.

    Args:
        host (str): The hostname or IP address for the IB gateway/TWS.
        port (int): The port number for the IB gateway/TWS.
        clientID (int): The client ID used for the IB connection.

    Returns:
        Callable[[Callable[..., Any]], Callable[..., Any]]:
            A decorator that can wrap functions, ensuring they run within
            an active IB connection context.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            ib = IB()
            ib.connect(host=host, port=port, clientId=client_id)
            try:
                func(*args, **kwargs)
            finally:
                ib.disconnect()

        return wrapper
    return decorator
