CREATE TABLE IF NOT EXISTS ExecutedOrdersTable(
    [TransactionID] INTEGER PRIMARY KEY,
    [ExecutedDatetime] INTEGER,
    [ExecutionPrice] REAL,
    [Fees] REAL,
    FOREIGN KEY (TransactionID)
        REFERENCES AllOrdersTable(TransactionID)
)