CREATE TABLE IF NOT EXISTS SecurityPrices (
    [ohlcv_id] INTEGER PRIMARY KEY,
    [symbol_id] INTEGER NOT NULL,
    [timestamp_utc_ms] INTEGER NOT NULL,
    [open_price] INTEGER NOT NULL,
    [high_price] INTEGER NOT NULL,
    [low_price] INTEGER NOT NULL,
    [close_price] INTEGER NOT NULL,
    [volume] INTEGER NOT NULL,
    UNIQUE (symbol_id, timestamp_utc_ms),
    FOREIGN KEY (symbol_id)
        REFERENCES SecuritiesInfo(symbol_id)
);