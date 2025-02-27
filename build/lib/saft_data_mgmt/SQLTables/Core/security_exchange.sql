CREATE TABLE IF NOT EXISTS SecurityExchanges (
    [exchange_id] INTEGER PRIMARY KEY,
    [exhcnage_name] TEXT NOT NULL,
    [local_timezone] TEXT,
    [rth_start_time_utc] TEXT,
    [rth_end_time_utc] TEXT,
    UNIQUE(exchange_name)
)