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
    [IPODate] TEXT
)

CREATE TABLE IF NOT EXISTS StockSectors (
    [SectorID] INTEGER PRIMARY KEY AUTO_INCREMENT,
    [SectorName] TEXT
)

CREATE TABLE IF NOT EXISTS StockIndustries (
    [IndustryID] INTEGER PRIMARY KEY AUTO_INCREMENT,
    [IndustryName] TEXT
)
