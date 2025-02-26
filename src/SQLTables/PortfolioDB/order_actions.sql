CREATE TABLE IF NOT EXISTS OrderActions (
    [order_action_id] INTEGER PRIMARY KEY,
    [order_action] TEXT,
    UNIQUE (order_action)
);