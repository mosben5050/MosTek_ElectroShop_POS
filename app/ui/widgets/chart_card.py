"""ChartCard — a reusable card that wraps a chart with title and empty state.

Layout:
    ┌──────────────────────────────────────┐
    │  Title                  [optional ▼] │
    │  ┌────────────────────────────────┐ │
    │  │                                 │ │
    │  │      Chart goes here            │ │
    │  │      (or empty state)           │ │
    │  │                                 │ │
    │  └────────────────────────────────┘ │
    └──────────────────────────────────────┘

Subclasses or callers populate the body via set_chart_widget()
or set_empty_state().
"""
from typing import Optional, List, Tuple
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QSizePolicy, QWidget,
    QStackedLayout,
)

from app.resources.styles import tokens as t


class ChartCard(QFrame):
    """A card that holds a chart, with title and built-in empty state."""

    # Emitted when the user changes the period dropdown
    period_changed = Signal(str)

    def __init__(
        self,
        title: str,
        period_options: Optional[List[Tuple[str, str]]] = None,
        # period_options is a list of (display_text, key) tuples like:
        #   [("7 Days", "7d"), ("30 Days", "30d"), ("90 Days", "90d")]
        empty_icon: str = "📊",
        empty_message: str = "No data yet",
        empty_subtext: str = "Data will appear here once you have activity.",
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)

        self._title_text = title
        self._period_options = period_options or []
        self._empty_icon = empty_icon
        self._empty_message = empty_message
        self._empty_subtext = empty_subtext

        self.setObjectName("ChartCard")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(340)

        self._build()

    # ────────────────────────────────────────────────────────────
    # Public API
    # ────────────────────────────────────────────────────────────
    def set_chart_widget(self, chart_widget: QWidget) -> None:
        """Show a real chart inside the card.

        Replaces the empty state. Call this when data is available.
        """
        # Make sure the chart widget shows above the empty state
        self._stacked.addWidget(chart_widget)
        self._stacked.setCurrentWidget(chart_widget)

    def show_empty_state(self) -> None:
        """Switch back to the empty-state display."""
        self._stacked.setCurrentWidget(self._empty_widget)

    def get_period(self) -> Optional[str]:
        """Return the currently selected period key, or None."""
        if not self._period_combo:
            return None
        return self._period_combo.currentData()

    # ────────────────────────────────────────────────────────────
    # Build
    # ────────────────────────────────────────────────────────────
    def _build(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(t.SPACE_5, t.SPACE_5, t.SPACE_5, t.SPACE_5)
        outer.setSpacing(t.SPACE_4)

        # ── Header row: title + (optional) period dropdown ──
        header_row = QHBoxLayout()
        header_row.setSpacing(t.SPACE_3)

        title_label = QLabel(self._title_text)
        title_label.setStyleSheet(
            f"color: {t.TEXT_PRIMARY};"
            f"font-size: {t.FONT_SIZE_LG}px;"
            f"font-weight: {t.FONT_WEIGHT_SEMIBOLD};"
            f"background: transparent;"
        )
        header_row.addWidget(title_label)
        header_row.addStretch()

        # Optional period selector
        self._period_combo = None
        if self._period_options:
            self._period_combo = QComboBox()
            self._period_combo.setFixedHeight(t.INPUT_HEIGHT_COMPACT)
            self._period_combo.setMinimumWidth(120)
            self._period_combo.setCursor(Qt.CursorShape.PointingHandCursor)
            for label, key in self._period_options:
                self._period_combo.addItem(label, userData=key)
            self._period_combo.currentIndexChanged.connect(
                lambda _: self.period_changed.emit(self._period_combo.currentData())
            )
            header_row.addWidget(self._period_combo)

        outer.addLayout(header_row)

        # ── Body: stacked layout (empty state OR real chart) ──
        body_container = QWidget()
        self._stacked = QStackedLayout(body_container)
        self._stacked.setContentsMargins(0, 0, 0, 0)

        # Build the empty state widget once
        self._empty_widget = self._build_empty_state()
        self._stacked.addWidget(self._empty_widget)
        self._stacked.setCurrentWidget(self._empty_widget)

        outer.addWidget(body_container, stretch=1)

    def _build_empty_state(self) -> QWidget:
        """Friendly placeholder shown when there's no data yet."""
        empty = QWidget()
        layout = QVBoxLayout(empty)
        layout.setSpacing(t.SPACE_3)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Big icon
        icon = QLabel(self._empty_icon)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet(
            "font-size: 56px;"
            "background: transparent;"
        )
        layout.addWidget(icon)

        # Main message
        msg = QLabel(self._empty_message)
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg.setStyleSheet(
            f"color: {t.TEXT_PRIMARY};"
            f"font-size: {t.FONT_SIZE_LG}px;"
            f"font-weight: {t.FONT_WEIGHT_SEMIBOLD};"
            f"background: transparent;"
        )
        layout.addWidget(msg)

        # Subtext
        sub = QLabel(self._empty_subtext)
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setWordWrap(True)
        sub.setStyleSheet(
            f"color: {t.TEXT_MUTED};"
            f"font-size: {t.FONT_SIZE_SM}px;"
            f"background: transparent;"
        )
        sub.setMaximumWidth(360)
        layout.addWidget(sub, alignment=Qt.AlignmentFlag.AlignCenter)

        return empty