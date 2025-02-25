"""This module contains the CLI tool for implementing a SAFT DB schema"""

from typing import List, Callable, Any

from src.Utils.config_info import ConfigInfo
from src.Utils.cli_checks import (
    check_dialect,
    check_db_path,
    check_db_name,
    check_security_types,
    check_yes_or_no,
    check_quotes_type,
)


class CLITool:
    """Class representing the CLI tool for setting up a SAFT DB schema."""

    def __init__(self):
        self.config_info = ConfigInfo()

    @property
    def sql_info_questions(self) -> List[dict]:
        """Returns a list of SQL dialects supported by the CLI tool"""
        sql_info_list = [
            {
                "q_text": "What SQL dialect will you be using? (current support: sqlite): ",
                "cleaning_func": lambda s: s.lower().strip(),
                "check_func": check_dialect,
                "corresponding_attribute": "db_dialect",
            },
            {
                "q_text": "What is the path you would like to host this database at? (not including DB name): ",
                "cleaning_func": lambda s: s.strip(),
                "check_func": check_db_path,
                "corresponding_attribute": "db_path",
            },
            {
                "q_text": "What would you like to name this database? (should end in .db): ",
                "cleaning_func": lambda s: s,
                "check_func": check_db_name,
                "corresponding_attribute": "db_name",
            },
        ]
        return sql_info_list

    @property
    def initial_flags_questions(self) -> List[dict]:
        """Returns a list of initial flags for the CLI tool"""
        initial_flags_list = [
            ## Initial Schema Questions ##
            {
                "q_text": "Would you like to implement our `market_data` schema? [Y/N]: ",
                "cleaning_func": lambda s: s.lower().strip(),
                "check_func": check_yes_or_no,
                "corresponding_attribute": "market_data_flag",
            },
            {
                "q_text": "Would you like to implement our `portfolio_data` schema? [Y/N]: ",
                "cleaning_func": lambda s: s.lower().strip(),
                "check_func": check_yes_or_no,
                "corresponding_attribute": "portfolio_data_flag",
            },
        ]
        return initial_flags_list

    @property
    def mkt_data_q_list(self):
        """Sets the questions for the market data schema"""
        mkt_data_q_list = [
            {
                "q_text": "Would you like to store historical security prices as integers? [Y/N]: ",
                "cleaning_func": lambda s: s.lower().strip(),
                "check_func": check_yes_or_no,
                "corresponding_attribute": "to_int_flag",
            },
            {
                "q_text": "Would you like to store OHLCV data? [Y/N]: ",
                "cleaning_func": lambda s: s.lower().strip(),
                "check_func": check_yes_or_no,
                "corresponding_attribute": "ohlcv_flag",
            },
            {
                "q_text": "Would you like to store Quotes data? [Y/N]: ",
                "cleaning_func": lambda s: s.lower().strip(),
                "check_func": check_yes_or_no,
                "corresponding_attribute": "quotes_flag",
            },
            {
                "q_text": "Of the following, which securities do you plan to track?"
                + "[Stocks, ETFs, Forex, Futures, All] (comma-separated): ",
                "cleaning_func": lambda securities_input: [
                    sec.strip() for sec in securities_input.split(",")
                ],
                "check_func": check_security_types,
                "corresponding_attribute": "seed_data",
            },
        ]
        return mkt_data_q_list

    @property
    def quotes_questions(self):
        """Sets the questions for the quotes data"""
        quotes_questions = [
            {
                "q_text": "Would you like to store full quotes or consolidated? ['Full'/'Consolidated']: ",
                "cleaning_func": lambda s: s.lower().strip(),
                "check_func": check_quotes_type,
                "corresponding_attribute": "full_quotes_flag",
            }
        ]
        return quotes_questions

    def get_prev_question_index(
        self, current_q_index, current_group
    ) -> tuple[int, List]:
        """
        If someone wants to go back to a previous question, then they can use ctrl+z
        to undo. If they are not on the first question, this will return the index of the previous question
        """

        if (current_q_index >= 1) or (current_q_index > len(current_group) * -1):
            prev_q_index = current_q_index - 1
            return prev_q_index, current_group
        print("There are no other previous questions")
        return current_q_index, current_group

    def get_question_info(
        self, q_group: List, q_index: int
    ) -> tuple[str, Callable, Callable, Any]:
        """
        Gets all the information for a question in a group
        """
        q_info: dict = q_group[q_index]
        q_text = q_info.get("q_text")
        cleaning_func = q_info.get("cleaning_fun")
        check_func = q_info.get("check_func")
        corresponding_attribute = q_info.get("corresponding_attribute")
        return q_text, cleaning_func, check_func, corresponding_attribute

    def q_builder(self, q_index, q_group):
        """
        This sets the question text, gets the response as an input,
        cleans the response, then sets the corresponding attribute.
        """
        q_text, cleaning_func, check_func, attr_name = self.get_question_info(q_group, q_index)
        response: str = input(f"{q_text}: ")

        # If the user hits ctrl+z
        if response == "^Z":
            q_index = self.get_prev_question_index(q_index, q_group)
            return q_index, q_group

        clean_response = cleaning_func(response)
        updated_val = check_func(clean_response)

        try:
            setattr(self.config_info, attr_name, clean_response)
            q_index += 1
            return q_index, q_group
        except Warning as w:
            print(w)
            setattr(self.config_info, attr_name, updated_val)
            q_index += 1
            return q_index, q_group
        except ValueError as e:
            print(e)
            return q_index, q_group
        except KeyboardInterrupt:
            print("Keyboard interrupt occurred, closing CLI tool...")
        except Exception as e:
            print("Unexpected exception occurred, try again: %x", e)
            return q_index, q_group

    def generate_config_info(self) -> ConfigInfo:
        """
        This function will generate the config info for the user
        """
        # SQL questions
        q_index = 0
        while q_index < len(self.sql_info_questions):
            q_index = self.q_builder(q_index, self.sql_info_questions)

        # Initial Flags Questions
        q_index = 0
        while q_index < len(self.initial_flags_questions):
            q_index = self.q_builder(q_index, self.initial_flags_questions)
        # Market Data Questions
        if self.config_info.market_data_flag:
            q_index = 0
            while q_index < len(self.mkt_data_q_list):
                self.q_builder(q_index, self.mkt_data_q_list)

        # Quotes Questions
        if self.config_info.quotes_flag:
            q_index = 0
            while q_index < len(self.quotes_questions):
                self.q_builder(q_index, self.quotes_questions)
        return self.config_info
