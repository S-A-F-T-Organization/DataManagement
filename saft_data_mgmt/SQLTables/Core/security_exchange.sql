CREATE TABLE IF NOT EXISTS SecurityExchanges (
    [exchange_id] INTEGER PRIMARY KEY,
    [exchange_name] TEXT NOT NULL,
    [local_timezone] TEXT,
    UNIQUE(exchange_name)
)