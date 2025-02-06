CREATE TABLE IF NOT EXISTS SecurityPrices (
    [SymbolID] INTEGER NOT NULL,
    [DateTime] INTEGER NOT NULL,
    [OpenPrice] INTEGER NOT NULL,
    [HighPrice] INTEGER NOT NULL,
    [LowPrice] INTEGER NOT NULL,
    [ClosePrice] INTEGER NOT NULL,
    [Volume] INTEGER NOT NULL,
    PRIMARY KEY ([SymbolID], [DateTime]),
    FOREIGN KEY (SymbolID)
        REFERENCES SecuritiesInfo(SymbolID)
)