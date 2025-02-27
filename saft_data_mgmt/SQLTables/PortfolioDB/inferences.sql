CREATE TABLE IF NOT EXISTS Inferences(
    [inference_id] INTEGER PRIMARY KEY,
    [symbol_id] INTEGER,
    [strategy_id] INTEGER,
    [session_id] INTEGER,
    [inference_outputs] INTEGER,
    [inference_start_timestamp_utc_ms] INTEGER,
    [inference_end_timestamp_utc_ms] INTEGER,
    [candle_reference_timestamp_utc_sec] INTEGER,
    UNIQUE (symbol_id, strategy_id, session_id, candle_reference_timestamp_utc_sec),
    FOREIGN KEY (symbol_id)
        REFERENCES SecuritiesInfo(symbol_id)
    FOREIGN KEY (strategy_id)
        REFERENCES Strategies(strategy_id)
    FOREIGN KEY (session_id)
        REFERENCES Sessions(session_id)
)