CREATE TABLE IF NOT EXISTS SecurityPrices (
    [SymbolID] INTEGER NOT NULL,
    [DateTime] INTEGER NOT NULL,
    [OpenPrice] REAL NOT NULL,
    [HighPrice] REAL NOT NULL,
    [LowPrice] REAL NOT NULL,
    [ClosePrice] REAL NOT NULL,
    [Volume] REAL NOT NULL,
    PRIMARY KEY ([SymbolID], [DateTime]),
    FOREIGN KEY (SymbolID)
        REFERENCES SecuritiesInfo(SymbolID)
)