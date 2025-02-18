CREATE OR ALTER TABLE MutualFundSnapshots (
    [snapshot_id] INT PRIMARY KEY,
    [nav] REAL NOT NULL,
    [expense_ratio] REAL NOT NULL,
    [ytd_return] REAL NOT NULL,
    FOREIGN KEY ([snapshot_id])
        REFERENCES Snapshots([snapshot_id])
)