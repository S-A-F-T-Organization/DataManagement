
CREATE TABLE IF NOT EXISTS OrderTypes (
    [OrderTypeID] INTEGER PRIMARY,
    [OrderType] TEXT,
    UNIQUE (OrderType)
)