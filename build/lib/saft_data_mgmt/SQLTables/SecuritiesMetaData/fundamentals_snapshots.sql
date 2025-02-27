CREATE TABLE IF NOT EXISTS FundamentalsSnapshots (
    [snapshot_id] INTEGER PRIMARY KEY,
    [symbol_id] INTEGER,
    [timestamp_utc_sec] TEXT,
    UNIQUE (symbol_id, timestamp_utc_sec),
    FOREIGN KEY (symbol_id)
        REFERENCES SecuritiesInfo(symbol_id)
)