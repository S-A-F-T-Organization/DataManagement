CREATE TABLE IF NOT EXISTS TransactionsTable(
    [TransactionID] INTEGER PRIMARY KEY,
    [AccountID] INTEGER,
    [TransactionTypeID] INTEGER,
    [TransactionDatetime] INTEGER,
    [TransactionValue] REAL,
    FOREIGN KEY (AccountID)
        REFERENCES AccountSummaryTable(AccountID),
    FOREIGN KEY (TransactionTypeID)
        REFERENCES TransactionTypesTable(TransactionTypeID)
)