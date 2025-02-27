CREATE TABLE IF NOT EXISTS Currencies (
    [currency_id] INTEGER PRIMARY,
    [currency_abbr] TEXT,
    UNIQUE(currency_abbr)
)