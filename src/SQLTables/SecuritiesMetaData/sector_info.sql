CREATE TABLE IF NOT EXISTS SectorInfo (
    [sector_id] INTEGER PRIMARY KEY,
    [sector_name] TEXT,
    UNIQUE (sector_name)
)