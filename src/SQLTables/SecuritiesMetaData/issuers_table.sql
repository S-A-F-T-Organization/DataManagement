CREATE TABLE IF NOT EXISTS Issuers (
    [IssuerID] INTEGER PRIMARY KEY,
    [IssuerName] TEXT,
    UNIQUE (IssuerName)
);