CREATE OR ALTER TABLE Models (
    [model_id] INTEGER PRIMARY KEY,
    [strategy_id] INTEGER NOT NULL,
    [model_name] TEXT NOT NULL,
    [model_type_id] INTEGER NOT NULL,
    [model_dvc_hash] TEXT NOT NULL,
    UNIQUE (model_dvc_hash),
    FOREIGN KEY (strategy_id)
        REFERENCES Strategies(strategy_id),
    FOREIGN KEY (model_type_id)
        REFERENCES ModelTypes(model_type_id)
)