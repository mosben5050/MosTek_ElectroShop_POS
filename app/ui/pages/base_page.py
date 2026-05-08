"""BasePage — the standard layout every full-screen view inherits from.

Provides:
  - A header with title + optional subtitle + optional action buttons
  - A scrollable content area that won't clip on small screens
  - Consistent margins and spacing across all pages

Usage:
    class SalesPage(BasePage):
        def __init__(self, parent=None):
            super().__init__(
                title="Sales",
                subtitle="Process customer transactions",
                parent=parent,
            )
            self.add_header_action(PrimaryButton("New Sale", on_click=self._new_sale))
            self.content_layout.addWidget(self._build_cart())
"""
from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea,
    QPushButton, QSizePolicy,
)

from app.resources.styles import tokens as t


class BasePage(QWidget):
    """Standard page layout: header + scrollable content."""

    def __init__(
        self,
        title: str,
        subtitle: str = "",
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)

        # Root layout — no margins, header and content fill edge-to-edge
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Header ───────────────────────────────────────────────
        self._header = self._build_header(title, subtitle)
        root.addWidget(self._header)

        # ── Scrollable content area ──────────────────────────────
        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        # The widget that actually holds the content
        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(
            t.SPACE_8, t.SPACE_6, t.SPACE_8, t.SPACE_8
        )
        self.content_layout.setSpacing(t.SPACE_4)

        self._scroll_area.setWidget(content_widget)
        root.addWidget(self._scroll_area, stretch=1)

    # ────────────────────────────────────────────────────────────
    # Header construction
    # ────────────────────────────────────────────────────────────
    def _build_header(self, title: str, subtitle: str) -> QWidget:
        header = QFrame()
        # Use objectName + global stylesheet rule instead of inline styling
        # so child widgets (like buttons) aren't affected by cascaded styles.
        header.setObjectName("PageHeader")
        header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        outer = QHBoxLayout(header)
        outer.setContentsMargins(t.SPACE_8, t.SPACE_5, t.SPACE_8, t.SPACE_5)
        outer.setSpacing(t.SPACE_4)

        # Left side: title + subtitle stacked
        text_box = QVBoxLayout()
        text_box.setSpacing(2)

        self._title_label = QLabel(title)
        self._title_label.setProperty("role", "title")
        text_box.addWidget(self._title_label)

        self._subtitle_label = QLabel(subtitle)
        self._subtitle_label.setProperty("role", "muted")
        if not subtitle:
            self._subtitle_label.hide()
        text_box.addWidget(self._subtitle_label)

        outer.addLayout(text_box, stretch=1)

        # Right side: action buttons go here
        self._actions_layout = QHBoxLayout()
        self._actions_layout.setSpacing(t.SPACE_2)
        outer.addLayout(self._actions_layout)

        return header

    # ────────────────────────────────────────────────────────────
    # Public API
    # ────────────────────────────────────────────────────────────
    def add_header_action(self, button: QPushButton) -> None:
        """Append an action button to the right side of the header."""
        self._actions_layout.addWidget(button)

    def set_title(self, title: str) -> None:
        self._title_label.setText(title)

    def set_subtitle(self, subtitle: str) -> None:
        self._subtitle_label.setText(subtitle)
        self._subtitle_label.setVisible(bool(subtitle))