CREATE TABLE IF NOT EXISTS ETFMetadata(
    [SymbolID] INTEGER PRIMARY KEY,
    [FullName] TEXT,
    [UnderlyingAssetTypeID] INTEGER,
    [IssuerID] INTEGER,
    [UnderlyingAsset] TEXT
)

CREATE TABLE IF NOT EXISTS Issuers (
    [IssuerID] INTEGER PRIMARY KEY AUTO_INCREMENT,
    [IssuerName] TEXT
)