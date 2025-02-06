"""
This module stores dataclass objects for each of the tables 
in the Portfolio Analytics database
"""

from dataclasses import dataclass
from typing import Union, List


@dataclass
class Transactions:
    """
    _summary_
    """
    transaction_id:Union[int, List[int]] = None
    account_id:Union[int, List[int]] = None
    transaction_type_id:Union[int, List[int]] = None
    transaction_value:Union[float, List[float]] = None


@dataclass
class TransactionTypes:
    """
    _summary_
    """
    transaction_type_id:Union[str, List[str]] = None
    transaction_type:Union[str, List[str]] = None


@dataclass
class AccountSummary:
    """
    _summary_
    """
    account_id:Union[int, List[int]] = None
    account_start_datetime:Union[int, List[int]] = None
    account_start_value:Union[float, List[float]] = None
    account_alias:Union[str, List[str]] = None


@dataclass
class AllOrders:
    """
    _summary_
    """
    transaction_id:Union[int, List[int]] = None
    placed_datetime:Union[int, List[int]] = None
    symbol_id:Union[int, List[int]] = None
    order_type_id:Union[int, List[int]] = None
    strategy_id:Union[int, List[int]] = None
    inference_id:Union[int, List[int]] = None
    action_id:Union[int, List[int]] = None


@dataclass
class CanceledOrders(AllOrders):
    """
    _summary_
    """
    transaction_id:Union[int, List[int]] = None
    canceled_datetime:Union[int, List[int]] = None

@dataclass
class PlacedOrders(AllOrders):
    """
    _summary_
    """
    transaction_id:Union[int, List[int]] = None
    executed_datetime:Union[int, List[int]] = None
    execution_price:Union[float, List[float]] = None
    fees:Union[float, List[float]] = None

@dataclass
class StrategyInfo:
    """
    _summary_
    """
    strategy_id:Union[int, List[int]] = None
    strategy_name:Union[str, List[str]] = None
    strategy_verion:Union[float, List[float]] = None

@dataclass
class ModelInference:
    """
    _summary_
    """
    inference_id:Union[int, List[int]] = None
    symbol_id:Union[int, List[int]] = None
    predicted_sentiment:Union[str, List[str]] = None
    inference_start_datetime:Union[int, List[int]] = None
    inference_end_datetime:Union[int, List[int]] = None
    confidence:Union[float, List[float]] = None
    reference_timestamp:Union[int, List[int]] = None
