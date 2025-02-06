CREATE TABLE IF NOT EXISTS SecurityTypes (
    [SecurityTypeID] INTEGER PRIMARY KEY AUTO_INCREMENT,
    [SecurityType] TEXT NOT NULL,
    UNIQUE(SecurityType)
)

CREATE TABLE IF NOT EXISTS SecurityExchanges (
    [ExchangeID] INTEGER PRIMARY KEY AUTO_INCREMENT,
    [Exchange] TEXT NOT NULL,
    UNIQUE(Exchange)
)

CREATE TABLE IF NOT EXISTS SecuritiesInfo(
    [SymbolID] INTEGER PRIMARY KEY AUTO_INCREMENT,
    [Symbol] TEXT,
    [SecurityTypeID] INTEGER NOT NULL,
    [ToInt] INTEGER NOT NULL,
    [ExchangeID] INTEGER NOT NULL,
    [RTHStartTimeUTC] TEXT,
    [RTHEndTimeUTC] TEXT,
    UNIQUE(Symbol, ExchangeID, SecurityTypeID),
    FOREIGN KEY (SecurityTypeID)
        REFERENCES SecurityTypes(SecurityTypeID),
    FOREIGN KEY (ExchangeID)
        REFERENCES SecurityExchanges(ExchangeID)
)