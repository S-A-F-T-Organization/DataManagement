CREATE TABLE IF NOT EXISTS Inferences(
    [inference_id] INTEGER PRIMARY KEY,
    [symbol_id] INTEGER,
    [strategy_id] INTEGER,
    [session_id] INTEGER,
    [inference_outputs] INTEGER,
    [inference_start_timestamp_utc_ms] INTEGER,
    [inference_end_timestamp_utc_ms] INTEGER,
    [candle_reference_timestamp_utc_sec] INTEGER,
    [inference_status] TEXT,
    UNIQUE (symbol_id, strategy_id, session_id),
    FOREIGN KEY (symbol_id)
        REFERENCES SecuritiesInfo(symbol_id)
)