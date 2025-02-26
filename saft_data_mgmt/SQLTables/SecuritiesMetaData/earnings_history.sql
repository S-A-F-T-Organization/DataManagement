CREATE TABLE IF NOT EXISTS EarningsHistory (
    [SymbolID] INTEGER PRIMARY KEY,
    [DateTime] TEXT,
    [Earnings] REAL,
    PRIMARY KEY ([SymbolID], [DateTime]),
    FOREIGN KEY (SymbolID)
        REFERENCES SecuritiesInfo(SymbolID)
)