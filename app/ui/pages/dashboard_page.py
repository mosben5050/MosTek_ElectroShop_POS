"""DashboardPage — the landing page after login.

Currently a friendly placeholder; will be filled with KPI cards,
recent activity, and quick actions in the next phase.
"""
from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame, QHBoxLayout

from app.resources.styles import tokens as t
from app.models.user import User
from app.ui.pages.base_page import BasePage


class DashboardPage(BasePage):
    """The first screen the user sees after signing in."""

    def __init__(self, user: User, parent: Optional[QWidget] = None):
        # Empty title/subtitle — TopBar shows the welcome heading instead
        super().__init__(title="", subtitle="", parent=parent)
        self._user = user

        # Hide the BasePage header since the TopBar has the welcome
        self._header.hide()

        placeholder_card = self._build_placeholder_card()
        self.content_layout.addWidget(placeholder_card)
        self.content_layout.addStretch()

    def _build_placeholder_card(self) -> QWidget:
        """A friendly 'coming soon' card while we build the real dashboard."""
        card = QFrame()
        card.setStyleSheet(
            f"background-color: {t.BG_CARD};"
            f"border: 1px solid {t.BORDER};"
            f"border-radius: {t.RADIUS_LG}px;"
            f"padding: {t.SPACE_8}px;"
        )

        layout = QVBoxLayout(card)
        layout.setSpacing(t.SPACE_3)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Big icon
        icon = QLabel("📊")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet(
            f"font-size: 56px;"
            f"background: transparent;"
        )
        layout.addWidget(icon)

        # Title
        title = QLabel("Dashboard coming soon")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            f"color: {t.TEXT_PRIMARY};"
            f"font-size: {t.FONT_SIZE_XL}px;"
            f"font-weight: {t.FONT_WEIGHT_SEMIBOLD};"
            f"background: transparent;"
        )
        layout.addWidget(title)

        # Description
        desc = QLabel(
            "Today's sales, open repairs, low-stock alerts, and "
            "recent activity will appear here."
        )
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setWordWrap(True)
        desc.setStyleSheet(
            f"color: {t.TEXT_MUTED};"
            f"font-size: {t.FONT_SIZE_BASE}px;"
            f"background: transparent;"
        )
        layout.addWidget(desc)

        # Wrap in a horizontal layout so the card doesn't stretch full-width
        wrapper = QWidget()
        wrap_layout = QHBoxLayout(wrapper)
        wrap_layout.setContentsMargins(0, 0, 0, 0)
        wrap_layout.addStretch()
        wrap_layout.addWidget(card)
        wrap_layout.addStretch()

        # Make the card a reasonable max width
        card.setMaximumWidth(560)

        return wrapper