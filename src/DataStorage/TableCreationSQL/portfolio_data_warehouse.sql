CREATE TABLE IF NOT EXISTS StrategyInfoTable(
    [StrategyID] INTEGER PRIMARY KEY AUTO_INCREMENT,
    [StrategyName] TEXT,
    [StrategyVersion] REAL,
    UNIQUE(StrategyName, StrategyVersion)
)

CREATE TABLE IF NOT EXISTS ModelInferenceTable(
    [InferenceID] INTEGER PRIMARY KEY,
    [SymbolID] INTEGER,
    [PredictedSentiment] INTEGER,
    [InferenceStartDatetime] INTEGER,
    [InferenceEndDatetime] INTEGER,
    [ConfidenceLevel] REAL,
    [ReferenceTimestamp] INTEGER,
    FOREIGN KEY (SymbolID)
        REFERENCES SecuritiesInfo(SymbolID)
)

CREATE TABLE IF NOT EXISTS SessionTable(
    [SessionID] INTEGER PRIMARY KEY AUTO_INCREMENT,
    [DatetimeCreated] INTEGER,
    [DatetimeEnded] INTEGER,
    [DataReaderStartDatetime] INTEGER
)

CREATE TABLE IF NOT EXISTS AccountSummaryTable(
    [AccountID] INTEGER PRIMARY KEY,
    [AccountStartDatetime] INTEGER,
    [AccountStartValue] REAL,
    [AccountAlias] TEXT
)

CREATE TABLE IF NOT EXISTS TransactionTypesTable(
    [TransactionTypeID] INTEGER PRIMARY KEY AUTO_INCREMENT,
    [TransactionType] TEXT,
    UNIQUE (TransactionType)
)

CREATE TABLE IF NOT EXISTS TransactionsTable(
    [TransactionID] INTEGER PRIMARY KEY AUTO_INCREMENT,
    [AccountID] INTEGER,
    [TransactionTypeID] INTEGER,
    [TransactionDatetime] INTEGER,
    [TransactionValue] REAL,
    FOREIGN KEY (AccountID)
        REFERENCES AccountSummaryTable(AccountID),
    FOREIGN KEY (TransactionTypeID)
        REFERENCES TransactionTypesTable(TransactionTypeID)
)

CREATE TABLE IF NOT EXISTS OrderActions (
    [ActionID] INTEGER PRIMARY AUTO_INCREMENT,
    [ActionName] TEXT,
    UNIQUE (ActionName)
)

CREATE TABLE IF NOT EXISTS OrderTypes (
    [OrderTypeID] INTEGER PRIMARY AUTO_INCREMENT,
    [OrderType] TEXT,
    UNIQUE (OrderType)
)

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

CREATE TABLE IF NOT EXISTS CanceledOrdersTable(
    [TransactionID] INTEGER PRIMARY KEY,
    [CanceledDatetime] INTEGER,
    FOREIGN KEY (TransactionID)
        REFERENCES AllOrdersTable(TransactionID)
)

CREATE TABLE IF NOT EXISTS ExecutedOrdersTable(
    [TransactionID] INTEGER PRIMARY KEY,
    [ExecutedDatetime] INTEGER,
    [ExecutionPrice] REAL,
    [Fees] REAL,
    FOREIGN KEY (TransactionID)
        REFERENCES AllOrdersTable(TransactionID)
)