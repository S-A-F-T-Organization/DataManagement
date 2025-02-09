CREATE TABLE IF NOT EXISTS ModelInferenceTable(
    [InferenceID] INTEGER PRIMARY KEY,
    [SymbolID] INTEGER,
    [PredictedSentiment] INTEGER,
    [InferenceStartDatetime] INTEGER,
    [InferenceEndDatetime] INTEGER,
    [ConfidenceLevel] REAL,
    [ReferenceTimestamp] INTEGER,
    FOREIGN KEY (SymbolID)
        REFERENCES SecuritiesInfo(SymbolID)
)