CREATE OR ALTER TABLE StrategyModules(
    [module_id] INTEGER PRIMARY KEY,
    [strategy_id] INTEGER NOT NULL,
    [module_name] TEXT NOT NULL,
    UNIQUE([strategy_id], [module_name]),
    FOREIGN KEY([strategy_id])
        REFERENCES Strategies([strategy_id])
)