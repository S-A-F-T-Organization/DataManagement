CREATE TABLE IF NOT EXISTS ForexMetadata(
    [SymbolID] INTEGER PRIMARY KEY,
    [BaseCurrencyID] INTEGER,
    [QuoteCurrencyID] INTEGER,
)

CREATE TABLE IF NOT EXISTS Currencies (
    [CurrencyID] INTEGER PRIMARY AUTO_INCREMENT,
    [CurrencyAbbr] TEXT
)