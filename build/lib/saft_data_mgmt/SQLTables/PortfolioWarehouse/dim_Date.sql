CREATE OR ALTER TABLE dim_date (
    [date_key] INTEGER NOT NULL,
    [date_mm_dd_yyyy] DATE NOT NULL,
    [day_of_week] VARCHAR(9) NOT NULL,
    [day_of_month] INTEGER NOT NULL,
    [day_of_year] INTEGER NOT NULL,
    [month] INTEGER NOT NULL,
    [quarter] INTEGER NOT NULL,
    [year] INTEGER NOT NULL,
    [is_weekend] INTEGER NOT NULL,
    [is_holiday] INTEGER NOT NULL,
    [midnight_utc_sec] INTEGER NOT NULL,
    PRIMARY KEY (date_key)
);