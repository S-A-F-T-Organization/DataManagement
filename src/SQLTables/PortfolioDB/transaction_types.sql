CREATE TABLE IF NOT EXISTS TransactionTypes(
    [transaction_type_id] INTEGER PRIMARY KEY,
    [transaction_type] TEXT,
    UNIQUE (transaction_type)
);
