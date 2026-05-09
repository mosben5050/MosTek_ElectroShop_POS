"""Authentication service — login, password hashing, password changes.

This is where the business rules live. The UI calls these methods and
gets back clean results — never raw SQL, never bcrypt internals.
"""
from typing import Optional
import bcrypt

from app.models.user import User
from app.repositories.user_repo import UserRepository


class AuthService:
    """Handles user authentication and password management."""

    def __init__(self, user_repo: Optional[UserRepository] = None):
        # Allowing the repo to be injected makes this class testable
        # (we can pass in a mock repo in unit tests later).
        self._users = user_repo or UserRepository()

    # ────────────────────────────────────────────────────────────
    # Password hashing primitives
    # ────────────────────────────────────────────────────────────
    @staticmethod
    def hash_password(plain_password: str) -> str:
        """Hash a plain password using bcrypt.

        bcrypt automatically generates and embeds a per-password salt,
        so two users with the same password get different hashes.
        Returns a string suitable for storing in the password_hash column.
        """
        if not plain_password:
            raise ValueError("Password cannot be empty")

        # bcrypt works in bytes; we encode/decode for our string API.
        # The 'rounds' parameter controls how slow hashing is (higher =
        # more secure but slower login). 12 is the current industry default.
        hashed_bytes = bcrypt.hashpw(
            plain_password.encode("utf-8"),
            bcrypt.gensalt(rounds=12),
        )
        return hashed_bytes.decode("utf-8")

    @staticmethod
    def verify_password(plain_password: str, stored_hash: str) -> bool:
        """Return True if the plain password matches the stored hash."""
        if not plain_password or not stored_hash:
            return False
        try:
            return bcrypt.checkpw(
                plain_password.encode("utf-8"),
                stored_hash.encode("utf-8"),
            )
        except (ValueError, TypeError):
            # Malformed hash — treat as failed verification
            return False

    # ────────────────────────────────────────────────────────────
    # Authentication
    # ────────────────────────────────────────────────────────────
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Return the User if credentials are valid, else None.

        We deliberately do NOT distinguish between "no such user" and
        "wrong password" in the return value — leaking that information
        would let attackers enumerate usernames.
        """
        if not username or not password:
            return None

        user = self._users.find_by_username(username.strip())
        if user is None:
            return None

        if not user.is_active:
            return None

        if not self.verify_password(password, user.password_hash or ""):
            return None

        # Successful login — update last_login_at
        self._users.update_last_login(user.id)
        return user

    # ────────────────────────────────────────────────────────────
    # User creation
    # ────────────────────────────────────────────────────────────
    def create_user(
        self,
        username: str,
        password: str,
        full_name: str,
        role: str = "cashier",
    ) -> User:
        """Create a new user with a hashed password.

        Raises ValueError if username already exists or input is invalid.
        """
        username = username.strip()
        full_name = full_name.strip()

        # Basic input validation
        if not username:
            raise ValueError("Username is required")
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not full_name:
            raise ValueError("Full name is required")
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        if role not in ("admin", "cashier", "technician"):
            raise ValueError(f"Invalid role: {role}")

        # Uniqueness check
        if self._users.find_by_username(username) is not None:
            raise ValueError(f"Username '{username}' is already taken")

        # All good — create the user
        new_user = User(
            id=None,
            username=username,
            full_name=full_name,
            role=role,
            is_active=True,
            password_hash=self.hash_password(password),
        )
        return self._users.create(new_user)

    # ────────────────────────────────────────────────────────────
    # First-run check
    # ────────────────────────────────────────────────────────────
    def has_any_users(self) -> bool:
        """Return True if at least one user exists in the database.

        Used at startup to decide whether to show the first-run setup
        wizard instead of the login page.
        """
        return self._users.count() > 0

    # ────────────────────────────────────────────────────────────
    # Password change
    # ────────────────────────────────────────────────────────────
    def change_password(
        self,
        user_id: int,
        old_password: str,
        new_password: str,
    ) -> bool:
        """Change a user's password. Returns True on success.

        Verifies the old password before allowing the change.
        Raises ValueError if the new password is too weak.
        """
        if len(new_password) < 6:
            raise ValueError("New password must be at least 6 characters")

        user = self._users.find_by_id(user_id)
        if user is None:
            return False

        if not self.verify_password(old_password, user.password_hash or ""):
            return False

        new_hash = self.hash_password(new_password)
        self._users.update_password_hash(user_id, new_hash)
        return True