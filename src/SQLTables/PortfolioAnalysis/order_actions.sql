CREATE TABLE IF NOT EXISTS OrderActions (
    [ActionID] INTEGER PRIMARY,
    [ActionName] TEXT,
    UNIQUE (ActionName)
)