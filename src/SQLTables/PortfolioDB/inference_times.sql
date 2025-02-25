CREATE TABLE IF NOT EXISTS inference_times (
    [inference_step_timing_id] INTEGER NOT NULL PRIMARY KEY,
    [inference_id] INTEGER NOT NULL,
    [inference_step_id] INTEGER NOT NULL,
    [step_start_timestamp_utc_ms] INTEGER NOT NULL,
    [step_end_timestamp_utc_ms] INTEGER NOT NULL,
    UNIQUE ([inference_id], [inference_step_id]),
    FOREIGN KEY ([inference_id])
        REFERENCES inferences ([inference_id])
);