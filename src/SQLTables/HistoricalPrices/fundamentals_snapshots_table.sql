CREATE TABLE IF NOT EXISTS FundamentalSnapshots (
    [SymbolID] INTEGER,
    [DateTime] TEXT,
    [MarketCap] REAL,
    PRIMARY KEY ([SymbolID], [DateTime]),
    FOREIGN KEY (SymbolID)
        REFERENCES SecuritiesInfo(SymbolID)
)