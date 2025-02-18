CREATE TABLE IF NOT EXISTS OrderActions (
    [action_id] INTEGER PRIMARY,
    [action_name] TEXT,
    UNIQUE (action_name)
)