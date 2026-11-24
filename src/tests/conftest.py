
import sys
from pathlib import Path

import pytest
from werkzeug.security import generate_password_hash

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import create_app
from database import create_user, connect


@pytest.fixture
def app(tmp_path):
    db_path = str(tmp_path / "test.db")

    training_data = (
        Path(__file__).resolve().parents[1]
        / "sample_training_data.csv"
    )

    application = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-secret",
        "DATABASE": db_path,
        "TRAINING_DATA": str(training_data)
    })

    # Create test accounts before opening the connection
    # used for provider records.
    uid = create_user(
        db_path,
        "Test User",
        "user@example.com",
        "1112223333",
        "password123",
        "user"
    )

    pid = create_user(
        db_path,
        "Test Provider",
        "provider@example.com",
        "1112224444",
        "password123",
        "provider"
    )

    aid = create_user(
        db_path,
        "Admin",
        "admin@example.com",
        "1112225555",
        "password123",
        "admin"
    )

    # Add provider information using one database connection.
    with connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO providers
            (user_id, business_name, service_area, approved)
            VALUES (?, ?, ?, 1)
            """,
            (pid, "Test Plumbing", "Test City")
        )

        conn.execute(
            """
            INSERT INTO provider_categories
            (provider_id, category_id)
            SELECT ?, id
            FROM categories
            WHERE name = 'Plumbing'
            """,
            (pid,)
        )

    application.config["TEST_IDS"] = {
        "user": uid,
        "provider": pid,
        "admin": aid
    }

    yield application


@pytest.fixture
def client(app):
    return app.test_client()
