CREATE TABLE SecurityPricesMBPFull (
    [quote_id]       INTEGER PRIMARY KEY,
    [symbol_id]      INTEGER NOT NULL,
    [timestamp_utc]  INTEGER NOT NULL,
    [action]         INTEGER NOT NULL,
    [side]           INTEGER NOT NULL,
    [size]           INTEGER NOT NULL,
    [depth]          INTEGER NOT NULL,
    [best_bid_price] REAL NOT NULL,
    [best_bid_size]  INTEGER NOT NULL,
    [best_ask_price] REAL NOT NULL,
    [best_ask_size]  INTEGER NOT NULL,
    [best_bid_ct]    INTEGER NOT NULL,
    [best_ask_ct]    INTEGER NOT NULL,
    FOREIGN KEY (symbol_id) REFERENCES SecuritiesInfo(symbol_id)
);

CREATE INDEX idx_SecurityPricesMBPFull_symbol_timestamp ON SecurityPricesMBPFull (symbol_id, timestamp_utc_ms);
