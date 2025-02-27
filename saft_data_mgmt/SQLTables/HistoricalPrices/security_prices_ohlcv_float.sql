CREATE TABLE IF NOT EXISTS SecurityPrices (
    [ohlcv_id] INTEGER PRIMARY KEY,
    [symbol_id] INTEGER NOT NULL,
    [timestamp_utc_ms] INTEGER NOT NULL,
    [open_price] REAL NOT NULL,
    [high_price] REAL NOT NULL,
    [low_price] REAL NOT NULL,
    [close_price] REAL NOT NULL,
    [volume] INTEGER NOT NULL,
    UNIQUE (symbol_id, timestamp_utc_ms),
    FOREIGN KEY (symbol_id)
        REFERENCES SecuritiesInfo(symbol_id)
);