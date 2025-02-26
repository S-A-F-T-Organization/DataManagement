CREATE TABLE IF NOT EXISTS SecuritiesInfo(
    [symbol_id] INTEGER PRIMARY KEY,
    [symbol] TEXT,
    [security_type_id] INTEGER NOT NULL,
    [to_int] INTEGER,
    [exchange_id] INTEGER NOT NULL,
    UNIQUE(symbol, exchange_id, security_type_id),
    FOREIGN KEY (security_type_id)
        REFERENCES SecurityTypes(security_type_id),
    FOREIGN KEY (exchange_id)
        REFERENCES SecurityExchanges(exchange_id)
)