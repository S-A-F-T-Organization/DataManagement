CREATE TABLE IF NOT EXISTS SecurityTypes (
    [SecurityTypeID] INTEGER PRIMARY KEY,
    [SecurityType] TEXT NOT NULL,
    UNIQUE(SecurityType)
)