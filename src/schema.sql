CREATE TABLE IF NOT EXISTS service_requests (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 description TEXT NOT NULL,
 predicted_category TEXT NOT NULL,
 final_category TEXT NOT NULL,
 confidence REAL NOT NULL,
 status TEXT NOT NULL DEFAULT 'Submitted',
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
