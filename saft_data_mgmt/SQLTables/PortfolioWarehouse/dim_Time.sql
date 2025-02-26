CREATE OR ALTER TABLE dim_Time (
    [time_key] INTEGER NOT NULL,
    [time_since_midnight_ms] INTEGER NOT NULL,
    [time_hh_mm_ss] TIME NOT NULL,
    [hour] INTEGER NOT NULL,
    [minute] INTEGER NOT NULL,
    [second] INTEGER NOT NULL,
    [time_of_day] TEXT NOT NULL,
    PRIMARY KEY (time_key)
);