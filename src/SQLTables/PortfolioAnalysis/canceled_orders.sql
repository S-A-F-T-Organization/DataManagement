CREATE TABLE IF NOT EXISTS CanceledOrdersTable(
    [TransactionID] INTEGER PRIMARY KEY,
    [CanceledDatetime] INTEGER,
    FOREIGN KEY (TransactionID)
        REFERENCES AllOrdersTable(TransactionID)
)