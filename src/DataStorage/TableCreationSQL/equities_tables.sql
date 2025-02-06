CREATE TABLE IF NOT EXISTS FundamentalSnapshots (
    [SymbolID] INTEGER PRIMARY KEY,
    [DateTime] TEXT,
    [MarketCap] REAL
)

CREATE TABLE IF NOT EXISTS DividendHistory (
    [SymbolID] INTEGER PRIMARY KEY,
    [DateTime] TEXT,
    [Dividend] REAL
)

CREATE TABLE IF NOT EXISTS EarningsHistory (
    [SymbolID] INTEGER PRIMARY KEY,
    [DateTime] TEXT,
    [Earnings] REAL
)

CREATE TABLE IF NOT EXISTS StockSplits (
    [SymbolID] INTEGER PRIMARY KEY,
    [DateTime] TEXT,
    [Split] REAL
)