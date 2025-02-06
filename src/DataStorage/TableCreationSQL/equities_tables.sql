CREATE TABLE IF NOT EXISTS FundamentalSnapshots (
    [SymbolID] INTEGER,
    [DateTime] TEXT,
    [MarketCap] REAL,
    PRIMARY KEY ([SymbolID], [DateTime]),
    FOREIGN KEY (SymbolID)
        REFERENCES SecuritiesInfo(SymbolID)
)

CREATE TABLE IF NOT EXISTS DividendHistory (
    [SymbolID] INTEGER PRIMARY KEY,
    [DateTime] TEXT,
    [Dividend] REAL,
    PRIMARY KEY ([SymbolID], [DateTime]),
    FOREIGN KEY (SymbolID)
        REFERENCES SecuritiesInfo(SymbolID)
)

CREATE TABLE IF NOT EXISTS EarningsHistory (
    [SymbolID] INTEGER PRIMARY KEY,
    [DateTime] TEXT,
    [Earnings] REAL,
    PRIMARY KEY ([SymbolID], [DateTime]),
    FOREIGN KEY (SymbolID)
        REFERENCES SecuritiesInfo(SymbolID)
)

CREATE TABLE IF NOT EXISTS StockSplits (
    [SymbolID] INTEGER PRIMARY KEY,
    [DateTime] TEXT,
    [Split] INTEGER,
    PRIMARY KEY ([SymbolID], [DateTime]),
    FOREIGN KEY (SymbolID)
        REFERENCES SecuritiesInfo(SymbolID)
)