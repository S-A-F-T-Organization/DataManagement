CREATE TABLE IF NOT EXISTS ForexMetadata(
    [symbol_id] INTEGER PRIMARY KEY,
    [base_currency_id] INTEGER,
    [quote_currency_id] INTEGER,
    FOREIGN KEY (base_currency_id)
        REFERENCES Currencies(currency_id),
    FOREIGN KEY (quote_currency_id)
        REFERENCES Currencies(currency_id),
    FOREIGN KEY (symbol_id)
        REFERENCES SecuritiesInfo(symnbol_id)
)