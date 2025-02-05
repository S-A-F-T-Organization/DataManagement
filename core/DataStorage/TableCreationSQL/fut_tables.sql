CREATE TABLE IF NOT EXISTS FuturesMetadata(
    [SymbolID] INTEGER PRIMARY KEY,
    [ExchangeID] INTEGER,
    [Multiplier] REAL,
    [TickSize] REAL,
    [TickValue] REAL,
    [UnderlyingAssetTypeID] INTEGER,
    [UnderlyingAsset] TEXT,
)