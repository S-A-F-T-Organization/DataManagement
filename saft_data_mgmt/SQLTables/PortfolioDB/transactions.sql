CREATE TABLE IF NOT EXISTS Transactions(
    [transaction_id] INTEGER PRIMARY KEY,
    [account_id] INTEGER,
    [transaction_type_id] INTEGER,
    [transaction_timestamp_utc_ms] INTEGER,
    [transaction_value] REAL,
    FOREIGN KEY (account_id)
        REFERENCES AccountInfo(account_id),
    FOREIGN KEY (transaction_type_id)
        REFERENCES TransactionTypes(transaction_type_id)
)