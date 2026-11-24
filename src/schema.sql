-- The application creates and updates these tables through database.init_db().
-- This file is retained as a readable database design reference.
CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE, phone TEXT, password_hash TEXT, role TEXT, active INTEGER, created_at TEXT);
CREATE TABLE providers (user_id INTEGER PRIMARY KEY, business_name TEXT, service_area TEXT, bio TEXT, availability TEXT, approved INTEGER);
CREATE TABLE categories (id INTEGER PRIMARY KEY, name TEXT UNIQUE, active INTEGER);
CREATE TABLE provider_categories (provider_id INTEGER, category_id INTEGER, PRIMARY KEY(provider_id,category_id));
CREATE TABLE service_requests (id INTEGER PRIMARY KEY, user_id INTEGER, provider_id INTEGER, description TEXT, item_details TEXT, service_area TEXT, predicted_category TEXT, final_category TEXT, confidence REAL, status TEXT, provider_notes TEXT, created_at TEXT, updated_at TEXT);
CREATE TABLE feedback (id INTEGER PRIMARY KEY, request_id INTEGER UNIQUE, user_id INTEGER, rating INTEGER, comment TEXT, created_at TEXT);
