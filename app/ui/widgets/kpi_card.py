"""KpiCard — a reusable dashboard metric card.

Layout:
    ┌────────────────────────────────┐
    │  [icon tile]  Label            │
    │                                │
    │  Big Value                     │
    │                                │
    │  ↑ 12.5% delta text            │
    │  or "No sales yet" empty state │
    └────────────────────────────────┘

Each card has a coloured icon tile that gives it identity. Use for
'Total Sales', 'Orders', 'Customers', etc. Built to be size-aware:
will sit nicely in any QGridLayout.
"""
from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QWidget,
)

from app.resources.styles import tokens as t


class KpiCard(QFrame):
    """A single dashboard metric card.

    Args:
        title: e.g. "Total Sales"
        value: e.g. "GHS 12,540.75" or "156" (the headline number)
        icon:  emoji used in the icon tile
        accent_color: background colour of the icon tile (hex string)
        delta: optional growth text e.g. "↑ 12.5% vs yesterday"
        empty_message: shown when value is "0" or empty
                       e.g. "No sales yet"
    """

    def __init__(
        self,
        title: str,
        value: str,
        icon: str,
        accent_color: str,
        delta: str = "",
        empty_message: str = "",
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)

        self._title = title
        self._value = value
        self._icon = icon
        self._accent_color = accent_color
        self._delta = delta
        self._empty_message = empty_message

        self.setObjectName("KpiCard")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumHeight(150)
        self.setMaximumHeight(180)

        self._build()

    # ────────────────────────────────────────────────────────────
    # Public API — values can be updated as data comes in
    # ────────────────────────────────────────────────────────────
    def update_value(
        self,
        value: str,
        delta: str = "",
        is_empty: bool = False,
    ) -> None:
        """Refresh the card's headline number and delta line."""
        self._value_label.setText(value)
        if is_empty and self._empty_message:
            self._delta_label.setText(self._empty_message)
            self._delta_label.setStyleSheet(self._empty_style())
        elif delta:
            self._delta_label.setText(delta)
            self._delta_label.setStyleSheet(self._delta_style(delta))
        else:
            self._delta_label.setText("")

    # ────────────────────────────────────────────────────────────
    # Build
    # ────────────────────────────────────────────────────────────
    def _build(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(t.SPACE_5, t.SPACE_5, t.SPACE_5, t.SPACE_5)
        outer.setSpacing(t.SPACE_3)

        # ── Top row: icon tile + title ──────────────────────────
        top_row = QHBoxLayout()
        top_row.setSpacing(t.SPACE_3)

        # Icon tile — small coloured square with the emoji
        icon_tile = QLabel(self._icon)
        icon_tile.setFixedSize(48, 48)
        icon_tile.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_tile.setStyleSheet(
            f"background-color: {self._accent_color};"
            f"border-radius: {t.RADIUS_MD}px;"
            f"font-size: 22px;"
        )
        top_row.addWidget(icon_tile)

        # Title label
        title_label = QLabel(self._title)
        title_label.setStyleSheet(
            f"color: {t.TEXT_MUTED};"
            f"font-size: {t.FONT_SIZE_SM}px;"
            f"font-weight: {t.FONT_WEIGHT_MEDIUM};"
            f"background: transparent;"
        )
        top_row.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignVCenter)
        top_row.addStretch()

        outer.addLayout(top_row)

        # ── Big value ───────────────────────────────────────────
        self._value_label = QLabel(self._value)
        self._value_label.setStyleSheet(
            f"color: {t.TEXT_PRIMARY};"
            f"font-size: {t.FONT_SIZE_3XL}px;"
            f"font-weight: {t.FONT_WEIGHT_BOLD};"
            f"background: transparent;"
        )
        outer.addWidget(self._value_label)

        # ── Delta / empty-state line ────────────────────────────
        delta_text = self._delta if self._delta else self._empty_message
        self._delta_label = QLabel(delta_text)
        self._delta_label.setStyleSheet(
            self._delta_style(self._delta) if self._delta else self._empty_style()
        )
        outer.addWidget(self._delta_label)

        outer.addStretch()

    # ────────────────────────────────────────────────────────────
    # Style helpers
    # ────────────────────────────────────────────────────────────
    @staticmethod
    def _delta_style(delta_text: str) -> str:
        """Green for positive (↑), red for negative (↓), muted otherwise."""
        if delta_text.startswith("↑"):
            color = t.SUCCESS
        elif delta_text.startswith("↓"):
            color = t.DANGER
        else:
            color = t.TEXT_MUTED
        return (
            f"color: {color};"
            f"font-size: {t.FONT_SIZE_SM}px;"
            f"font-weight: {t.FONT_WEIGHT_SEMIBOLD};"
            f"background: transparent;"
        )

    @staticmethod
    def _empty_style() -> str:
        return (
            f"color: {t.TEXT_MUTED};"
            f"font-size: {t.FONT_SIZE_SM}px;"
            f"font-weight: {t.FONT_WEIGHT_MEDIUM};"
            f"font-style: italic;"
            f"background: transparent;"
        )