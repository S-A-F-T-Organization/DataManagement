CREATE OR ALTER TABLE OptionsOHLCV(
    [option_ohlcv_id] INTEGER NOT NULL PRIMARY KEY,
    [underlying_symbol_id] INTEGER NOT NULL,
    [timestamp_utc_ms] INTEGER NOT NULL,
    [strike_price] FLOAT NOT NULL,
    [option_type_id] INTEGER NOT NULL,
    [open_price] FLOAT NOT NULL,
    [high_price] FLOAT NOT NULL,
    [low_price] FLOAT NOT NULL,
    [close_price] FLOAT NOT NULL,
    [volume] INTEGER NOT NULL,
    UNIQUE([underlying_symbol_id], [timestamp_utc_ms], [strike_price], [option_type_id]),
    FOREIGN KEY([underlying_symbol_id])
        REFERENCES SecuritiesInfo([symbol_id])
);