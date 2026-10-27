-- Optional SQLite setup script for the Local Service Problem Diagnosis
-- and Matching System.
--
-- IMPORTANT: Check the table and column names against app.py and the existing
-- service_requests.db before using this script. Do not run it over a database
-- you need to preserve without first making a backup.

CREATE TABLE IF NOT EXISTS service_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    confidence REAL,
    status TEXT NOT NULL DEFAULT 'New',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
