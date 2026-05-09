"""DashboardPage — the landing page after login.

Phase A: 5 KPI cards across the top, all showing empty states until
real data exists. More phases coming: charts, recent transactions,
low stock alerts.
"""
from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame,
)

from app.resources.styles import tokens as t
from app.models.user import User
from app.ui.pages.base_page import BasePage
from app.ui.widgets.kpi_card import KpiCard


class DashboardPage(BasePage):
    """The first screen after sign-in. Inspired by modern POS dashboards."""

    def __init__(self, user: User, parent: Optional[QWidget] = None):
        super().__init__(title="", subtitle="", parent=parent)
        self._user = user

        # Hide the BasePage header — TopBar shows the welcome
        self._header.hide()

        self._build_kpi_row()

        # Placeholder for the rest of the dashboard (charts + tables)
        # Will be filled in in Phase B and C
        self._build_coming_soon_section()

        self.content_layout.addStretch()

    # ────────────────────────────────────────────────────────────
    # Phase A — KPI Cards
    # ────────────────────────────────────────────────────────────
    def _build_kpi_row(self) -> None:
        """Build the row of 5 KPI cards across the top of the dashboard."""

        # Container row with consistent spacing
        kpi_grid = QGridLayout()
        kpi_grid.setSpacing(t.SPACE_4)
        kpi_grid.setContentsMargins(0, 0, 0, 0)

        # Card definitions — same colours used in the reference image,
        # adapted for our blue+gold brand
        cards = [
            {
                "title": "Total Sales",
                "value": f"{t.CURRENCY_SYMBOL_DEFAULT} 0.00",
                "icon": "💰",
                "color": "#EDE9FE",   # soft purple
                "empty": "No sales yet",
            },
            {
                "title": "Total Orders",
                "value": "0",
                "icon": "🛒",
                "color": "#DCFCE7",   # soft green
                "empty": "No orders yet",
            },
            {
                "title": "Open Repairs",
                "value": "0",
                "icon": "🔧",
                "color": "#FED7AA",   # soft orange
                "empty": "No active tickets",
            },
            {
                "title": "Customers",
                "value": "0",
                "icon": "👥",
                "color": "#DBEAFE",   # soft blue (matches our brand)
                "empty": "No customers yet",
            },
            {
                "title": "Low Stock Items",
                "value": "0",
                "icon": "⚠️",
                "color": "#FEE2E2",   # soft red
                "empty": "All items in stock",
            },
        ]

        # Lay them out in a single row using QGridLayout so they share
        # available width equally and wrap on narrower screens
        for col, card_def in enumerate(cards):
            card = KpiCard(
                title=card_def["title"],
                value=card_def["value"],
                icon=card_def["icon"],
                accent_color=card_def["color"],
                empty_message=card_def["empty"],
            )
            kpi_grid.addWidget(card, 0, col)

        # Make all 5 columns have equal stretch
        for col in range(5):
            kpi_grid.setColumnStretch(col, 1)

        self.content_layout.addLayout(kpi_grid)

    # ────────────────────────────────────────────────────────────
    # Coming soon — placeholder until charts and tables are built
    # ────────────────────────────────────────────────────────────
    def _build_coming_soon_section(self) -> None:
        """Friendly placeholder for the rest of the dashboard."""
        spacer = QWidget()
        spacer.setFixedHeight(24)
        self.content_layout.addWidget(spacer)

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

        icon = QLabel("📈")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("font-size: 48px; background: transparent;")
        layout.addWidget(icon)

        title = QLabel("Charts and reports coming next")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            f"color: {t.TEXT_PRIMARY};"
            f"font-size: {t.FONT_SIZE_LG}px;"
            f"font-weight: {t.FONT_WEIGHT_SEMIBOLD};"
            f"background: transparent;"
        )
        layout.addWidget(title)

        desc = QLabel(
            "Sales overview chart, payment method breakdown, "
            "top products, recent transactions, and low-stock alerts "
            "will appear here once we build them."
        )
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setWordWrap(True)
        desc.setStyleSheet(
            f"color: {t.TEXT_MUTED};"
            f"font-size: {t.FONT_SIZE_BASE}px;"
            f"background: transparent;"
        )
        layout.addWidget(desc)

        self.content_layout.addWidget(card)