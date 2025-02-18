CREATE TABLE IF NOT EXISTS AllOrders (
    [order_id] INTEGER PRIMARY KEY,
    [transaction_id] INTEGER,
    [placed_datetime] INTEGER,
    [symbol_id] INTEGER,
    [order_type_id] INTEGER,
    [strategy_id] INTEGER,
    [session_id] INTEGER,
    [inference_id] INTEGER,
    [quantity] INTEGER,
    [action_id] INTEGER,
    UNIQUE (transaction_id),
    FOREIGN KEY (symbol_id)
        REFERENCES SecuritiesInfo(symbol_id),
    FOREIGN KEY (strategy_id)
        REFERENCES Strategies(strategy_id),
    FOREIGN KEY (session_id)
        REFERENCES Sessions(session_id),
    FOREIGN KEY (inference_id)
        REFERENCES Inferences(inference_id),
    FOREIGN KEY (transaction_id)
        REFERENCES Transactions(transaction_id),
    FOREIGN KEY (action_id)
        REFERENCES OrderActions(action_id),
    FOREIGN KEY (order_type_id)
        REFERENCES OrderTypes(order_type_id)
);