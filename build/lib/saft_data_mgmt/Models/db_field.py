"""
Module: db_field
Description: This defines the Field object for managing a SAFT-style SQL database for financial market and account data.
"""

from typing import Any, Optional
from dataclasses import dataclass

@dataclass
class Field:
    """
    Represents a column (field) in a database table.
    
    Attributes:
        name (str): The name of the field.
        data_type (str): The SQL data type (e.g., 'INTEGER', 'VARCHAR').
        nullable (bool): Indicates if the field can be null.
        unique (bool): Indicates if the field must be unique.
        default (Any): The default value for the field.
        foreign_key (Optional[str]): Optional reference to a foreign key in the format "other_table.other_field".
        index (bool): Indicates if the field should be indexed.
    """
    name: str
    data_type: str
    nullable: bool = True
    unique: bool = False
    default: Any = None
    foreign_key: Optional[str] = None
    index: bool = False

    def describe(self) -> None:
        """
        Prints a dictionary of the fields attributes

        Returns:
            dict: a dictionary containing the
        """
        info = {
            "field_name": self.name,
            "field_data_type":self.data_type,
            "field_nullable":self.nullable,
            "field_unique":self.unique,
            "field_default_val":self.default,
            "field_foreign_key":self.foreign_key,
            "field_index":self.index
        }
        print(info)
