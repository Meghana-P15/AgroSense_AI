-- Run this after creating and connecting to the agrosense_ai database.
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    model_type VARCHAR(50) NOT NULL,
    input_data JSONB NOT NULL,
    output_data JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_predictions_model_type ON predictions(model_type);
CREATE INDEX IF NOT EXISTS ix_predictions_created_at ON predictions(created_at);
