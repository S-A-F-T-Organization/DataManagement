CREATE TABLE IF NOT EXISTS DividendHistory (
    [SymbolID] INTEGER PRIMARY KEY,
    [DateTime] TEXT,
    [Dividend] REAL,
    PRIMARY KEY ([SymbolID], [DateTime]),
    FOREIGN KEY (SymbolID)
        REFERENCES SecuritiesInfo(SymbolID)
)