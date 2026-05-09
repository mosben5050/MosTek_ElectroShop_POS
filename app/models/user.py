"""User model — represents a staff member who can log into the system."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """Plain Python object representing one row from the users table.

    We use @dataclass so we get __init__, __repr__, and __eq__ for free.
    Database hydration happens in app.repositories.user_repo — this class
    just holds the data.
    """
    id: Optional[int]              # None for not-yet-persisted users
    username: str
    full_name: str
    role: str                      # 'admin', 'cashier', or 'technician'
    is_active: bool = True
    password_hash: Optional[str] = None  # never expose this in the UI
    created_at: Optional[str] = None
    last_login_at: Optional[str] = None

    # ────────────────────────────────────────────────────────────
    # Convenience properties
    # ────────────────────────────────────────────────────────────
    @property
    def is_admin(self) -> bool:
        return self.role == "admin"

    @property
    def is_cashier(self) -> bool:
        return self.role == "cashier"

    @property
    def is_technician(self) -> bool:
        return self.role == "technician"

    @property
    def display_name(self) -> str:
        """The name shown in headers, dropdowns, etc."""
        return self.full_name or self.username

    def __str__(self) -> str:
        return f"User({self.username}, {self.role})"