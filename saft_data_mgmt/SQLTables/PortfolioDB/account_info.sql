CREATE TABLE IF NOT EXISTS AccountInfo(
    [account_id] INTEGER PRIMARY KEY,
    [account_start_timestamp_utc_sec] INTEGER,
    [account_start_value] REAL,
    [account_alias] TEXT,
    [paper_trade_flag] INTEGER,
    UNIQUE([account_alias])
)