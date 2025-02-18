
CREATE TABLE IF NOT EXISTS OrderTypes (
    [order_type_id] INTEGER PRIMARY,
    [order_type] TEXT,
    UNIQUE (order_type)
)