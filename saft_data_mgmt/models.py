"""
This module contains all of the relevant data models including the SQL data tables and
predefined joins that are useful for many workflows.
"""

from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# ----------------------------------------------------------------#
#                       Core Tables                              #
# ----------------------------------------------------------------#


class SecurityTypes(Base):
    """Represents the SecurityTypes table."""

    __tablename__ = "SecurityTypes"

    security_type_id = Column(SmallInteger, primary_key=True)
    security_type = Column(String(50), nullable=False, unique=True)

    securities = relationship("SecuritiesInfo", back_populates="security_type")

    def __repr__(self):
        return f"SecurityType(id={self.security_type_id}, type={self.security_type})"


class SecurityExchanges(Base):
    """Represents the SecurityExchanges table."""

    __tablename__ = "SecurityExchanges"

    exchange_id = Column(SmallInteger, primary_key=True)
    exchange_name = Column(String(50), nullable=False, unique=True)
    local_timezone = Column(String(30))

    securities = relationship("SecuritiesInfo", back_populates="exchange")

    def __repr__(self):
        return f"SecurityExchange(id={self.exchange_id}, name={self.exchange_name})"


class SecuritiesInfo(Base):
    """Represents the SecuritiesInfo table."""

    __tablename__ = "SecuritiesInfo"
    __table_args__ = (
        UniqueConstraint(
            "symbol",
            "exchange_id",
            "security_type_id",
            name="uix_symbol_exchange_security_type",
        ),
    )

    symbol_id = Column(Integer, primary_key=True)
    symbol = Column(String(15))
    security_type_id = Column(
        Integer, ForeignKey("SecurityTypes.security_type_id"), nullable=False
    )
    to_int = Column(SmallInteger)
    exchange_id = Column(
        Integer, ForeignKey("SecurityExchanges.exchange_id"), nullable=False
    )

    security_type = relationship("SecurityTypes", back_populates="securities")
    exchange = relationship("SecurityExchanges", back_populates="securities")

    def __repr__(self):
        return f"Security(id={self.symbol_id}, symbol={self.symbol})"


# ----------------------------------------------------------------#
#           Historical Prices – Trade/Quotes Models              #
# ----------------------------------------------------------------#


# Variant using INTEGER types for prices
class SecurityPricesMBPConsolidatedInt(Base):
    """Represents the SecurityPricesMBPConsolidated table with integer prices."""

    __tablename__ = "SecurityPricesMBPConsolidated"
    quote_id = Column(Integer, primary_key=True)
    symbol_id = Column(Integer, ForeignKey("SecuritiesInfo.symbol_id"), nullable=False)
    timestamp_utc_ms = Column(Integer, nullable=False)
    trade_size = Column(Integer, nullable=False)
    trade_price = Column(Integer, nullable=False)
    best_bid_price = Column(Integer, nullable=False)
    best_bid_size = Column(Integer, nullable=False)
    best_ask_price = Column(Integer, nullable=False)
    best_ask_size = Column(Integer, nullable=False)
    best_bid_ct = Column(Integer, nullable=False)
    best_ask_ct = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("symbol_id", "timestamp_utc_ms", name="uix_symbol_timestamp"),
    )


# Variant using REAL types for prices
class SecurityPricesMBPConsolidatedFloat(Base):
    """Represents the SecurityPricesMBPConsolidated table with float prices."""

    __tablename__ = "SecurityPricesMBPConsolidated"
    quote_id = Column(Integer, primary_key=True)
    symbol_id = Column(Integer, ForeignKey("SecuritiesInfo.symbol_id"), nullable=False)
    timestamp_utc_ms = Column(Integer, nullable=False)
    trade_size = Column(Integer, nullable=False)
    trade_price = Column(Float, nullable=False)
    best_bid_price = Column(Float, nullable=False)
    best_bid_size = Column(Integer, nullable=False)
    best_ask_price = Column(Float, nullable=False)
    best_ask_size = Column(Integer, nullable=False)
    best_bid_ct = Column(Integer, nullable=False)
    best_ask_ct = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("symbol_id", "timestamp_utc_ms", name="uix_symbol_timestamp"),
    )


# ----------------------------------------------------------------#
#               Historical Prices – OHLCV Models                 #
# ----------------------------------------------------------------#


# OHLCV integer variant
class SecurityPricesOHLCVInt(Base):
    """Represents the SecurityPricesOHLCV table with integer prices."""

    __tablename__ = "SecurityPricesOHLCV"
    ohlcv_id = Column(Integer, primary_key=True)
    symbol_id = Column(Integer, ForeignKey("SecuritiesInfo.symbol_id"), nullable=False)
    timestamp_utc_ms = Column(Integer, nullable=False)
    open_price = Column(Integer, nullable=False)
    high_price = Column(Integer, nullable=False)
    low_price = Column(Integer, nullable=False)
    close_price = Column(Integer, nullable=False)
    volume = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("symbol_id", "timestamp_utc_ms", name="uix_symbol_timestamp"),
    )


# OHLCV float variant (note the table name differs)
class SecurityPricesOHLCVFloat(Base):
    """Represents the SecurityPrices table with float prices."""

    __tablename__ = "SecurityPrices"
    ohlcv_id = Column(Integer, primary_key=True)
    symbol_id = Column(Integer, ForeignKey("SecuritiesInfo.symbol_id"), nullable=False)
    timestamp_utc_ms = Column(Integer, nullable=False)
    open_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("symbol_id", "timestamp_utc_ms", name="uix_symbol_timestamp"),
    )


# ----------------------------------------------------------------#
#               Historical Prices – MBP Full Models              #
# ----------------------------------------------------------------#


# MBP Full integer variant
class SecurityPricesMBPFullInt(Base):
    """Represents the SecurityPricesMBPFull table with integer prices."""

    __tablename__ = "SecurityPricesMBPFull"
    quote_id = Column(Integer, primary_key=True)
    symbol_id = Column(Integer, ForeignKey("SecuritiesInfo.symbol_id"), nullable=False)
    timestamp_utc_ms = Column(Integer, nullable=False)
    action = Column(Integer, nullable=False)
    side = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    depth = Column(Integer, nullable=False)
    best_bid_price = Column(Integer, nullable=False)
    best_bid_size = Column(Integer, nullable=False)
    best_ask_price = Column(Integer, nullable=False)
    best_ask_size = Column(Integer, nullable=False)
    best_bid_ct = Column(Integer, nullable=False)
    best_ask_ct = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "symbol_id",
            "timestamp_utc_ms",
            "action",
            "side",
            "depth",
            name="uix_symbol_timestamp_action_side_depth",
        ),
    )


# MBP Full float variant
class SecurityPricesMBPFullFloat(Base):
    """Represents the SecurityPricesMBPFull table with float prices."""

    __tablename__ = "SecurityPricesMBPFull"
    quote_id = Column(Integer, primary_key=True)
    symbol_id = Column(Integer, ForeignKey("SecuritiesInfo.symbol_id"), nullable=False)
    timestamp_utc_ms = Column(Integer, nullable=False)
    action = Column(Integer, nullable=False)
    side = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    depth = Column(Integer, nullable=False)
    best_bid_price = Column(Float, nullable=False)
    best_bid_size = Column(Integer, nullable=False)
    best_ask_price = Column(Float, nullable=False)
    best_ask_size = Column(Integer, nullable=False)
    best_bid_ct = Column(Integer, nullable=False)
    best_ask_ct = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "symbol_id",
            "timestamp_utc_ms",
            "action",
            "side",
            "depth",
            name="uix_symbol_timestamp_action_side_depth",
        ),
    )


# ----------------------------------------------------------------#
#            Options OHLCV Models (Int vs Float)                 #
# ----------------------------------------------------------------#


# Options OHLCV integer variant
class OptionsOHLCVInt(Base):
    """Represents the OptionsOHLCV table with integer prices."""

    __tablename__ = "OptionsOHLCV"
    option_ohlcv_id = Column(Integer, primary_key=True, nullable=False)
    underlying_symbol_id = Column(
        Integer, ForeignKey("SecuritiesInfo.symbol_id"), nullable=False
    )
    timestamp_utc_ms = Column(Integer, nullable=False)
    strike_price = Column(Integer, nullable=False)
    option_type_id = Column(Integer, nullable=False)
    open_price = Column(Integer, nullable=False)
    high_price = Column(Integer, nullable=False)
    low_price = Column(Integer, nullable=False)
    close_price = Column(Integer, nullable=False)
    volume = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "underlying_symbol_id",
            "timestamp_utc_ms",
            "strike_price",
            "option_type_id",
            name="uix_options",
        ),
    )


# Options OHLCV float variant
class OptionsOHLCVFloat(Base):
    """Represents the OptionsOHLCV table with float prices."""

    __tablename__ = "OptionsOHLCV"
    option_ohlcv_id = Column(Integer, primary_key=True, nullable=False)
    underlying_symbol_id = Column(
        Integer, ForeignKey("SecuritiesInfo.symbol_id"), nullable=False
    )
    timestamp_utc_ms = Column(Integer, nullable=False)
    strike_price = Column(Float, nullable=False)
    option_type_id = Column(Integer, nullable=False)
    open_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "underlying_symbol_id",
            "timestamp_utc_ms",
            "strike_price",
            "option_type_id",
            name="uix_options",
        ),
    )


# ----------------------------------------------------------------#
#              Securities MetaData Tables                        #
# ----------------------------------------------------------------#


class Issuers(Base):
    """Represents the Issuers table."""

    __tablename__ = "Issuers"
    issuer_id = Column(Integer, primary_key=True)
    issuer_name = Column(String(100), unique=True)

    def __repr__(self):
        return f"Issuer(id={self.issuer_id}, name={self.issuer_name})"


class UnderlyingAssetTypes(Base):
    """Represents the UnderlyingAssetTypes table."""

    __tablename__ = "UnderlyingAssetTypes"
    underlying_asset_type_id = Column(Integer, primary_key=True)
    underlying_asset_type = Column(String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"UnderlyingAssetType(id={self.underlying_asset_type_id}, type={self.underlying_asset_type})"


class StockSplits(Base):
    """Represents the StockSplits table."""

    __tablename__ = "StockSplits"
    split_id = Column(Integer, primary_key=True)
    symbol_id = Column(Integer, ForeignKey("SecuritiesInfo.symbol_id"))
    split_timestamp_utc_sec = Column(Integer)
    share_multiplier = Column(Integer)

    __table_args__ = (
        UniqueConstraint(
            "symbol_id", "split_timestamp_utc_sec", name="uix_stock_split"
        ),
    )

    def __repr__(self):
        return f"StockSplit(id={self.split_id}, symbol_id={self.symbol_id})"


class StockMetadata(Base):
    """Represents the StockMetadata table."""

    __tablename__ = "StockMetadata"
    symbol_id = Column(Integer, primary_key=True)
    full_name = Column(String(200))
    sector_id = Column(SmallInteger, ForeignKey("SectorInfo.sector_id"))
    industry_id = Column(Integer, ForeignKey("IndustryInfo.industry_id"))
    ipo_date_utc_sec = Column(Integer)

    def __repr__(self):
        return f"StockMetadata(symbol_id={self.symbol_id}, full_name={self.full_name})"


class SectorInfo(Base):
    """Represents the SectorInfo table."""

    __tablename__ = "SectorInfo"
    sector_id = Column(SmallInteger, primary_key=True)
    sector_name = Column(String(150), unique=True)

    def __repr__(self):
        return f"SectorInfo(id={self.sector_id}, name={self.sector_name})"


class MutualFundSnapshots(Base):
    """Represents the MutualFundSnapshots table."""

    __tablename__ = "MutualFundSnapshots"
    snapshot_id = Column(Integer, primary_key=True)
    nav = Column(Float, nullable=False)
    expense_ratio = Column(Float, nullable=False)
    ytd_return = Column(Float, nullable=False)

    def __repr__(self):
        return f"MutualFundSnapshot(id={self.snapshot_id}, nav={self.nav})"


class IndustryInfo(Base):
    """Represents the industry_info table."""

    __tablename__ = "industry_info"
    industry_id = Column(SmallInteger, primary_key=True)
    industry_name = Column(String(150), unique=True)

    def __repr__(self):
        return f"IndustryInfo(id={self.industry_id}, name={self.industry_name})"


class FuturesMetadata(Base):
    """Represents the FuturesMetadata table."""

    __tablename__ = "FuturesMetadata"
    symbol_id = Column(Integer, primary_key=True)
    exchange_id = Column(SmallInteger)
    multiplier = Column(Float)
    min_tick_size = Column(Float)
    min_tick_value = Column(Float)
    underlying_asset_type_id = Column(
        Integer, ForeignKey("UnderlyingAssetTypes.underlying_asset_type_id")
    )
    underlying_asset_name = Column(String(100))

    def __repr__(self):
        return f"FuturesMetadata(symbol_id={self.symbol_id}, underlying_asset_name={self.underlying_asset_name})"


class FundamentalsSnapshots(Base):
    """Represents the FundamentalsSnapshots table."""

    __tablename__ = "FundamentalsSnapshots"
    snapshot_id = Column(Integer, primary_key=True)
    symbol_id = Column(Integer, ForeignKey("SecuritiesInfo.symbol_id"))
    timestamp_utc_sec = Column(Integer)

    __table_args__ = (
        UniqueConstraint(
            "symbol_id", "timestamp_utc_sec", name="uix_fundamentals_snapshots"
        ),
    )

    def __repr__(self):
        return (
            f"FundamentalsSnapshot(id={self.snapshot_id}, symbol_id={self.symbol_id})"
        )


class ETFMetadata(Base):
    """Represents the ETFMetadata table."""

    __tablename__ = "ETFMetadata"
    symbol_id = Column(Integer, primary_key=True)
    full_name = Column(String(200))
    underlying_asset_type_id = Column(
        Integer, ForeignKey("UnderlyingAssetTypes.underlying_asset_type_id")
    )
    issuer_id = Column(Integer, ForeignKey("Issuers.issuer_id"))
    underlying_asset_name = Column(String(100))

    def __repr__(self):
        return f"ETFMetadata(symbol_id={self.symbol_id}, full_name={self.full_name})"


class EquitiesSnapshots(Base):
    """Represents the EquitiesSnapshots table."""

    __tablename__ = "EquitiesSnapshots"
    snapshot_id = Column(
        Integer, ForeignKey("FundamentalsSnapshots.snapshot_id"), primary_key=True
    )
    market_cap = Column(Float)
    pe_ratio = Column(Float)
    eps_ttm = Column(Float)
    dividend_yield = Column(Float)
    dividend_per_share = Column(Float)
    price_to_book = Column(Float)

    def __repr__(self):
        return f"EquitiesSnapshots(snapshot_id={self.snapshot_id})"


class Currencies(Base):
    """Represents the Currencies table."""

    __tablename__ = "Currencies"
    currency_id = Column(Integer, primary_key=True)
    currency_abbr = Column(String(10), nullable=False, unique=True)

    def __repr__(self):
        return f"Currency(id={self.currency_id}, abbr={self.currency_abbr})"


class ForexMetadata(Base):
    """Represents the ForexMetadata table."""

    __tablename__ = "ForexMetadata"
    symbol_id = Column(
        Integer, ForeignKey("SecuritiesInfo.symbol_id"), primary_key=True
    )
    base_currency_id = Column(
        SmallInteger, ForeignKey("Currencies.currency_id"), nullable=False
    )
    quote_currency_id = Column(
        SmallInteger, ForeignKey("Currencies.currency_id"), nullable=False
    )

    def __repr__(self):
        return f"ForexMetadata(symbol_id={self.symbol_id})"


# ----------------------------------------------------------------#
#                      PortfolioDB Tables                          #
# ----------------------------------------------------------------#


class AccountInfo(Base):
    """Represents the AccountInfo table."""

    __tablename__ = "AccountInfo"
    account_id = Column(Integer, primary_key=True)
    account_start_timestamp_utc_sec = Column(Integer)
    account_start_value = Column(Float)
    account_alias = Column(String(150), unique=True)
    paper_trade_flag = Column(Integer)

    def __repr__(self):
        return f"AccountInfo(id={self.account_id}, alias={self.account_alias})"


class OrderTypes(Base):
    """Represents the OrderTypes table."""

    __tablename__ = "OrderTypes"
    order_type_id = Column(Integer, primary_key=True)
    order_type = Column(String(50), unique=True)

    def __repr__(self):
        return f"OrderTypes(id={self.order_type_id}, type={self.order_type})"


class OrderActions(Base):
    """Represents the OrderActions table."""

    __tablename__ = "OrderActions"
    order_action_id = Column(SmallInteger, primary_key=True)
    order_action = Column(String(50), unique=True)

    def __repr__(self):
        return f"OrderActions(id={self.order_action_id}, action={self.order_action})"


class TransactionTypes(Base):
    """Represents the TransactionTypes table."""

    __tablename__ = "TransactionTypes"
    transaction_type_id = Column(Integer, primary_key=True)
    transaction_type = Column(String(50), unique=True)

    def __repr__(self):
        return f"TransactionTypes(id={self.transaction_type_id}, type={self.transaction_type})"


class Transactions(Base):
    """Represents the Transactions table."""

    __tablename__ = "Transactions"
    transaction_id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("AccountInfo.account_id"))
    transaction_type_id = Column(
        Integer, ForeignKey("TransactionTypes.transaction_type_id")
    )
    transaction_timestamp_utc_ms = Column(Integer)
    transaction_value = Column(Float)

    def __repr__(self):
        return f"Transactions(id={self.transaction_id}, value={self.transaction_value})"


class Sessions(Base):
    """Represents the Sessions table."""

    __tablename__ = "Sessions"
    session_id = Column(Integer, primary_key=True)
    created_timestamp_utc_ms = Column(Integer)
    ended_timestamp_utc_ms = Column(Integer)

    def __repr__(self):
        return f"Sessions(id={self.session_id})"


class Strategies(Base):
    """Represents the Strategies table."""

    __tablename__ = "Strategies"
    strategy_id = Column(Integer, primary_key=True)
    strategy_name = Column(String(100))
    strategy_version = Column(String(50))
    strategy_description = Column(String(200))

    __table_args__ = (
        UniqueConstraint(
            "strategy_name", "strategy_version", name="uix_strategy_name_version"
        ),
    )

    def __repr__(self):
        return f"Strategies(id={self.strategy_id}, name={self.strategy_name})"


class Modules(Base):
    """Represents the Modules table."""

    __tablename__ = "Modules"
    module_id = Column(Integer, primary_key=True)
    strategy_id = Column(Integer, ForeignKey("Strategies.strategy_id"), nullable=False)
    module_name = Column(String(100), nullable=False)

    __table_args__ = (
        UniqueConstraint("strategy_id", "module_name", name="uix_strategy_module"),
    )

    def __repr__(self):
        return f"Modules(id={self.module_id}, module_name={self.module_name})"


class Inferences(Base):
    """Represents the Inferences table."""

    __tablename__ = "Inferences"
    inference_id = Column(Integer, primary_key=True)
    symbol_id = Column(Integer, ForeignKey("SecuritiesInfo.symbol_id"))
    strategy_id = Column(Integer, ForeignKey("Strategies.strategy_id"))
    session_id = Column(Integer, ForeignKey("Sessions.session_id"))
    inference_outputs = Column(Integer)
    inference_start_timestamp_utc_ms = Column(Integer)
    inference_end_timestamp_utc_ms = Column(Integer)
    candle_reference_timestamp_utc_sec = Column(Integer)

    __table_args__ = (
        UniqueConstraint(
            "symbol_id",
            "strategy_id",
            "session_id",
            "candle_reference_timestamp_utc_sec",
            name="uix_inference_unique",
        ),
    )

    def __repr__(self):
        return f"Inferences(id={self.inference_id})"


class InferenceTimes(Base):
    """Represents the inference_times table."""

    __tablename__ = "inference_times"
    inference_step_timing_id = Column(Integer, primary_key=True, nullable=False)
    inference_id = Column(
        Integer, ForeignKey("Inferences.inference_id"), nullable=False
    )
    inference_step_id = Column(Integer, nullable=False)
    step_start_timestamp_utc_ms = Column(Integer, nullable=False)
    step_end_timestamp_utc_ms = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "inference_id", "inference_step_id", name="uix_inference_step"
        ),
    )

    def __repr__(self):
        return f"InferenceTimes(id={self.inference_step_timing_id})"


class InferenceSteps(Base):
    """Represents the InferenceSteps table."""

    __tablename__ = "InferenceSteps"
    inference_step_id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey("Modules.module_id"), nullable=False)
    step_name = Column(String(100), nullable=False)

    __table_args__ = (
        UniqueConstraint("module_id", "step_name", name="uix_module_step"),
    )

    def __repr__(self):
        return f"InferenceSteps(id={self.inference_step_id}, name={self.step_name})"


class AllOrders(Base):
    """Represents the AllOrders table."""

    __tablename__ = "AllOrders"
    order_id = Column(Integer, primary_key=True)
    symbol_id = Column(Integer, ForeignKey("SecuritiesInfo.symbol_id"))
    transaction_id = Column(
        Integer, ForeignKey("Transactions.transaction_id"), unique=True
    )
    broker_order_id = Column(Integer)
    order_placed_timestamp_utc_ms = Column(Integer)
    order_type_id = Column(Integer, ForeignKey("OrderTypes.order_type_id"))
    order_action_id = Column(Integer, ForeignKey("OrderActions.order_action_id"))
    inference_id = Column(Integer, ForeignKey("Inferences.inference_id"))
    quantity = Column(Integer)

    def __repr__(self):
        return f"AllOrders(id={self.order_id})"


class CanceledOrders(Base):
    """Represents the CanceledOrders table."""

    __tablename__ = "CanceledOrders"
    order_id = Column(Integer, ForeignKey("AllOrders.order_id"), primary_key=True)
    canceled_timestamp_utc_ms = Column(Integer)

    def __repr__(self):
        return f"CanceledOrders(order_id={self.order_id})"


class ConditionalOrders(Base):
    """Represents the ConditionalOrders table."""

    __tablename__ = "ConditionalOrders"
    order_id = Column(Integer, ForeignKey("AllOrders.order_id"), primary_key=True)
    trigger_price = Column(Float, nullable=False)

    def __repr__(self):
        return f"ConditionalOrders(order_id={self.order_id}, trigger_price={self.trigger_price})"


class ExecutedOrdersTable(Base):
    """Represents the ExecutedOrdersTable."""

    __tablename__ = "ExecutedOrdersTable"
    order_id = Column(Integer, ForeignKey("AllOrders.order_id"), primary_key=True)
    execution_timestamp_utc_ms = Column(Integer)
    execution_price = Column(Float)
    fees = Column(Float)

    def __repr__(self):
        return f"ExecutedOrdersTable(order_id={self.order_id})"


class ModelLibraries(Base):
    """Represents the ModelLibraries table."""

    __tablename__ = "ModelLibraries"
    model_library_id = Column(Integer, primary_key=True)
    model_library = Column(String(100), nullable=False, unique=True)

    def __repr__(self):
        return (
            f"ModelLibraries(id={self.model_library_id}, library={self.model_library})"
        )


class ModelTypes(Base):
    """Represents the ModelTypes table."""

    __tablename__ = "ModelTypes"
    model_type_id = Column(Integer, primary_key=True)
    model_type = Column(String(100), nullable=False)
    model_library_id = Column(
        Integer, ForeignKey("ModelLibraries.model_library_id"), nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "model_type", "model_library_id", name="uix_model_type_library"
        ),
    )

    def __repr__(self):
        return f"ModelTypes(id={self.model_type_id}, type={self.model_type})"


class Models(Base):
    """Represents the Models table."""

    __tablename__ = "Models"
    model_id = Column(Integer, primary_key=True)
    strategy_id = Column(Integer, ForeignKey("Strategies.strategy_id"), nullable=False)
    model_name = Column(String(100), nullable=False)
    model_type_id = Column(
        Integer, ForeignKey("ModelTypes.model_type_id"), nullable=False
    )
    model_dvc_hash = Column(String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"Models(id={self.model_id}, name={self.model_name})"
