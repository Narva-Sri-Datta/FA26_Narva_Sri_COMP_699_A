
import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash


CATEGORIES = [
    "Plumbing",
    "Electrical",
    "Appliance Repair",
    "Carpentry",
    "Painting",
    "Cleaning",
    "Other"
]


def connect(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    db = sqlite3.connect(path, timeout=30)
    db.row_factory = sqlite3.Row

    db.execute("PRAGMA foreign_keys = ON")
    db.execute("PRAGMA busy_timeout = 30000")

    return db


def init_db(path):
    with connect(path) as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL
                    CHECK(role IN ('user', 'provider', 'admin')),
                active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                active INTEGER NOT NULL DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS providers (
                user_id INTEGER PRIMARY KEY
                    REFERENCES users(id) ON DELETE CASCADE,
                business_name TEXT NOT NULL,
                service_area TEXT NOT NULL,
                bio TEXT DEFAULT '',
                availability TEXT NOT NULL DEFAULT 'Available',
                approved INTEGER NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS provider_categories (
                provider_id INTEGER NOT NULL
                    REFERENCES providers(user_id) ON DELETE CASCADE,
                category_id INTEGER NOT NULL
                    REFERENCES categories(id),
                PRIMARY KEY(provider_id, category_id)
            );

            CREATE TABLE IF NOT EXISTS service_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id),
                provider_id INTEGER REFERENCES users(id),
                description TEXT NOT NULL,
                item_details TEXT DEFAULT '',
                service_area TEXT DEFAULT '',
                predicted_category TEXT NOT NULL,
                final_category TEXT NOT NULL,
                confidence REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'Submitted',
                provider_notes TEXT DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id INTEGER NOT NULL UNIQUE
                    REFERENCES service_requests(id) ON DELETE CASCADE,
                user_id INTEGER NOT NULL REFERENCES users(id),
                rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
                comment TEXT DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_requests_user
                ON service_requests(user_id);

            CREATE INDEX IF NOT EXISTS idx_requests_provider
                ON service_requests(provider_id);

            CREATE INDEX IF NOT EXISTS idx_categories_name
                ON categories(name);
        """)

        for name in CATEGORIES:
            db.execute(
                "INSERT OR IGNORE INTO categories(name) VALUES (?)",
                (name,)
            )


def create_user(path, name, email, phone, password, role):
    with connect(path) as db:
        cur = db.execute(
            """
            INSERT INTO users
            (name, email, phone, password_hash, role)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                name.strip(),
                email.strip().lower(),
                phone.strip(),
                generate_password_hash(password),
                role
            )
        )

        return cur.lastrowid


def get_categories(path, active_only=False):
    """
    Return category records from the database.
    Each record contains id, name, and active.
    """
    with connect(path) as db:
        if active_only:
            rows = db.execute(
                """
                SELECT id, name, active
                FROM categories
                WHERE active = 1
                ORDER BY name
                """
            ).fetchall()
        else:
            rows = db.execute(
                """
                SELECT id, name, active
                FROM categories
                ORDER BY name
                """
            ).fetchall()

        return [dict(row) for row in rows]


def add_category(path, name):
    name = name.strip()

    if not name:
        raise ValueError("Category name is required.")

    with connect(path) as db:
        db.execute(
            "INSERT INTO categories(name) VALUES (?)",
            (name,)
        )


def update_category(path, category_id, name):
    name = name.strip()

    if not name:
        raise ValueError("Category name is required.")

    with connect(path) as db:
        cursor = db.execute(
            """
            UPDATE categories
            SET name = ?
            WHERE id = ?
            """,
            (name, category_id)
        )

        return cursor.rowcount > 0


def set_category_active(path, category_id, active):
    with connect(path) as db:
        cursor = db.execute(
            """
            UPDATE categories
            SET active = ?
            WHERE id = ?
            """,
            (int(bool(active)), category_id)
        )

        return cursor.rowcount > 0


def delete_category(path, category_id):
    with connect(path) as db:
        cursor = db.execute(
            "DELETE FROM categories WHERE id = ?",
            (category_id,)
        )

        return cursor.rowcount > 0


def row_dict(row):
    return dict(row) if row else None
