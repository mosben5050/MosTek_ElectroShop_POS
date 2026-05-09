"""User repository — all SQL operations on the users table.

The rest of the app uses these methods (find_by_username, create, etc.)
and never writes raw SQL against users. If we ever change the schema or
swap SQLite for another database, only this file changes.
"""
from typing import Optional, List
from datetime import datetime

from app.database.connection import get_connection
from app.models.user import User


class UserRepository:
    """Data access layer for the users table."""

    # ────────────────────────────────────────────────────────────
    # Read methods
    # ────────────────────────────────────────────────────────────
    def find_by_id(self, user_id: int) -> Optional[User]:
        """Return the user with this id, or None if not found."""
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE id = ?",
                (user_id,),
            ).fetchone()
        return self._row_to_user(row) if row else None

    def find_by_username(self, username: str) -> Optional[User]:
        """Return the user with this username (case-insensitive), or None."""
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE LOWER(username) = LOWER(?)",
                (username,),
            ).fetchone()
        return self._row_to_user(row) if row else None

    def list_all(self, active_only: bool = True) -> List[User]:
        """Return every user. By default, only active ones."""
        sql = "SELECT * FROM users"
        params = ()
        if active_only:
            sql += " WHERE is_active = 1"
        sql += " ORDER BY full_name COLLATE NOCASE"

        with get_connection() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [self._row_to_user(r) for r in rows]

    def count(self) -> int:
        """Return how many users exist in total (active + inactive)."""
        with get_connection() as conn:
            row = conn.execute("SELECT COUNT(*) AS n FROM users").fetchone()
        return row["n"] if row else 0

    # ────────────────────────────────────────────────────────────
    # Write methods
    # ────────────────────────────────────────────────────────────
    def create(self, user: User) -> User:
        """Insert a new user and return it with the assigned id.

        The user's password_hash must already be set — hashing happens
        in the service layer, not here.
        """
        if not user.password_hash:
            raise ValueError("Cannot create user without a password_hash")

        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO users (username, password_hash, full_name, role, is_active)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    user.username,
                    user.password_hash,
                    user.full_name,
                    user.role,
                    1 if user.is_active else 0,
                ),
            )
            conn.commit()
            user.id = cursor.lastrowid
        return user

    def update_last_login(self, user_id: int) -> None:
        """Stamp the user's last_login_at to right now."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with get_connection() as conn:
            conn.execute(
                "UPDATE users SET last_login_at = ? WHERE id = ?",
                (now, user_id),
            )
            conn.commit()

    def update_password_hash(self, user_id: int, new_hash: str) -> None:
        """Replace a user's password hash (for change-password flow)."""
        with get_connection() as conn:
            conn.execute(
                "UPDATE users SET password_hash = ? WHERE id = ?",
                (new_hash, user_id),
            )
            conn.commit()

    def set_active(self, user_id: int, is_active: bool) -> None:
        """Soft-deactivate a user without deleting their history."""
        with get_connection() as conn:
            conn.execute(
                "UPDATE users SET is_active = ? WHERE id = ?",
                (1 if is_active else 0, user_id),
            )
            conn.commit()

    # ────────────────────────────────────────────────────────────
    # Helpers
    # ────────────────────────────────────────────────────────────
    @staticmethod
    def _row_to_user(row) -> User:
        """Convert a sqlite3.Row into our User dataclass."""
        return User(
            id=row["id"],
            username=row["username"],
            password_hash=row["password_hash"],
            full_name=row["full_name"],
            role=row["role"],
            is_active=bool(row["is_active"]),
            created_at=row["created_at"],
            last_login_at=row["last_login_at"],
        )