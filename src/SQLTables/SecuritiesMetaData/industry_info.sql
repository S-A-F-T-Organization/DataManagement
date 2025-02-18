CREATE TABLE IF NOT EXISTS industry_info (
    [industry_id] INTEGER PRIMARY KEY,
    [industry_name] TEXT,
    UNIQUE (industry_name)
)