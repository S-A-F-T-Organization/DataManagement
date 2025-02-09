CREATE TABLE IF NOT EXISTS TransactionTypesTable(
    [TransactionTypeID] INTEGER PRIMARY KEY,
    [TransactionType] TEXT,
    UNIQUE (TransactionType)
)
