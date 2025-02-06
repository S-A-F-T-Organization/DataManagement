CREATE TABLE IF NOT EXISTS AllOrdersTable(
    [TransactionID] INTEGER PRIMARY KEY,
    [PlacedDatetime] INTEGER,
    [SymbolID] INTEGER,
    [OrderType] TEXT,
    [StrategyID] INTEGER,
    [SessionID] INTEGER,
    [InferenceID] INTEGER
)

CREATE TABLE IF NOT EXISTS CanceledOrdersTable(
    [TransactionID] INTEGER PRIMARY KEY,
    [CanceledDatetime] INTEGER,
)

CREATE TABLE IF NOT EXISTS ExecutedOrdersTable(
    [TransactionID] INTEGER PRIMARY KEY,
    [ExecutedDatetime] INTEGER,
    [ExecutionPrice] REAL,
    [Fees] REAL
)

CREATE TABLE IF NOT EXISTS TransactionsTable(
    [TransactionID] INTEGER PRIMARY KEY AUTO_INCREMENT,
    [AccountID] INTEGER,
    [TransactionTypeID] INTEGER,
    [TransactionDatetime] INTEGER,
    [TransactionValue] REAL
)

CREATE TABLE IF NOT EXISTS AccountSummaryTable(
    [AccountID] INTEGER PRIMARY KEY,
    [AccountStartDatetime] INTEGER,
    [AccountStartValue] REAL,
    [AccountAlias] TEXT
)

CREATE TABLE IF NOT EXISTS TransactionTypesTable(
    [TransactionTypeID] INTEGER PRIMARY KEY AUTO_INCREMENT,
    [TransactionType] TEXT
)

CREATE TABLE IF NOT EXISTS SessionTable(
    [SessionID] INTEGER PRIMARY KEY AUTO_INCREMENT,
    [DatetimeCreated] INTEGER,
    [DatetimeEnded] INTEGER,
    [DataReaderStartDatetime] INTEGER
)

CREATE TABLE IF NOT EXISTS ModelInferenceTable(
    [InferenceID] INTEGER PRIMARY KEY,
    [SymbolID] INTEGER,
    [PredictedSentiment] INTEGER,
    [InferenceStartDatetime] INTEGER,
    [InferenceEndDatetime] INTEGER,
    [ConfidenceLevel] REAL,
    [ReferenceTimestamp] INTEGER
)

/*
-- This table is generated programmatically using a dictionary of features/datatypes provided by the user
CREATE TABLE IF NOT EXISTS InputFeaturesTable(
    [InferenceID] INTEGER PRIMARY KEY,
)
*/
CREATE TABLE IF NOT EXISTS StrategyInfoTable(
    [StrategyID] INTEGER PRIMARY KEY AUTO_INCREMENT,
    [StrategyName] TEXT,
    [StrategyVersion] REAL
)