CREATE TABLE IF NOT EXISTS ETFMetadata (
    [symbol_id] INTEGER PRIMARY KEY,
    [full_name] TEXT,
    [underlying_asset_type_id] INTEGER,
    [issuer_id] INTEGER,
    [underlying_asset_name] TEXT,
    UNIQUE (symbol_id),
    FOREIGN KEY (issuer_id)
        REFERENCES Issuers(issuer_id),
    FOREIGN KEY (symbol_id)
        REFERENCES SecuritiesInfo(symbol_id)
    FOREIGN KEY (underlying_asset_type_id)
        REFERENCES UnderlyingTypes(asset_type_id)
);