-- ============================================
-- Job Aggregator - PostgreSQL Schema
-- For Supabase / PostgreSQL Database
-- ============================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- Table: jobs
-- Stores job listings from various sources
-- ============================================
CREATE TABLE IF NOT EXISTS jobs (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    description TEXT,
    salary_min BIGINT,
    salary_max BIGINT,
    apply_url VARCHAR(500) NOT NULL,
    source VARCHAR(100),
    
    -- AI-processed fields
    skills JSONB DEFAULT '[]'::jsonb,
    experience_level VARCHAR(50),
    is_remote BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for jobs table
CREATE INDEX IF NOT EXISTS idx_jobs_created_at ON jobs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_jobs_title ON jobs(title);
CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company);
CREATE INDEX IF NOT EXISTS idx_jobs_location ON jobs(location);
CREATE INDEX IF NOT EXISTS idx_jobs_salary ON jobs(salary_min, salary_max);
CREATE INDEX IF NOT EXISTS idx_jobs_experience_level ON jobs(experience_level);
CREATE INDEX IF NOT EXISTS idx_jobs_is_remote ON jobs(is_remote);

-- GIN index for JSONB skills array (for efficient contains queries)
CREATE INDEX IF NOT EXISTS idx_jobs_skills ON jobs USING GIN(skills);

-- ============================================
-- Table: users_preferences
-- Stores user job search preferences
-- ============================================
CREATE TABLE IF NOT EXISTS users_preferences (
    id BIGSERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL UNIQUE,
    
    -- Search preferences
    keywords JSONB DEFAULT '[]'::jsonb,
    preferred_locations JSONB DEFAULT '[]'::jsonb,
    min_salary BIGINT,
    max_salary BIGINT,
    experience_levels JSONB DEFAULT '[]'::jsonb,
    remote_only BOOLEAN DEFAULT FALSE,
    
    -- Notification settings
    email_notifications BOOLEAN DEFAULT TRUE,
    push_notifications BOOLEAN DEFAULT TRUE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for users_preferences table
CREATE INDEX IF NOT EXISTS idx_users_preferences_user_id ON users_preferences(user_id);
CREATE INDEX IF NOT EXISTS idx_users_preferences_min_salary ON users_preferences(min_salary);

-- ============================================
-- Trigger: Auto-update updated_at timestamp
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to jobs table
DROP TRIGGER IF EXISTS update_jobs_updated_at ON jobs;
CREATE TRIGGER update_jobs_updated_at
    BEFORE UPDATE ON jobs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Apply trigger to users_preferences table
DROP TRIGGER IF EXISTS update_users_preferences_updated_at ON users_preferences;
CREATE TRIGGER update_users_preferences_updated_at
    BEFORE UPDATE ON users_preferences
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- Sample Data (Optional - for testing)
-- ============================================
INSERT INTO jobs (title, company, location, description, salary_min, salary_max, apply_url, source, skills, experience_level, is_remote)
VALUES 
    ('Senior Backend Developer', 'Tech Startup Indonesia', 'Jakarta, Indonesia', 
     'Kami mencari Senior Backend Developer dengan pengalaman Python/FastAPI untuk membangun sistem scalable.', 
     15000000, 25000000, 'https://example.com/apply/1', 'manual',
     '["Python", "FastAPI", "PostgreSQL", "Docker"]'::jsonb, 'senior', false),
    
    ('Data Analyst', 'E-Commerce Giant', 'Remote', 
     'Posisi Data Analyst untuk tim analytics. SQL dan Python required untuk analisis data besar.',
     10000000, 18000000, 'https://example.com/apply/2', 'manual',
     '["SQL", "Python", "Tableau", "Excel"]'::jsonb, 'mid', true),
    
    ('Flutter Mobile Developer', 'Fintech Company', 'Bandung, Indonesia',
     'Develop mobile apps menggunakan Flutter untuk iOS dan Android platform.',
     12000000, 20000000, 'https://example.com/apply/3', 'manual',
     '["Flutter", "Dart", "Firebase", "REST API"]'::jsonb, 'mid', false)
ON CONFLICT DO NOTHING;

-- ============================================
-- Useful Queries (Reference)
-- ============================================

-- Get jobs with salary filter
-- SELECT * FROM jobs WHERE salary_min >= 10000000 ORDER BY created_at DESC;

-- Get remote jobs only
-- SELECT * FROM jobs WHERE is_remote = TRUE ORDER BY created_at DESC;

-- Search jobs by skill (using JSONB contains)
-- SELECT * FROM jobs WHERE skills ? 'Python';

-- Get jobs matching user preferences
-- SELECT j.* FROM jobs j
-- CROSS JOIN users_preferences up
-- WHERE up.user_id = 'user123'
-- AND (up.min_salary IS NULL OR j.salary_min >= up.min_salary)
-- AND (up.remote_only = FALSE OR j.is_remote = TRUE);
