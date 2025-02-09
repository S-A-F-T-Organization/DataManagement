CREATE TABLE IF NOT EXISTS StockSectors (
    [SectorID] INTEGER PRIMARY KEY,
    [SectorName] TEXT,
    UNIQUE (SectorName)
)

CREATE TABLE IF NOT EXISTS StockIndustries (
    [IndustryID] INTEGER PRIMARY KEY,
    [IndustryName] TEXT,
    UNIQUE (IndustryName)
)

CREATE TABLE IF NOT EXISTS StockMetadata (
    [SymbolID] INTEGER PRIMARY KEY,
    [FullName] TEXT,
    [SPComponent] INTEGER,
    [NQComponent] INTEGER,
    [DJComponent] INTEGER,
    [RTYComponent] INTEGER,
    [VIXComponent] INTEGER,
    [SectorID] INTEGER,
    [IndustryID] INTEGER,
    [IPODate] TEXT,
    FOREIGN KEY (SymbolID)
        REFERENCES SecuritiesInfo(SymbolID),
    FOREIGN KEY (SectorID)
        REFERENCES StockSectors(SectorID),
    FOREIGN KEY (IndustryID)
        REFERENCES StockIndustries(IndustryID)
)