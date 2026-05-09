"""LoginPage — the entry screen for the application."""
from typing import Optional
from PySide6.QtCore import Qt, Signal, QSettings
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QSizePolicy,
    QCheckBox,
)

from app.resources.styles import tokens as t
from app.resources.assets import logo_path, login_background_path
from app.ui.widgets.feature_row import FeatureRow
from app.ui.widgets.buttons import PrimaryButton, SecondaryButton, GhostButton
from app.ui.widgets.inputs import TextField, PasswordField
from app.services.auth_service import AuthService


class LoginPage(QWidget):
    """Two-column login screen with background image."""

    login_succeeded = Signal(object)  # carries the User object

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self._auth = AuthService()
        self._settings = QSettings("MosTek", "ElectroPOS")
        self._background = QPixmap(login_background_path())

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self._left_panel = self._build_left_panel()
        root.addWidget(self._left_panel, stretch=1)

        self._right_panel = self._build_right_panel()
        root.addWidget(self._right_panel, stretch=1)

        # Wire up keyboard shortcuts and restore remembered username
        self._wire_keyboard_shortcuts()
        self._restore_remembered_username()

    def paintEvent(self, event):
        if not self._background.isNull():
            painter = QPainter(self)
            scaled = self._background.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
            painter.end()
        super().paintEvent(event)

    # ════════════════════════════════════════════════════════════
    # LEFT PANEL
    # ════════════════════════════════════════════════════════════
    def _build_left_panel(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("LoginLeftPanel")
        panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        outer = QVBoxLayout(panel)
        outer.setContentsMargins(t.SPACE_12, t.SPACE_8, t.SPACE_12, t.SPACE_8)
        outer.addStretch()

        content = QVBoxLayout()
        content.setSpacing(t.SPACE_4)

        # Logo + brand name
        brand_row = QHBoxLayout()
        brand_row.setSpacing(t.SPACE_4)
        brand_row.setAlignment(Qt.AlignmentFlag.AlignLeft)

        logo_label = QLabel()
        logo_pixmap = QPixmap(logo_path())
        if not logo_pixmap.isNull():
            logo_label.setPixmap(
                logo_pixmap.scaled(
                    96, 96,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        logo_label.setStyleSheet("background: transparent;")
        brand_row.addWidget(logo_label)

        name_box = QVBoxLayout()
        name_box.setSpacing(2)

        brand_name = QLabel("MosTek ElectroPOS")
        brand_name.setStyleSheet(
            f"color: {t.TEXT_INVERSE};"
            f"font-size: 32px;"
            f"font-weight: {t.FONT_WEIGHT_BOLD};"
            f"background: transparent;"
        )
        name_box.addWidget(brand_name)

        tagline = QLabel("Smart. Simple. Secure.")
        tagline.setStyleSheet(
            f"color: rgba(255, 255, 255, 0.8);"
            f"font-size: {t.FONT_SIZE_LG}px;"
            f"font-weight: {t.FONT_WEIGHT_MEDIUM};"
            f"background: transparent;"
        )
        name_box.addWidget(tagline)

        brand_row.addLayout(name_box)
        brand_row.addStretch()
        content.addLayout(brand_row)

        # Gold accent line
        accent_line = QFrame()
        accent_line.setFixedHeight(3)
        accent_line.setFixedWidth(80)
        accent_line.setStyleSheet(
            f"background-color: {t.ACCENT};"
            f"border: none;"
            f"border-radius: 1px;"
        )
        content.addWidget(accent_line)
        content.addSpacing(t.SPACE_8)

        # Feature rows
        features = [
            ("⚡", "Fast & Efficient",
             "Speed up your sales process with ease."),
            ("📊", "Accurate Reports",
             "Get real-time insights and powerful analytics."),
            ("🛡️", "Secure & Reliable",
             "Your data is safe with enterprise-grade security."),
            ("👥", "Easy to Use",
             "Designed for everyone, so you can focus on what matters."),
        ]
        for icon, title, desc in features:
            content.addWidget(FeatureRow(icon, title, desc, on_dark=True))
            content.addSpacing(t.SPACE_3)

        outer.addLayout(content)
        outer.addStretch()

        # Footer
        footer = QLabel("© 2026 MosTek Solutions. All rights reserved.")
        footer.setAlignment(Qt.AlignmentFlag.AlignLeft)
        footer.setStyleSheet(
            f"color: rgba(255, 255, 255, 0.6);"
            f"font-size: {t.FONT_SIZE_XS}px;"
            f"background: transparent;"
        )
        outer.addWidget(footer)

        return panel

    # ════════════════════════════════════════════════════════════
    # RIGHT PANEL
    # ════════════════════════════════════════════════════════════
    def _build_right_panel(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("LoginRightPanel")
        panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        outer = QVBoxLayout(panel)
        outer.setContentsMargins(t.SPACE_8, t.SPACE_8, t.SPACE_8, t.SPACE_8)
        outer.addStretch()

        wrapper = QHBoxLayout()
        wrapper.addStretch()
        wrapper.addWidget(self._build_login_card())
        wrapper.addStretch()

        outer.addLayout(wrapper)
        outer.addStretch()

        return panel

    # ════════════════════════════════════════════════════════════
    # LOGIN CARD
    # ════════════════════════════════════════════════════════════
    def _build_login_card(self) -> QWidget:
        # Outer gradient border frame
        border_frame = QFrame()
        border_frame.setObjectName("LoginCardBorder")
        border_frame.setFixedWidth(520)

        border_layout = QVBoxLayout(border_frame)
        border_layout.setContentsMargins(2, 2, 2, 2)
        border_layout.setSpacing(0)

        # Inner white card
        card = QFrame()
        card.setObjectName("LoginCard")
        border_layout.addWidget(card)

        # Form
        form = QVBoxLayout(card)
        form.setContentsMargins(
            t.SPACE_10, t.SPACE_10, t.SPACE_10, t.SPACE_10
        )
        form.setSpacing(0)

        # Lock icon
        lock_icon = QLabel("🔒")
        lock_icon.setFixedSize(72, 72)
        lock_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lock_icon.setStyleSheet(
            f"background-color: {t.PRIMARY_LIGHT};"
            f"border: 2px solid {t.PRIMARY};"
            f"border-radius: 36px;"
            f"font-size: 28px;"
        )
        icon_row = QHBoxLayout()
        icon_row.addStretch()
        icon_row.addWidget(lock_icon)
        icon_row.addStretch()
        form.addLayout(icon_row)
        form.addSpacing(t.SPACE_4)

        # Heading
        heading = QLabel("Welcome Back!")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        heading.setStyleSheet(
            f"color: {t.TEXT_PRIMARY};"
            f"font-size: {t.FONT_SIZE_2XL}px;"
            f"font-weight: {t.FONT_WEIGHT_BOLD};"
            f"background: transparent;"
        )
        form.addWidget(heading)

        # Subtitle
        subtitle = QLabel("Sign in to continue to MosTek ElectroPOS")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(
            f"color: {t.TEXT_MUTED};"
            f"font-size: {t.FONT_SIZE_BASE}px;"
            f"background: transparent;"
        )
        form.addWidget(subtitle)
        form.addSpacing(t.SPACE_8)

        # Username
        self._username_field = TextField(
            label="",
            placeholder="Username",
            icon="👤",
        )
        form.addWidget(self._username_field)
        form.addSpacing(t.SPACE_3)

        # Password
        self._password_field = PasswordField(
            label="",
            placeholder="Password",
            icon="🔒",
        )
        form.addWidget(self._password_field)
        form.addSpacing(t.SPACE_4)

        # Remember me + Forgot password
        remember_row = QHBoxLayout()
        remember_row.setContentsMargins(0, 0, 0, 0)

        self._remember_checkbox = QCheckBox("Remember me")
        self._remember_checkbox.setStyleSheet(
            f"color: {t.TEXT_SECONDARY};"
            f"font-size: {t.FONT_SIZE_SM}px;"
            f"background: transparent;"
        )
        self._remember_checkbox.setCursor(Qt.CursorShape.PointingHandCursor)
        remember_row.addWidget(self._remember_checkbox)
        remember_row.addStretch()

        forgot_btn = GhostButton("Forgot password?", on_click=self._on_forgot_password)
        remember_row.addWidget(forgot_btn)

        form.addLayout(remember_row)
        form.addSpacing(t.SPACE_5)

        # Sign in button
        sign_in_btn = PrimaryButton("→  SIGN IN", on_click=self._on_sign_in)
        sign_in_btn.setMinimumHeight(t.BUTTON_HEIGHT_LG)
        form.addWidget(sign_in_btn)
        form.addSpacing(t.SPACE_4)

        # OR divider
        or_row = QHBoxLayout()
        or_row.setContentsMargins(0, 0, 0, 0)

        line_left = QFrame()
        line_left.setFixedHeight(1)
        line_left.setStyleSheet(f"background-color: {t.BORDER}; border: none;")
        or_row.addWidget(line_left, stretch=1)

        or_label = QLabel("  OR  ")
        or_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        or_label.setStyleSheet(
            f"color: {t.TEXT_MUTED};"
            f"font-size: {t.FONT_SIZE_SM}px;"
            f"font-weight: {t.FONT_WEIGHT_MEDIUM};"
            f"background: transparent;"
            f"padding: 0 8px;"
        )
        or_row.addWidget(or_label)

        line_right = QFrame()
        line_right.setFixedHeight(1)
        line_right.setStyleSheet(f"background-color: {t.BORDER}; border: none;")
        or_row.addWidget(line_right, stretch=1)

        form.addLayout(or_row)
        form.addSpacing(t.SPACE_4)

        # PIN button
        pin_btn = SecondaryButton("⌨   USE PIN LOGIN", on_click=self._on_pin_login)
        pin_btn.setMinimumHeight(t.BUTTON_HEIGHT_LG)
        form.addWidget(pin_btn)

        return border_frame

    # ════════════════════════════════════════════════════════════
    # Action handlers
    # ════════════════════════════════════════════════════════════
    def _on_sign_in(self):
        username = self._username_field.text().strip()
        password = self._password_field.text()

        # Clear any previous errors
        self._username_field.clear_error()
        self._password_field.clear_error()

        # Basic field-level validation
        if not username:
            self._username_field.set_error("Username is required")
            return
        if not password:
            self._password_field.set_error("Password is required")
            return

        # Try to authenticate against the database
        user = self._auth.authenticate(username, password)

        if user is None:
            # Show error on the password field. We deliberately use a
            # generic message so attackers can't tell whether the username
            # or the password was wrong.
            self._password_field.set_error("Invalid username or password")
            self._password_field.set_text("")  # clear the password field
            self._password_field.set_focus()
            return

        # Success!
        print(f"[Login] {user.username} signed in successfully ({user.role})")
        self._persist_remember_me(user.username)
        self.login_succeeded.emit(user)


    def _on_pin_login(self):
        print("[Login] PIN login requested (not yet implemented)")

    def _on_forgot_password(self):
        """Show an info dialog explaining how to recover access."""
        from PySide6.QtWidgets import QMessageBox
        msg = QMessageBox(self)
        msg.setWindowTitle("Password Recovery")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("Forgot your password?")
        msg.setInformativeText(
            "For your security, only an administrator can reset your password.\n\n"
            "Please contact your shop administrator to have your password reset, "
            "or sign in with a PIN if you have one set up."
        )
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    # ────────────────────────────────────────────────────────────
    # Keyboard shortcuts and "Remember me"
    # ────────────────────────────────────────────────────────────
    def _wire_keyboard_shortcuts(self):
        """Make Enter behave naturally:
           - Enter in username field → jump to password field
           - Enter in password field → trigger sign-in
        """
        self._username_field.line_edit.returnPressed.connect(
            self._password_field.set_focus
        )
        self._password_field.line_edit.returnPressed.connect(
            self._on_sign_in
        )

    def _restore_remembered_username(self):
        """If 'Remember me' was on last time, pre-fill the username."""
        remembered = self._settings.value("login/remembered_username", "")
        if remembered:
            self._username_field.set_text(str(remembered))
            self._remember_checkbox.setChecked(True)
            # Focus the password field since username is already filled
            self._password_field.set_focus()
        else:
            self._username_field.set_focus()

    def _persist_remember_me(self, username: str):
        """Save or clear the remembered username based on checkbox state.

        IMPORTANT: We only ever store the username, NEVER the password.
        Storing passwords on disk is a security risk we don't take.
        """
        if self._remember_checkbox.isChecked():
            self._settings.setValue("login/remembered_username", username)
        else:
            self._settings.remove("login/remembered_username")