CREATE TABLE IF NOT EXISTS StockSplits (
    [split_id] INTEGER PRIMARY KEY,
    [symbol_id] INTEGER,
    [split_timestamp_utc_sec] INTEGER,
    [share_multiplier] INTEGER,
    UNIQUE (symbol_id, split_timestamp_utc_sec),
    FOREIGN KEY (symbol_id)
        REFERENCES SecuritiesInfo(symbol_id)
)