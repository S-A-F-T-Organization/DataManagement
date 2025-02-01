CREATE TABLE PriceHistory (
    ObsID INTEGER PRIMARY KEY AUTOINCREMENT,
    [DateTime] INTEGER,
    SymbolID INTEGER,
    OpenPrice INTEGER,
    HighPrice INTEGER,
    LowPrice INTEGER,
    ClosePrice INTEGER,
    Volume INTEGER,
    FOREIGN KEY (SymbolID) REFERENCES SecuritiesInfo(SymbolID),
    UNIQUE ([DateTime], SymbolID)
);

CREATE TABLE SecuritiesInfo (
    SymbolID INTEGER PRIMARY KEY AUTOINCREMENT,
    Symbol TEXT,
    SecurityTypeID INTEGER,
    ToINTEGER INTEGER,
    UNIQUE (Symbol, SecurityTypeID)
);

CREATE TABLE SecurityTypes (
    SecurityTypeID INTEGER PRIMARY KEY AUTOINCREMENT,
    SecurityType TEXT,
    UNIQUE (SecurityType)
);

CREATE TABLE SecurityExchanges (
    ExchangeID INTEGER PRIMARY KEY AUTOINCREMENT,
    ExchangeName TEXT,
    UNIQUE (ExchangeName)
);

CREATE TABLE FuturesMetadata (
    SymbolID INTEGER PRIMARY KEY,
    Multiplier INTEGER,
    ExchangeID INTEGER,
    FOREIGN KEY (SymbolID) REFERENCES SecuritiesInfo(SymbolID),
    FOREIGN KEY (ExchangeID) REFERENCES SecurityExchanges(ExchangeID)
);

CREATE TABLE ForexMetadata (
    SymbolID INTEGER PRIMARY KEY,
    BaseCurrency TEXT,
    QuoteCurrency TEXT,
    FOREIGN KEY (SymbolID) REFERENCES SecuritiesInfo(SymbolID)
);

CREATE TABLE EquityMetadata (
    SymbolID INTEGER PRIMARY KEY,
    ExchangeID INTEGER,
    HasDividends INTEGER,
    EquityTypeID INTEGER,
    FOREIGN KEY (SymbolID) REFERENCES SecuritiesInfo(SymbolID),
    FOREIGN KEY (EquityTypeID) REFERENCES EquityTypes(EquityTypeID)
);

CREATE TABLE EquityTypes (
    EquityTypeID INTEGER PRIMARY KEY AUTOINCREMENT,
    TypeName TEXT,
    UNIQUE (TypeName)
);