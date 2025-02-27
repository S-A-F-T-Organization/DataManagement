CREATE OR ALTER TABLE EquitiesSnapshots (
    [snapshot_id] INTEGER PRIMARY KEY,
    [market_cap] REAL,
    [pe_ratio] REAL,
    [eps_ttm] REAL,
    [dividend_yield] REAL,
    [dividend_per_share] REAL,
    [price_to_book] REAL,
    FOREIGN KEY ([snapshot_id])
        REFERENCES FundamentalsSnapShots([snapshot_id])
);