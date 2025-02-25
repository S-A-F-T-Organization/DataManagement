"""This module contains all of the functions for checking the configuration info."""

import warnings
from typing import Union

def check_dialect(response: str) -> None:
    """
    Check if the SQL dialect is valid.

    Args:
        config_info (ConfigInfo): The configuration info object.

    Raises:
        ValueError: If the dialect is not supported.
    """
    if response not in ["sqlite", "sqlite3"]:
        raise ValueError(
            "Invalid SQL dialect. Please try again."
            "We currently only offer support for SQLite (try 'sqlite' or 'sqlite3'). "
            "PostgreSQL support is coming soon!"
        )


def check_db_path(response: str) -> None:
    """
    Check if the database path is valid. A valid path:
    1. cannot be empty
    2. cannot be None
    3. cannot end in .db
    4. must be a string
    5. cannot end in a slash

    Args:
        config_info (ConfigInfo): The configuration info object.

    Raises:
        ValueError: If path is not valid
    """
    if not isinstance(response, str):
        raise ValueError(
            f"Invalid database path, expected a string but received response of type {type(response)}. Please try again."
        )
    if not response:
        raise ValueError(
            "Invalid database path, expected a string but received None. Please try again."
        )
    if response.endswith(".db"):
        raise ValueError(
            "Invalid database path, path should not end in .db. Please try again."
        )
    if response.endswith("/"):
        raise ValueError(
            "Invalid database path, path should not end in a slash. Please try again."
        )

def check_db_name(response: str) -> Union[str, None]:
    """Check if the database name is valid
    1. cannot be empty
    2. cannot be None
    3. must end in .db
    4. must be a string

    Args:
        config_info (ConfigInfo): The configuration info object.

    Raises:
        ValueError: If path is not valid
        Warning: If name does not end in .db
        ValueError: If name is not a string
        ValueError: If name is empty
    """
    if not response:
        raise ValueError(
            "Invalid database name, expected a string but received None. Please try again."
        )
    if not isinstance(response, str):
        raise ValueError(
            f"Invalid database name, expected a string but received response of type {type(response)}. Please try again."
        )
    if not response.endswith(".db"):
        db_name = response + ".db"
        warnings.warn(
            "Database name should end in .db. This has been automatically appended to the name."
        )
        return db_name
    return None


def check_yes_or_no(response: str) -> None:
    """
    Check if the user's response to the market data schema question is valid.
    Valid responses are:
    1. 'Y' or 'N' in either upper or lower case

    Args:
        marked_data_response (str): The user's response to the market data schema question.

    Raises:
        ValueError: If the response is not 'Y' or 'N'.
    """
    if response not in ["Y", "N", "y", "n"]:
        raise ValueError("Invalid response. Please enter 'Y' or 'N'.")


def check_security_types(response: list[str]) -> None:
    """
    Check if the security types are valid.
    Supported security types: ['Stocks', 'ETFs', 'Forex', 'Futures']

    Args:
        config_info (ConfigInfo): The configuration info object.

    Raises:
        ValueError: If the security type is not supported.
    """
    supported_sec_types = ["stocks", "etfs", "forex", "futures", "fund", "all"]

    for sec_type in response:
        if sec_type not in supported_sec_types:
            raise ValueError(
                f"Unrecognized security type '{sec_type}'. Supported types: {supported_sec_types}"
            )


def check_quotes_type(response: str):
    """
    Check if the quotes type is valid.
    Supported quotes types: ['quotes', 'full_quotes']

    Args:
        config_info (ConfigInfo): The configuration info object.

    Raises:
        ValueError: If the quotes type is not supported.
    """
    supported_quotes_types = ["full", "consolidated"]
    if response not in supported_quotes_types:
        raise ValueError(
            f"Unrecognized quotes type '{response}'. Supported types: {supported_quotes_types}"
        )
