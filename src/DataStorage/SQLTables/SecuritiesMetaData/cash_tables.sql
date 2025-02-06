CREATE TABLE IF NOT EXISTS Currencies (
    [CurrencyID] INTEGER PRIMARY AUTO_INCREMENT,
    [CurrencyAbbr] TEXT,
    UNIQUE(CurrencyAbbr)
)

CREATE TABLE IF NOT EXISTS ForexMetadata(
    [SymbolID] INTEGER PRIMARY KEY,
    [BaseCurrencyID] INTEGER,
    [QuoteCurrencyID] INTEGER,
    FOREIGN KEY (BaseCurrencyID)
        REFERENCES Currencies(CurrencyID),
    FOREIGN KEY (QuoteCurrencyID)
        REFERENCES Currencies(CurrencyID),
    FOREIGN KEY (SymbolID)
        REFERENCES SecuritiesInfo(SymbolID)
)

