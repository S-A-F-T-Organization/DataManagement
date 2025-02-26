CREATE TABLE IF NOT EXISTS ConditionalOrders (
    [order_id] INTEGER PRIMARY KEY,
    [trigger_price] REAL NOT NULL,
    FOREIGN KEY ([order_id]) 
        REFERENCES AllOrders ([order_id])
)