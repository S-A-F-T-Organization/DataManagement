CREATE TABLE IF NOT EXISTS SessionTable(
    [session_id] INTEGER PRIMARY KEY,
    [created_timestamp_utc_ms] INTEGER,
    [ended_timestamp_utc_ms] INTEGER
)