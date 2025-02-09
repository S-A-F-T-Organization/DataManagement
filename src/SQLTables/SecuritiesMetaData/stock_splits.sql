CREATE TABLE IF NOT EXISTS StockSplits (
    [SymbolID] INTEGER PRIMARY KEY,
    [DateTime] TEXT,
    [Split] INTEGER,
    PRIMARY KEY ([SymbolID], [DateTime]),
    FOREIGN KEY (SymbolID)
        REFERENCES SecuritiesInfo(SymbolID)
)