CREATE TABLE IF NOT EXISTS SecuritiesInfo(
    [SymbolID] INTEGER PRIMARY KEY,
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