CREATE DATABASE eventsdb;

\c eventsdb;

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE eventsA (
    id SERIAL PRIMARY KEY,
    event_title TEXT NOT NULL,
    event_date TEXT NOT NULL,
    event_url TEXT,
    event_summary TEXT,
    event_description TEXT,
    event_category TEXT,
    embedding vector(384) NOT NULL
);

CREATE TABLE eventsB (
    id SERIAL PRIMARY KEY,
    event_title TEXT NOT NULL,
    event_date TEXT NOT NULL,
    event_url TEXT,
    event_summary TEXT,
    event_description TEXT,
    event_category TEXT,
    embedding vector(384) NOT NULL
);
