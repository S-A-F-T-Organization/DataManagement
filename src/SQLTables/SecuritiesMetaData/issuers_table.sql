CREATE TABLE IF NOT EXISTS Issuers (
    [issuer_id] INTEGER PRIMARY KEY,
    [issuer_name] TEXT,
    UNIQUE (issuer_name)
);