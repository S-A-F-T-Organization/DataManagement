CREATE TABLE IF NOT EXISTS InferenceSteps(
    [inference_step_id] INTEGER PRIMARY KEY,
    [module_id] INTEGER NOT NULL,
    [step_name] TEXT NOT NULL,
    UNIQUE([module_id], [step_name]),
    FOREIGN KEY([module_id])
        REFERENCES Modules([module_id])
)