CREATE TABLE IF NOT EXISTS OrderActions (
    [order_action_id] INTEGER PRIMARY,
    [order_action] TEXT,
    UNIQUE (order_action)
)