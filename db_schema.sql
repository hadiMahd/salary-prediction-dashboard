-- 1. CORE PREDICTIONS TABLE
CREATE TABLE predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    work_year INTEGER NOT NULL,
    experience_level VARCHAR(10) NOT NULL CHECK (experience_level IN ('EN', 'MI', 'SE', 'EX')),
    employment_type VARCHAR(10) NOT NULL CHECK (employment_type IN ('FT', 'PT', 'CT', 'FL')),
    job_title VARCHAR(150) NOT NULL,
    company_size VARCHAR(10) NOT NULL CHECK (company_size IN ('S', 'M', 'L')),
    remote_ratio INTEGER NOT NULL CHECK (remote_ratio IN (0, 50, 100)),
    company_location VARCHAR(10) NOT NULL,
    predicted_salary NUMERIC(12, 2) NOT NULL,
    llm_narrative TEXT,
    chart_data JSONB,
    inference_latency_ms NUMERIC(6, 2),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. MODEL PERFORMANCE & TRANSPARENCY TABLE
CREATE TABLE model_performance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_version VARCHAR(50) NOT NULL,
    algorithm VARCHAR(50) DEFAULT 'RandomForestRegressor',
    r2_score NUMERIC(4,3),
    mae NUMERIC(8,2),
    rmse NUMERIC(8,2),
    feature_importance JSONB, -- e.g., {"experience_level": 0.35, "company_region": 0.22, ...}
    hyperparameters JSONB,
    training_date TIMESTAMPTZ DEFAULT NOW()
);

-- PERFORMANCE INDEXES
CREATE INDEX idx_predictions_created_at ON predictions(created_at DESC);
CREATE INDEX idx_predictions_experience ON predictions(experience_level);
CREATE INDEX idx_predictions_location ON predictions(company_location);

-- SUPABASE RLS (SECURITY)
ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public read access" ON predictions FOR SELECT USING (true);

ALTER TABLE model_performance ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public read access" ON model_performance FOR SELECT USING (true);