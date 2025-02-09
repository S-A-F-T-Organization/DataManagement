CREATE TABLE IF NOT EXISTS AllOrdersTable (
    [TransactionID] INTEGER PRIMARY KEY,
    [PlacedDatetime] INTEGER,
    [SymbolID] INTEGER,
    [OrderTypeID] INTEGER,
    [StrategyID] INTEGER,
    [SessionID] INTEGER,
    [InferenceID] INTEGER,
    [SecQuantity] INTEGER,
    [ActionID] INTEGER,
    FOREIGN KEY (SymbolID)
        REFERENCES SecuritiesInfo(SymbolID),
    FOREIGN KEY (StrategyID)
        REFERENCES StrategyInfoTable(StrategyID),
    FOREIGN KEY (SessionID)
        REFERENCES SessionTable(SessionID),
    FOREIGN KEY (InferenceID)
        REFERENCES ModelInferenceTable(InferenceID),
    FOREIGN KEY (TransactionID)
        REFERENCES TransactionsTable(TransactionID)
    FOREIGN KEY (ActionID)
        REFERENCES OrderActions(ActionID)
    FOREIGN KEY (OrderTypeID)
        REFERENCES OrderTypes(OrderTypeID)
    
);