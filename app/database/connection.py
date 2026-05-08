"""SQLite connection helper.

This module is the only place that knows *how* to talk to SQLite.
The rest of the app uses get_connection() and never imports sqlite3 directly.
"""
import sqlite3
from pathlib import Path
from app.config import DB_PATH, DATA_DIR

SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def ensure_database_exists() -> None:
    """Create the data folder and database file if they don't exist yet.

    Safe to call on every app start. If the DB already exists, this is a no-op.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    is_new = not DB_PATH.exists()

    conn = sqlite3.connect(DB_PATH)
    try:
        # Always enforce foreign keys for this connection
        conn.execute("PRAGMA foreign_keys = ON")

        if is_new:
            print(f"[DB] First run — creating database at {DB_PATH}")
            schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
            conn.executescript(schema_sql)
            conn.commit()
            print("[DB] Schema created successfully.")
        else:
            # Run schema with IF NOT EXISTS — safe even on existing DBs
            schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
            conn.executescript(schema_sql)
            conn.commit()
    finally:
        conn.close()


def get_connection() -> sqlite3.Connection:
    """Return a new SQLite connection with sensible defaults.

    Each part of the app should open its own short-lived connection,
    use it, and close it (use a `with` block).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    # Return rows as dict-like objects: row['name'] instead of row[0]
    conn.row_factory = sqlite3.Row
    return conn