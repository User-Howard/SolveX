-- SolveX Database Schema
-- PostgreSQL DDL

-- Drop tables if they exist (for clean recreation)
DROP TABLE IF EXISTS resource_tags CASCADE;
DROP TABLE IF EXISTS problem_tags CASCADE;
DROP TABLE IF EXISTS problem_relations CASCADE;
DROP TABLE IF EXISTS solution_resources CASCADE;
DROP TABLE IF EXISTS problem_resources CASCADE;
DROP TABLE IF EXISTS tags CASCADE;
DROP TABLE IF EXISTS resources CASCADE;
DROP TABLE IF EXISTS solutions CASCADE;
DROP TABLE IF EXISTS problems CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Problems table
CREATE TABLE problems (
    problem_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    problem_type VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    resolved BOOLEAN DEFAULT FALSE
);

-- Solutions table
CREATE TABLE solutions (
    solution_id SERIAL PRIMARY KEY,
    problem_id INTEGER NOT NULL REFERENCES problems(problem_id) ON DELETE CASCADE,
    parent_solution_id INTEGER REFERENCES solutions(solution_id) ON DELETE CASCADE,
    code_snippet TEXT NOT NULL,
    explanation TEXT,
    approach_type VARCHAR(100),
    version_number INTEGER DEFAULT 1,
    branch_type VARCHAR(50),
    improvement_description TEXT,
    success_rate FLOAT,
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT no_self_loop CHECK (solution_id != parent_solution_id),
    CONSTRAINT solution_success_rate_range CHECK (success_rate >= 0 AND success_rate <= 100)
);

-- Resources table
CREATE TABLE resources (
    resource_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    title VARCHAR(500),
    source_platform VARCHAR(50),
    content_summary TEXT,
    visit_count INTEGER DEFAULT 1,
    first_visited_at TIMESTAMP,
    last_visited_at TIMESTAMP,
    usefulness_score FLOAT,
    CONSTRAINT resource_usefulness_range CHECK (usefulness_score >= 0 AND usefulness_score <= 5)
);

-- Tags table
CREATE TABLE tags (
    tag_id SERIAL PRIMARY KEY,
    tag_name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50),
    description TEXT
);

-- Problem-Resource junction table
CREATE TABLE problem_resources (
    problem_id INTEGER NOT NULL REFERENCES problems(problem_id) ON DELETE CASCADE,
    resource_id INTEGER NOT NULL REFERENCES resources(resource_id) ON DELETE CASCADE,
    relevance_score FLOAT,
    contribution_type VARCHAR(50),
    added_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (problem_id, resource_id),
    CONSTRAINT problem_resource_relevance_range CHECK (relevance_score >= 0 AND relevance_score <= 1)
);

-- Solution-Resource junction table
CREATE TABLE solution_resources (
    solution_id INTEGER NOT NULL REFERENCES solutions(solution_id) ON DELETE CASCADE,
    resource_id INTEGER NOT NULL REFERENCES resources(resource_id) ON DELETE CASCADE,
    PRIMARY KEY (solution_id, resource_id)
);

-- Problem-Problem relation table
CREATE TABLE problem_relations (
    from_problem_id INTEGER NOT NULL REFERENCES problems(problem_id) ON DELETE CASCADE,
    to_problem_id INTEGER NOT NULL REFERENCES problems(problem_id) ON DELETE CASCADE,
    relation_type VARCHAR(50),
    strength FLOAT,
    PRIMARY KEY (from_problem_id, to_problem_id),
    CONSTRAINT problem_relation_strength_range CHECK (strength >= 0 AND strength <= 1),
    CONSTRAINT no_self_relation CHECK (from_problem_id != to_problem_id)
);

-- Problem-Tag junction table
CREATE TABLE problem_tags (
    problem_id INTEGER NOT NULL REFERENCES problems(problem_id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(tag_id) ON DELETE CASCADE,
    PRIMARY KEY (problem_id, tag_id)
);

-- Resource-Tag junction table
CREATE TABLE resource_tags (
    resource_id INTEGER NOT NULL REFERENCES resources(resource_id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(tag_id) ON DELETE CASCADE,
    confidence FLOAT,
    PRIMARY KEY (resource_id, tag_id),
    CONSTRAINT resource_tag_confidence_range CHECK (confidence >= 0 AND confidence <= 1)
);

-- Create indexes for better query performance
CREATE INDEX idx_problems_user_id ON problems(user_id);
CREATE INDEX idx_problems_created_at ON problems(created_at DESC);
CREATE INDEX idx_solutions_problem_id ON solutions(problem_id);
CREATE INDEX idx_solutions_parent_id ON solutions(parent_solution_id);
CREATE INDEX idx_solutions_created_at ON solutions(created_at DESC);
CREATE INDEX idx_resources_user_id ON resources(user_id);
CREATE INDEX idx_resources_last_visited ON resources(last_visited_at DESC);
CREATE INDEX idx_problem_resources_resource_id ON problem_resources(resource_id);
CREATE INDEX idx_solution_resources_resource_id ON solution_resources(resource_id);
CREATE INDEX idx_problem_relations_to ON problem_relations(to_problem_id);
CREATE INDEX idx_problem_tags_tag_id ON problem_tags(tag_id);
CREATE INDEX idx_resource_tags_tag_id ON resource_tags(tag_id);
