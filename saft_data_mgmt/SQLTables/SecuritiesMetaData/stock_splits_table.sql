CREATE TABLE IF NOT EXISTS StockSplits (
    [split_id] INTEGER PRIMARY KEY,
    [symbol_id] INTEGER,
    [splite_timestamp_utc_sec] INTEGER,
    [share_multiplier] INTEGER,
    UNIQUE (symbol_id, splite_timestamp_utc_sec),
    FOREIGN KEY (SymbolID)
        REFERENCES SecuritiesInfo(SymbolID)
)