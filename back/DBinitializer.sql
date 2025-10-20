CREATE DATABASE eventsdb;
\c eventsdb;

CREATE EXTENSION IF NOT EXISTS vector;

CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE TABLE IF NOT EXISTS eventsa (
    id SERIAL PRIMARY KEY,
    event_title TEXT NOT NULL,
    event_dates TEXT NOT NULL,
    event_url TEXT,
    event_summary TEXT,
    event_description TEXT,
    event_category TEXT,
    embedding vector(384) NOT NULL
);

CREATE TABLE IF NOT EXISTS eventsb (
    id SERIAL PRIMARY KEY,
    event_title TEXT NOT NULL,
    event_dates TEXT NOT NULL,
    event_url TEXT,
    event_summary TEXT,
    event_description TEXT,
    event_category TEXT,
    embedding vector(384) NOT NULL
);


CREATE INDEX IF NOT EXISTS eventsa_text_idx
ON eventsA
USING gin (to_tsvector('english',
    coalesce(event_title, '') || ' ' ||
    coalesce(event_summary, '') || ' ' ||
    coalesce(event_description, '')
));

CREATE INDEX IF NOT EXISTS eventsb_text_idx
ON eventsB
USING gin (to_tsvector('english',
    coalesce(event_title, '') || ' ' ||
    coalesce(event_summary, '') || ' ' ||
    coalesce(event_description, '')
));


CREATE INDEX IF NOT EXISTS eventsa_trgm_idx
ON eventsA
USING gin (event_title gin_trgm_ops);

CREATE INDEX IF NOT EXISTS eventsb_trgm_idx
ON eventsB
USING gin (event_title gin_trgm_ops);


