CREATE TABLE IF NOT EXISTS Strategies(
    [strategy_id] INTEGER PRIMARY KEY,
    [strategy_name] TEXT,
    [strategy_version] TEXT,
    [strategy_description] TEXT,
    UNIQUE(strategy_name, strategy_version)
)