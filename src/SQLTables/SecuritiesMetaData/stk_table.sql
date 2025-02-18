CREATE TABLE IF NOT EXISTS StockMetadata (
    symbol_id INTEGER PRIMARY KEY,
    full_name TEXT,
    sp_component INTEGER,
    nq_component INTEGER,
    djia_component INTEGER,
    rty_component INTEGER,
    sector_id INTEGER,
    industry_id INTEGER,
    ipo_date_utc_sec INTEGER,
    FOREIGN KEY (symbol_id)
        REFERENCES SecuritiesInfo(symbol_id),
    FOREIGN KEY (sector_id)
        REFERENCES SectorInfo(sector_id),
    FOREIGN KEY (industry_id)
        REFERENCES IndustryInfo(industry_id)
);