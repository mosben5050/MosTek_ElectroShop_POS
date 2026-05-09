"""Sidebar — the main navigation panel of the AppShell.

Dark-navy themed (inspired by modern POS dashboards). Contents:
  - Brand block (logo + "MosTek ElectroPOS" + edition tagline)
  - Toggle button (collapse/expand)
  - Menu items (admin-only items hidden for non-admins)
  - Store information footer (shop name, terminal, cashier)
  - Sign Out button at the very bottom

Emits:
    item_selected(str)  — the key of the menu item that was clicked
    sign_out_clicked()  — user clicked Sign Out
"""
from dataclasses import dataclass
from typing import List, Optional
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton,
    QSizePolicy,
)

from app.resources.styles import tokens as t
from app.resources.assets import logo_path
from app.models.user import User


# ════════════════════════════════════════════════════════════════
@dataclass
class MenuItem:
    key: str
    label: str
    icon: str
    admin_only: bool = False
    is_separator: bool = False


MENU_ITEMS: List[MenuItem] = [
    MenuItem("dashboard", "Dashboard", "🏠"),
    MenuItem("sales",     "Sales",     "💰"),
    MenuItem("repairs",   "Repairs",   "🔧"),
    MenuItem("products",  "Products",  "📦"),
    MenuItem("inventory", "Inventory", "📊"),
    MenuItem("customers", "Customers", "👥"),
    MenuItem("sep1", "", "", is_separator=True),
    MenuItem("users",     "Users",     "🛡️", admin_only=True),
    MenuItem("reports",   "Reports",   "📈", admin_only=True),
    MenuItem("settings",  "Settings",  "⚙️", admin_only=True),
]


class Sidebar(QFrame):
    """Dark-navy collapsible navigation sidebar."""

    item_selected = Signal(str)
    sign_out_clicked = Signal()

    EXPANDED_WIDTH = 260
    COLLAPSED_WIDTH = 72

    def __init__(self, user: User, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self._user = user
        self._is_collapsed = False
        self._buttons: dict[str, QPushButton] = {}
        self._active_key: Optional[str] = None

        self.setObjectName("Sidebar")
        self.setFixedWidth(self.EXPANDED_WIDTH)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        self._build()

    # ────────────────────────────────────────────────────────────
    # Public API
    # ────────────────────────────────────────────────────────────
    def set_active(self, key: str) -> None:
        self._active_key = key
        for k, btn in self._buttons.items():
            btn.setProperty("active", k == key)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def toggle_collapsed(self) -> None:
        self._is_collapsed = not self._is_collapsed
        self.setFixedWidth(
            self.COLLAPSED_WIDTH if self._is_collapsed else self.EXPANDED_WIDTH
        )
        for btn in self._buttons.values():
            self._update_button_text(btn)

        # Hide non-essential elements when collapsed
        is_expanded = not self._is_collapsed

        # Brand block: hide ENTIRELY when collapsed (no logo trace)
        self._brand_widget.setVisible(is_expanded)

        # Sign Out button: icon-only when collapsed
        if self._is_collapsed:
            self._sign_out_btn.setText("🚪")
            self._sign_out_btn.setToolTip("Sign Out")
        else:
            self._sign_out_btn.setText("  🚪    Sign Out")
            self._sign_out_btn.setToolTip("")

    def refresh_store_info(self) -> None:
        """No-op kept for API compatibility (store info now in Settings page)."""
        pass

    # ────────────────────────────────────────────────────────────
    # Build
    # ────────────────────────────────────────────────────────────
    def _build(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(t.SPACE_3, t.SPACE_4, t.SPACE_3, t.SPACE_4)
        layout.setSpacing(t.SPACE_1)


        # ── Brand block ─────────────────────────────────────────
        # ── Brand block (wrapped in a widget so we can hide it as one unit) ──
        self._brand_widget = QWidget()
        self._brand_widget.setStyleSheet("background: transparent;")
        brand_layout = self._build_brand_block()
        self._brand_widget.setLayout(brand_layout)
        layout.addWidget(self._brand_widget)
        layout.addSpacing(t.SPACE_4)

        # ── Menu items ──────────────────────────────────────────
        for item in MENU_ITEMS:
            if item.admin_only and not self._user.is_admin:
                continue

            if item.is_separator:
                sep = QFrame()
                sep.setObjectName("SidebarSeparator")
                sep.setFixedHeight(1)
                layout.addWidget(sep)
                layout.addSpacing(t.SPACE_2)
                continue

            btn = self._make_menu_button(item)
            self._buttons[item.key] = btn
            layout.addWidget(btn)

        # Push everything below to the bottom
            # Push Sign Out to the bottom
            layout.addStretch()

            # Separator before Sign Out
            sep_bottom = QFrame()
            sep_bottom.setObjectName("SidebarSeparator")
            sep_bottom.setFixedHeight(1)
            layout.addWidget(sep_bottom)

            layout.addSpacing(t.SPACE_2)

        # ── Sign Out ────────────────────────────────────────────
        # ── Sign Out ────────────────────────────────────────────
        self._sign_out_btn = QPushButton()
        self._sign_out_btn.setObjectName("SidebarSignOut")
        self._sign_out_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._sign_out_btn.setFixedHeight(44)
        self._sign_out_btn.setText("  🚪    Sign Out")
        self._sign_out_btn.clicked.connect(self.sign_out_clicked.emit)
        layout.addWidget(self._sign_out_btn)


    # ────────────────────────────────────────────────────────────
    def _build_brand_block(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(t.SPACE_2)
        row.setContentsMargins(t.SPACE_2, 0, t.SPACE_2, 0)

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap(logo_path())
        if not pixmap.isNull():
            logo_label.setPixmap(
                pixmap.scaled(
                    40, 40,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        logo_label.setStyleSheet("background: transparent;")
        row.addWidget(logo_label)

        # Brand text
        text_box = QVBoxLayout()
        text_box.setSpacing(0)
        text_box.setContentsMargins(0, 0, 0, 0)

        title = QLabel("MosTek ElectroPOS")
        title.setObjectName("SidebarBrandTitle")
        text_box.addWidget(title)

        self._brand_sub = QLabel("Premium Edition")
        self._brand_sub.setObjectName("SidebarBrandSub")
        text_box.addWidget(self._brand_sub)

        row.addLayout(text_box, stretch=1)
        return row

    def _make_menu_button(self, item: MenuItem) -> QPushButton:
        btn = QPushButton()
        btn.setObjectName("SidebarItem")
        btn.setFixedHeight(48)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setProperty("menu_key", item.key)
        btn.setProperty("active", False)
        btn.setProperty("menu_icon", item.icon)
        btn.setProperty("menu_label", item.label)
        self._update_button_text(btn)
        btn.clicked.connect(lambda _, k=item.key: self._on_item_clicked(k))
        return btn

    def _update_button_text(self, btn: QPushButton) -> None:
        icon = btn.property("menu_icon")
        label = btn.property("menu_label")
        if self._is_collapsed:
            btn.setText(icon)
            btn.setToolTip(label)
        else:
            btn.setText(f"  {icon}    {label}")
            btn.setToolTip("")

    def _on_item_clicked(self, key: str) -> None:
        self.set_active(key)
        self.item_selected.emit(key)

