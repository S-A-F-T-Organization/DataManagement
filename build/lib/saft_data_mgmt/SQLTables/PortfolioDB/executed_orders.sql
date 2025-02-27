CREATE TABLE IF NOT EXISTS ExecutedOrdersTable(
    [order_id] INTEGER PRIMARY KEY,
    [execution_timestamp_utc_ms] INTEGER,
    [execution_price] REAL,
    [fees] REAL,
    FOREIGN KEY (order_id)
        REFERENCES AllOrders(order_id)
)