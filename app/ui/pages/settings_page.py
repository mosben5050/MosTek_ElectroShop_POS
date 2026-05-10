"""SettingsPage — admin configuration hub."""
from typing import Optional
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QFrame,
)

from app.resources.styles import tokens as t
from app.models.user import User
from app.ui.pages.base_page import BasePage


class SettingsPage(BasePage):
    """The settings hub — admin only.

    Emits `shop_info_updated` when the Shop Profile tab saves changes,
    so the sidebar/topbar can refresh their displays.
    """

    shop_info_updated = Signal()

    def __init__(self, user: User, parent: Optional[QWidget] = None):
        # Empty title/subtitle — TopBar shows the heading instead
        super().__init__(title="", subtitle="", parent=parent)
        self._user = user

        # Hide the BasePage header — TopBar handles it
        self._header.hide()

        self._build_tabs()

    def _build_tabs(self) -> None:
        """Build the QTabWidget with 5 placeholder tabs."""
        self._tabs = QTabWidget()
        self._tabs.setObjectName("SettingsTabs")
        self._tabs.setDocumentMode(True)

        # Shop Profile — REAL tab
        from app.ui.pages.settings_tabs.shop_profile_tab import ShopProfileTab
        self._shop_profile_tab = ShopProfileTab()
        self._shop_profile_tab.saved.connect(self.shop_info_updated.emit)
        self._tabs.addTab(self._shop_profile_tab, "🏪  Shop Profile")

        # Tax & Currency — REAL tab
        from app.ui.pages.settings_tabs.tax_currency_tab import TaxCurrencyTab
        self._tax_currency_tab = TaxCurrencyTab()
        self._tax_currency_tab.saved.connect(self.shop_info_updated.emit)
        self._tabs.addTab(self._tax_currency_tab, "💰  Tax & Currency")
        
        self._tabs.addTab(
            self._build_placeholder_tab(
                icon="🧾",
                title="Receipt",
                message="Customise the header and footer text printed on customer receipts.",
                coming_phase="Coming soon",
            ),
            "Receipt",
        )
        self._tabs.addTab(
            self._build_placeholder_tab(
                icon="💾",
                title="Backup & Restore",
                message="Manually back up your data, or restore from a previous backup file.",
                coming_phase="Coming soon",
            ),
            "Backup",
        )
        self._tabs.addTab(
            self._build_placeholder_tab(
                icon="ℹ️",
                title="About",
                message="App version, license info, and where to get help.",
                coming_phase="Coming soon",
            ),
            "About",
        )

        self.content_layout.addWidget(self._tabs)
        self.content_layout.addStretch()

    @staticmethod
    def _build_placeholder_tab(
        icon: str,
        title: str,
        message: str,
        coming_phase: str,
    ) -> QWidget:
        """A friendly placeholder shown inside each not-yet-built tab."""
        wrapper = QWidget()
        wrapper_layout = QVBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(0, t.SPACE_5, 0, 0)
        wrapper_layout.setSpacing(0)
        wrapper_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Card with content — natural sizing, centred horizontally
        card = QFrame()
        card.setObjectName("SettingsPlaceholder")
        card.setMaximumWidth(640)
        card.setStyleSheet(
            f"QFrame#SettingsPlaceholder {{"
            f"  background-color: {t.BG_CARD};"
            f"  border: 1px solid {t.BORDER};"
            f"  border-radius: {t.RADIUS_LG}px;"
            f"}}"
        )

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(
            t.SPACE_8, t.SPACE_8, t.SPACE_8, t.SPACE_8
        )
        card_layout.setSpacing(t.SPACE_3)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(
            "font-size: 56px; background: transparent; padding: 0; margin: 0;"
        )
        card_layout.addWidget(icon_label)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(
            f"color: {t.TEXT_PRIMARY};"
            f"font-size: {t.FONT_SIZE_XL}px;"
            f"font-weight: {t.FONT_WEIGHT_SEMIBOLD};"
            f"background: transparent;"
        )
        card_layout.addWidget(title_label)

        msg_label = QLabel(message)
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg_label.setWordWrap(True)
        msg_label.setStyleSheet(
            f"color: {t.TEXT_MUTED};"
            f"font-size: {t.FONT_SIZE_BASE}px;"
            f"background: transparent;"
        )
        card_layout.addWidget(msg_label)

        card_layout.addSpacing(t.SPACE_2)

        badge_row = QHBoxLayout()
        badge_row.setContentsMargins(0, 0, 0, 0)
        badge_row.addStretch()

        badge = QLabel(coming_phase)
        badge.setStyleSheet(
            f"color: {t.PRIMARY};"
            f"background-color: {t.PRIMARY_LIGHT};"
            f"font-size: {t.FONT_SIZE_XS}px;"
            f"font-weight: {t.FONT_WEIGHT_SEMIBOLD};"
            f"padding: 6px 14px;"
            f"border-radius: 12px;"
        )
        badge_row.addWidget(badge)
        badge_row.addStretch()

        card_layout.addLayout(badge_row)

        # Centre the card horizontally
        center_row = QHBoxLayout()
        center_row.addStretch()
        center_row.addWidget(card)
        center_row.addStretch()

        wrapper_layout.addLayout(center_row)
        wrapper_layout.addStretch()

        return wrapper