"""TopBar — the persistent header at the top of the AppShell.

Layout (left to right):
  [☰ toggle]  Welcome heading + subtitle    [Live clock]    [User pill]

Inspired by modern SaaS dashboards (Linear, Stripe). The shop branding
lives in the sidebar's STORE INFORMATION block, not here — the top bar
is dedicated to the current page's primary heading and global actions.
"""
from typing import Optional
from datetime import datetime
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QWidget, QSizePolicy,
)

from app.resources.styles import tokens as t
from app.models.user import User


class TopBar(QFrame):
    """Persistent header. Reused across every page."""

    user_pill_clicked = Signal()
    toggle_sidebar_clicked = Signal()

    HEIGHT = 80

    def __init__(self, user: User, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self._user = user

        self.setObjectName("TopBar")
        self.setFixedHeight(self.HEIGHT)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self._build()
        self._start_clock()

    # ────────────────────────────────────────────────────────────
    # Public API
    # ────────────────────────────────────────────────────────────
    def set_heading(self, title: str, subtitle: str = "") -> None:
        """Update the heading shown in the top bar (call when navigating)."""
        self._title_label.setText(title)
        if subtitle:
            self._subtitle_label.setText(subtitle)
            self._subtitle_label.show()
        else:
            self._subtitle_label.hide()

    # ────────────────────────────────────────────────────────────
    # Build
    # ────────────────────────────────────────────────────────────
    def _build(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(t.SPACE_6, t.SPACE_4, t.SPACE_6, t.SPACE_4)
        layout.setSpacing(t.SPACE_5)
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # ── Sidebar collapse toggle (left) ───────────────────────
        # Uses « / » arrows to clearly signal "collapse / expand sidebar"
        # rather than the hamburger which reads as "open a menu".
        self._toggle_btn = QPushButton("«")
        self._toggle_btn.setObjectName("TopBarToggle")
        self._toggle_btn.setFixedSize(44, 44)
        self._toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._toggle_btn.setToolTip("Collapse sidebar")
        self._toggle_btn.clicked.connect(self._on_toggle_clicked)
        layout.addWidget(
            self._toggle_btn, alignment=Qt.AlignmentFlag.AlignVCenter
        )

        # ── Heading + subtitle ──────────────────────────────────
        heading_box = QVBoxLayout()
        heading_box.setSpacing(2)
        heading_box.setContentsMargins(0, 0, 0, 0)

        self._title_label = QLabel(f"Welcome back, {self._user.display_name}")
        self._title_label.setStyleSheet(
            f"color: {t.TEXT_PRIMARY};"
            f"font-size: {t.FONT_SIZE_2XL}px;"
            f"font-weight: {t.FONT_WEIGHT_BOLD};"
            f"background: transparent;"
        )
        heading_box.addWidget(self._title_label)

        self._subtitle_label = QLabel("Here's a quick overview of your shop today.")
        self._subtitle_label.setStyleSheet(
            f"color: {t.TEXT_MUTED};"
            f"font-size: {t.FONT_SIZE_BASE}px;"
            f"background: transparent;"
        )
        heading_box.addWidget(self._subtitle_label)

        layout.addLayout(heading_box)
        layout.addStretch()

        # ── Live clock ──────────────────────────────────────────
        # ── Live clock ──────────────────────────────────────────
        # ── Live clock ──────────────────────────────────────────
        self._clock_label = QLabel()
        self._clock_label.setObjectName("TopBarClock")
        self._clock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._clock_label)

        # ── User pill ───────────────────────────────────────────
        self.user_pill = self._build_user_pill()  # public — anchored by user menu
        layout.addWidget(self.user_pill)

    def _on_toggle_clicked(self):
        """Toggle the sidebar AND flip the arrow direction."""
        self.toggle_sidebar_clicked.emit()
        # Flip the arrow visually (we track state locally)
        if self._toggle_btn.text() == "«":
            self._toggle_btn.setText("»")
            self._toggle_btn.setToolTip("Expand sidebar")
        else:
            self._toggle_btn.setText("«")
            self._toggle_btn.setToolTip("Collapse sidebar")

    def _build_user_pill(self) -> QLabel:
        """User card — IDENTICAL to the clock card (same widget type, same QSS class).

        Built as a QLabel (not QPushButton) so the styling matches the
        clock perfectly with zero competing rules. Click handling done
        via mousePressEvent.
        """
        text = f"👤   {self._user.display_name}   ⌄"

        label = QLabel(text)
        label.setObjectName("UserPill")
        label.setCursor(Qt.CursorShape.PointingHandCursor)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Make the label clickable
        def on_click(_event):
            self.user_pill_clicked.emit()

        label.mousePressEvent = on_click

        return label

    @staticmethod
    def _extract_initials(name: str) -> str:
        parts = [p for p in name.split() if p]
        if not parts:
            return "?"
        if len(parts) == 1:
            return parts[0][:2].upper()
        return (parts[0][0] + parts[-1][0]).upper()

    # ────────────────────────────────────────────────────────────
    # Live clock
    # ────────────────────────────────────────────────────────────
    def _start_clock(self) -> None:
        self._update_clock()
        self._clock_timer = QTimer(self)
        self._clock_timer.timeout.connect(self._update_clock)
        self._clock_timer.start(1000)

    def _update_clock(self) -> None:
        now = datetime.now()
        self._clock_label.setText(now.strftime("📅  %a, %d %b %Y  ·  %H:%M:%S"))