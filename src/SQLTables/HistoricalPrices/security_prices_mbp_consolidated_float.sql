CREATE TABLE SecurityPricesMBPConsolidated (
    quote_id INTEGER PRIMARY KEY,
    symbol_id INTEGER NOT NULL,
    timestamp_utc_ms INTEGER NOT NULL,
    depth INTEGER NOT NULL,
    best_bid_price REAL NOT NULL,
    best_bid_size  INTEGER NOT NULL,
    best_ask_price REAL,
    best_ask_size INTEGER NOT NULL,
    best_bid_ct INTEGER NOT NULL,
    best_ask_ct INTEGER NOT NULL,
    FOREIGN KEY (symbol_id) REFERENCES SecuritiesInfo(symbol_id)
);

CREATE INDEX idx_SecurityPricesMBPConsolidated_symbol_timestamp ON SecurityPricesMBPConsolidated (symbol_id, timestamp_utc_ms);