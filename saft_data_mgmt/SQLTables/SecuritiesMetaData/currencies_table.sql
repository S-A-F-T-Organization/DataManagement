CREATE TABLE IF NOT EXISTS Currencies (
    [CurrencyID] INTEGER PRIMARY,
    [CurrencyAbbr] TEXT,
    UNIQUE(CurrencyAbbr)
)