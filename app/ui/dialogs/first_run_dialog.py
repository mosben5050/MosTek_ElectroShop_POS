"""First-run setup dialog — shown once when no users exist yet.

Forces the very first user to be created as an admin so there's
always at least one account that can manage the system.
"""
from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget

from app.resources.styles import tokens as t
from app.services.auth_service import AuthService
from app.models.user import User
from app.ui.dialogs.base_dialog import BaseDialog
from app.ui.widgets.buttons import PrimaryButton, SecondaryButton
from app.ui.widgets.inputs import TextField, PasswordField


class FirstRunDialog(BaseDialog):
    """Shown on first launch to create the initial admin user."""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(
            parent=parent,
            title="Welcome to MosTek ElectroPOS",
            min_width=520,
            min_height=560,
        )

        self._auth = AuthService()
        self._created_user: Optional[User] = None

        self._build_content()
        self._build_footer_buttons()

    # ────────────────────────────────────────────────────────────
    # Public API
    # ────────────────────────────────────────────────────────────
    @property
    def created_user(self) -> Optional[User]:
        """The user that was created. None if dialog was cancelled."""
        return self._created_user

    # ────────────────────────────────────────────────────────────
    # Build UI
    # ────────────────────────────────────────────────────────────
    def _build_content(self) -> None:
        # Friendly intro
        intro = QLabel(
            "Looks like this is your first time running ElectroPOS!\n"
            "Let's create your administrator account to get started."
        )
        intro.setWordWrap(True)
        intro.setStyleSheet(
            f"color: {t.TEXT_SECONDARY};"
            f"font-size: {t.FONT_SIZE_BASE}px;"
            f"background: transparent;"
            f"padding-bottom: 8px;"
        )
        self.content_layout.addWidget(intro)

        # Form fields
        self._full_name_field = TextField(
            label="Full name",
            placeholder="e.g. Kwame Mensah",
            required=True,
            compact=True,
        )
        self.content_layout.addWidget(self._full_name_field)

        self._username_field = TextField(
            label="Username",
            placeholder="e.g. kwame (used to sign in)",
            required=True,
            compact=True,
        )
        self.content_layout.addWidget(self._username_field)

        self._password_field = PasswordField(
            label="Password",
            placeholder="At least 6 characters",
            required=True,
            compact=True,
        )
        self.content_layout.addWidget(self._password_field)

        self._confirm_field = PasswordField(
            label="Confirm password",
            placeholder="Type the password again",
            required=True,
            compact=True,
        )
        self.content_layout.addWidget(self._confirm_field)

        # Hint about the role
        hint = QLabel(
            "ℹ This account will have full administrator access. "
            "You can create cashier and technician accounts later from Settings."
        )
        hint.setWordWrap(True)
        hint.setStyleSheet(
            f"color: {t.TEXT_MUTED};"
            f"font-size: {t.FONT_SIZE_SM}px;"
            f"background: {t.PRIMARY_LIGHT};"
            f"border-radius: {t.RADIUS_MD}px;"
            f"padding: 12px;"
        )
        self.content_layout.addWidget(hint)

        self.content_layout.addStretch()

    def _build_footer_buttons(self) -> None:
        self.add_footer_button(
            SecondaryButton("Quit", on_click=self.reject)
        )
        self.add_footer_button(
            PrimaryButton("Create Admin Account", on_click=self._on_create)
        )

    # ────────────────────────────────────────────────────────────
    # Action handler
    # ────────────────────────────────────────────────────────────
    def _on_create(self) -> None:
        # Clear any previous errors
        self._full_name_field.clear_error()
        self._username_field.clear_error()
        self._password_field.clear_error()
        self._confirm_field.clear_error()

        full_name = self._full_name_field.text().strip()
        username = self._username_field.text().strip()
        password = self._password_field.text()
        confirm = self._confirm_field.text()

        # Validation — surface errors next to the relevant field
        has_error = False

        if not full_name:
            self._full_name_field.set_error("Full name is required")
            has_error = True

        if not username:
            self._username_field.set_error("Username is required")
            has_error = True
        elif len(username) < 3:
            self._username_field.set_error("Must be at least 3 characters")
            has_error = True

        if not password:
            self._password_field.set_error("Password is required")
            has_error = True
        elif len(password) < 6:
            self._password_field.set_error("Must be at least 6 characters")
            has_error = True

        if password != confirm:
            self._confirm_field.set_error("Passwords do not match")
            has_error = True

        if has_error:
            return

        # Try to create the user
        try:
            self._created_user = self._auth.create_user(
                username=username,
                password=password,
                full_name=full_name,
                role="admin",
            )
            self.accept()
        except ValueError as e:
            # Service-level errors (uniqueness, etc.) — show on username
            self._username_field.set_error(str(e))