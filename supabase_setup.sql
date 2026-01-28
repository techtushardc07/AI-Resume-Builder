-- Supabase Table Setup for Learning Assistant
-- Run this SQL in your Supabase SQL Editor

CREATE TABLE IF NOT EXISTS student_sessions (
  id BIGSERIAL PRIMARY KEY,
  session_id TEXT UNIQUE NOT NULL,
  student_name TEXT,
  student_age INTEGER,
  learning_goal TEXT,
  track TEXT CHECK (track IN ('academic', 'skill', 'wellbeing')),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_session_id ON student_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_track ON student_sessions(track);
CREATE INDEX IF NOT EXISTS idx_created_at ON student_sessions(created_at);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_student_sessions_updated_at 
  BEFORE UPDATE ON student_sessions 
  FOR EACH ROW 
  EXECUTE FUNCTION update_updated_at_column();
