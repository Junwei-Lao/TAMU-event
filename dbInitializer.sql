-- Create a new database
CREATE DATABASE testerDB;

-- Switch into the new database
\c testerDB;

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create the events table
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    event_title TEXT NOT NULL,
    event_date TEXT NOT NULL,
    event_url TEXT,
    event_summary TEXT,
    event_description TEXT,
    event_category TEXT,
    embedding vector(384) NOT NULL
);
