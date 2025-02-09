CREATE TABLE IF NOT EXISTS StrategyInfoTable(
    [StrategyID] INTEGER PRIMARY KEY,
    [StrategyName] TEXT,
    [StrategyVersion] REAL,
    UNIQUE(StrategyName, StrategyVersion)
)