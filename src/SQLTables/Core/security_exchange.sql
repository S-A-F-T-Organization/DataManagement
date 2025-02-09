CREATE TABLE IF NOT EXISTS SecurityExchanges (
    [ExchangeID] INTEGER PRIMARY KEY,
    [Exchange] TEXT NOT NULL,
    UNIQUE(Exchange)
)