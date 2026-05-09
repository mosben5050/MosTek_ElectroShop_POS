"""UserMenu — popup menu shown when the user clicks their pill in the TopBar.

Items: My profile, Change password, Preferences, About, Sign Out.

Emits `action_selected(str)` with the action key. The AppShell decides
what to do for each.
"""
from typing import Optional
from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtWidgets import QMenu, QWidget

from app.resources.styles import tokens as t


class UserMenu(QMenu):
    """Dropdown menu attached to the user pill."""

    action_selected = Signal(str)

    ACTIONS = [
        ("profile",         "👤  My Profile"),
        ("change_password", "🔑  Change Password"),
        ("preferences",     "⚙️  Preferences"),
        ("about",           "ℹ️  About"),
        ("__separator__",   ""),
        ("sign_out",        "🚪  Sign Out"),
    ]

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.setMinimumWidth(220)
        self.setStyleSheet(
            f"QMenu {{"
            f"  background-color: {t.BG_CARD};"
            f"  border: 1px solid {t.BORDER};"
            f"  border-radius: {t.RADIUS_MD}px;"
            f"  padding: 6px;"
            f"}}"
            f"QMenu::item {{"
            f"  padding: 10px 16px;"
            f"  border-radius: {t.RADIUS_SM}px;"
            f"  color: {t.TEXT_PRIMARY};"
            f"  font-size: {t.FONT_SIZE_BASE}px;"
            f"}}"
            f"QMenu::item:selected {{"
            f"  background-color: {t.PRIMARY_LIGHT};"
            f"  color: {t.PRIMARY};"
            f"}}"
            f"QMenu::separator {{"
            f"  height: 1px;"
            f"  background: {t.BORDER};"
            f"  margin: 6px 8px;"
            f"}}"
        )

        for key, label in self.ACTIONS:
            if key == "__separator__":
                self.addSeparator()
                continue

            action = self.addAction(label)
            action.triggered.connect(
                lambda _checked=False, k=key: self.action_selected.emit(k)
            )

    def show_below(self, anchor_widget: QWidget) -> None:
        """Pop up the menu just below the given widget, right-aligned."""
        global_bottom_right = anchor_widget.mapToGlobal(
            QPoint(anchor_widget.width(), anchor_widget.height() + 4)
        )
        # Right-align: shift left by menu width
        self.exec(
            QPoint(
                global_bottom_right.x() - self.sizeHint().width(),
                global_bottom_right.y(),
            )
        )