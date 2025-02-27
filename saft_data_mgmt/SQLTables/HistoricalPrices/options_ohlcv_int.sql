CREATE OR ALTER TABLE OptionsOHLCV(
    [option_ohlcv_id] INTEGER NOT NULL PRIMARY KEY,
    [underlying_symbol_id] INTEGER NOT NULL,
    [timestamp_utc_ms] INTEGER NOT NULL,
    [strike_price] INTEGER NOT NULL,
    [option_type_id] INTEGER NOT NULL,
    [open_price] INTEGER NOT NULL,
    [high_price] INTEGER NOT NULL,
    [low_price] INTEGER NOT NULL,
    [close_price] INTEGER NOT NULL,
    [volume] INTEGER NOT NULL,
    UNIQUE([underlying_symbol_id], [timestamp_utc_ms], [strike_price], [option_type_id]),
    FOREIGN KEY([underlying_symbol_id])
        REFERENCES SecuritiesInfo([symbol_id])
)