-- fact table
CREATE TABLE IF NOT EXISTS transaction_table (
    [trade_id] TEXT PRIMARY KEY,
    [model_id] TEXT NOT NULL,
    [session_id] TEXT NOT NULL,
    [strategy_id] TEXT NOT NULL,
    [high_level_trade_policy_id] TEXT NOT NULL,
    [start_timestamp_ms] INTEGER NOT NULL,
    [end_timestamp_ms] INTEGER NOT NULL, 
    [ticker] TEXT NOT NULL,
    [quantity] INT NOT NULL,
    [profit_loss_total] REAL NOT NULL 
);

-- ticker dimension tables
CREATE TABLE IF NOT EXISTS ticker_table (
    [ticker] TEXT PRIMARY KEY,
    [description] TEXT NOT NULL,
    [exchange] TEXT NOT NULL, 
    [asset_type] TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS future_metadata_table (
    [ticker] TEXT PRIMARY KEY,
    [future_group] TEXT NOT NULL,
    [to_int_scalar] INTEGER NOT NULL,
    [to_price_scalar] INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS ticker_standard_schedule_table (
    [ticker] TEXT PRIMARY KEY, 
    [start_time_utc] TEXT NOT NULL,
    [duration_of_trading_period_ms] INTEGER NOT NULL,

    -- booleans
    [include_monday] INTEGER NOT NULL, 
    [include_tuesday] INTEGER NOT NULL, 
    [include_wednesday] INTEGER NOT NULL, 
    [include_thursday] INTEGER NOT NULL, 
    [include_friday] INTEGER NOT NULL, 
    [include_saturday] INTEGER NOT NULL, 
    [include_sunday] INTEGER NOT NULL 
);

-- dimension table
CREATE TABLE IF NOT EXISTS session_table (
    [session_id] TEXT PRIMARY KEY,
    [created_on_ms] INTEGER NOT NULL,
    [start_timestamp_ms] INTEGER NOT NULL, 
    [end_timestamp_ms] INTEGER NOT NULL,
    [data_reader_start_timestamp_ms] INTEGER NOT NULL
);

-- dimension table
CREATE TABLE IF NOT EXISTS model_table (
    [model_id] TEXT PRIMARY KEY, 
    [model_name] TEXT NOT NULL,
    [created_at_timestamp_ms] INTEGER NOT NULL,
    [created_by] TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS initial_data_requirement_table (
    [initial_data_req_id] INT PRIMARY KEY,
    [model_id] TEXT NOT NULL,
    [user_defined_id] TEXT NOT NULL,

    [req_desc] TEXT NOT NULL,
    [ticker] TEXT NOT NULL,
    [time_anchor] TEXT NOT NULL,
    [start_offset_from_anchor_ms] INTEGER NOT NULL,
    [measure_for_ms] INTEGER NOT NULL,
    [interval_to_measure_at_ms] INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS reoccur_data_requirement_table (
    [reoccur_data_req_id] INT PRIMARY KEY,
    [model_id] TEXT NOT NULL,
    [user_defined_id] TEXT NOT NULL,
    [ticker] TEXT NOT NULL,
    [interval_to_measure_at_ms] INTEGER NOT NULL,
    [num_measurements_required] INTEGER NOT NULL,
    [require_consecutive] INTEGER NOT NULL -- boolean
);

-- for storing which strategy was used for trades
-- dimension table 
CREATE TABLE IF NOT EXISTS trade_strategy_table (
    [strategy_table_id] TEXT PRIMARY KEY,
    [on_sentiment] TEXT NOT NULL,
    [min_confidence] INTEGER NOT NULL,
    [static_time_to_hold_ms] INTEGER,
    [stop_loss_pct] REAL NOT NULL
);

-- dimension table
CREATE TABLE IF NOT EXISTS high_level_trade_policy_table (
    [high_level_trade_policy_id] TEXT PRIMARY KEY,
    [max_concurrent_trades_allowed] INTEGER NOT NULL,
    [max_pct_account_utilization] REAL NOT NULL,
    [min_account_balence_needed_cents] INTEGER NOT NULL
);