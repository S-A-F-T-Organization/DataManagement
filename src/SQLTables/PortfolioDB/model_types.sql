CREATE OR ALTER TABLE ModelTypes (
    model_type_id INTEGER PRIMARY KEY,
    model_type TEXT NOT NULL,
    model_library_id INTEGER NOT NULL,
    UNIQUE (model_type, model_library_id),
    FOREIGN KEY (model_library_id)
        REFERENCES ModelLibraries(model_library_id)
);