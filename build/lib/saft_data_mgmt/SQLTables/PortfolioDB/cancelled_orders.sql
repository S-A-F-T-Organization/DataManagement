CREATE TABLE IF NOT EXISTS CanceledOrders(
    [order_id] INTEGER PRIMARY KEY,
    [canceled_timestamp_utc_ms] INTEGER,
    FOREIGN KEY (order_id)
        REFERENCES AllOrders(order_id)
)