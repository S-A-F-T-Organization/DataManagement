CREATE TABLE SecurityPricesMBPConsolidated (
    [quote_id] INTEGER PRIMARY KEY,
    [symbol_id] INTEGER NOT NULL,
    [timestamp_utc_ms] INTEGER NOT NULL,
    [trade_size] INTEGER NOT NULL,
    [trade_price] INTEGER NOT NULL,
    [best_bid_price] INTEGER NOT NULL,
    [best_bid_size]  INTEGER NOT NULL,
    [best_ask_price] INTEGER NOT NULL,
    [best_ask_size] INTEGER NOT NULL,
    [best_bid_ct] INTEGER NOT NULL,
    [best_ask_ct] INTEGER NOT NULL,
    UNIQUE(symbol_id, timestamp_utc_ms),
    FOREIGN KEY (symbol_id)
        REFERENCES SecuritiesInfo(symbol_id)
);