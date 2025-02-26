CREATE TABLE IF NOT EXISTS UnderlyingAssetTypes(
    [underlying_asset_type_id] INTEGER PRIMARY KEY,
    [underlying_asset_type] TEXT NOT NULL,
    UNIQUE (underlying_asset_type)
)