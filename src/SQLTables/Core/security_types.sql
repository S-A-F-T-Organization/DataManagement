CREATE TABLE IF NOT EXISTS SecurityTypes (
    [security_type_id] INTEGER PRIMARY KEY,
    [security_type] TEXT NOT NULL,
    UNIQUE(security_type)
)