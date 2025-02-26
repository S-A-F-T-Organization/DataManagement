CREATE TABLE IF NOT EXISTS AllOrders (
    [order_id] INTEGER PRIMARY KEY,
    [symbol_id] INTEGER,
    [broker_order_id] INTEGER,
    [order_placed_datetime] INTEGER,
    [transaction_id] INTEGER,
    [order_type_id] INTEGER,
    [order_action_id] INTEGER,
    [inference_id] INTEGER,
    [quantity] INTEGER,
    UNIQUE (transaction_id),
    FOREIGN KEY (symbol_id)
        REFERENCES SecuritiesInfo(symbol_id),
    FOREIGN KEY (inference_id)
        REFERENCES Inferences(inference_id),
    FOREIGN KEY (transaction_id)
        REFERENCES Transactions(transaction_id),
    FOREIGN KEY (order_action_id)
        REFERENCES OrderActions(order_action_id),
    FOREIGN KEY (order_type_id)
        REFERENCES OrderTypes(order_type_id)
);