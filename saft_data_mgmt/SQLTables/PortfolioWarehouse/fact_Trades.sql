CREATE OR ALTER TABLE fact_Trades (
    trade_key INTEGER NOT NULL PRIMARY KEY,
    trade_open_date_key INTEGER NOT NULL,
    trade_close_date_key INTEGER NOT NULL,
    trade_open_time_key INTEGER NOT NULL,
    trade_close_time_key INTEGER NOT NULL,
    realized_pnl REAL NOT NULL,
    fees_paid REAL NOT NULL,
    trade_max_value REAL NOT NULL,
    trade_min_value REAL NOT NULL,
    max_value_time_from_open INTEGER NOT NULL,
    min_value_time_from_open INTEGER NOT NULL

)