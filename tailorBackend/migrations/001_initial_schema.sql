-- Initial Database Schema for Tailor Backend
-- This SQL file provides a reference implementation
-- Prisma will handle migrations automatically, but this is useful for understanding the schema

-- Create enum type for job status
CREATE TYPE job_status AS ENUM ('PENDING', 'COMPLETED', 'FAILED');

-- Create users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    name VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create resumes table
CREATE TABLE resumes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    file_path TEXT NOT NULL,
    original_filename VARCHAR(255),
    parsed_text TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create jobs table (core entity)
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    resume_id UUID REFERENCES resumes(id) ON DELETE SET NULL,
    title VARCHAR(255),
    company_name VARCHAR(255),
    job_description TEXT,
    tailored_resume_text TEXT,
    status job_status DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX idx_resumes_user_id ON resumes(user_id);
CREATE INDEX idx_jobs_user_id ON jobs(user_id);
CREATE INDEX idx_jobs_resume_id ON jobs(resume_id);
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_users_email ON users(email);

-- Add comments for documentation
COMMENT ON TABLE users IS 'Stores user accounts and authentication information';
COMMENT ON TABLE resumes IS 'Stores uploaded resumes that can be reused across multiple jobs';
COMMENT ON TABLE jobs IS 'Core entity representing a tailoring session - combines user, resume, job description, and tailored result';

COMMENT ON COLUMN jobs.status IS 'Tracks the progress of the tailoring job: PENDING, COMPLETED, or FAILED';
COMMENT ON COLUMN jobs.tailored_resume_text IS 'The tailored resume content';
COMMENT ON COLUMN jobs.job_description IS 'The target job posting or description provided by the user';

