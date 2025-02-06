CREATE TABLE IF NOT EXISTS Issuers (
    [IssuerID] INTEGER PRIMARY KEY AUTO_INCREMENT,
    [IssuerName] TEXT,
    UNIQUE (IssuerName)
)

CREATE TABLE IF NOT EXISTS ETFMetadata(
    [SymbolID] INTEGER PRIMARY KEY,
    [FullName] TEXT,
    [UnderlyingAssetTypeID] INTEGER,
    [IssuerID] INTEGER,
    [UnderlyingAsset] TEXT,
    UNIQUE (SymbolID)
    FOREIGN KEY (IssuerID)
        REFERENCES Issuers(IssuerID),
    FOREIGN KEY (SymbolID)
        REFERENCES SecuritiesInfo(SymbolID)
)

