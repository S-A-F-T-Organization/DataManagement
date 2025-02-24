CREATE TABLE IF NOT EXISTS SecuritiesInfo(
    [SymbolID] INTEGER PRIMARY KEY AUTO_INCREMENT,
    [SecurityTypeID] INTEGER NOT NULL,
    [ToInt] INTEGER NOT NULL,
    [ExchangeID] INTEGER NOT NULL,
    [RTHStartTime] TEXT,
    [RTHEndTime] TEXT
)

CREATE TABLE IF NOT EXISTS SecurityPrices (
    [SymbolID] INTEGER NOT NULL,
    [DateTime] INTEGER NOT NULL,
    [OpenPrice] INTEGER NOT NULL,
    [HighPrice] INTEGER NOT NULL,
    [LowPrice] INTEGER NOT NULL,
    [ClosePrice] INTEGER NOT NULL,
    [Volume] INTEGER NOT NULL
)

CREATE TABLE IF NOT EXISTS SecurityTypes (
    [SecurityTypeID] INTEGER PRIMARY KEY AUTO_INCREMENT,
    [SecurityType] TEXT NOT NULL
)

CREATE TABLE IF NOT EXISTS SecurityExchanges (
    [ExchangeID] INTEGER PRIMARY KEY AUTO_INCREMENT,
    [Exchange] TEXT NOT NULL
)