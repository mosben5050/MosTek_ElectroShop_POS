"""ConfirmDialog — a reusable yes/no confirmation dialog.

Designed for actions like sign out, delete, void, etc. Where pressing
the destructive button has consequences the user should think about.

Usage:
    if ConfirmDialog.ask(
        parent=self,
        title="Sign Out?",
        message="You'll need to sign in again to continue.",
        confirm_text="Sign Out",
        is_destructive=True,
    ):
        # user clicked the confirm button
        do_the_thing()
"""
from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout

from app.resources.styles import tokens as t
from app.ui.dialogs.base_dialog import BaseDialog
from app.ui.widgets.buttons import PrimaryButton, SecondaryButton, DangerButton


class ConfirmDialog(BaseDialog):
    """A simple Yes/No confirmation modal."""

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        title: str = "Are you sure?",
        message: str = "This action cannot be undone.",
        confirm_text: str = "Confirm",
        cancel_text: str = "Cancel",
        is_destructive: bool = False,
        icon: str = "❓",
    ):
        super().__init__(
            parent=parent,
            title=title,
            min_width=440,
            min_height=240,
        )

        self._build_content(message, icon)
        self._build_footer_buttons(confirm_text, cancel_text, is_destructive)

    # ────────────────────────────────────────────────────────────
    # Class method for one-line usage
    # ────────────────────────────────────────────────────────────
    @classmethod
    def ask(
        cls,
        parent: Optional[QWidget] = None,
        title: str = "Are you sure?",
        message: str = "",
        confirm_text: str = "Confirm",
        cancel_text: str = "Cancel",
        is_destructive: bool = False,
        icon: str = "❓",
    ) -> bool:
        """Show the dialog and return True if the user confirmed."""
        from PySide6.QtWidgets import QDialog
        dlg = cls(
            parent=parent,
            title=title,
            message=message,
            confirm_text=confirm_text,
            cancel_text=cancel_text,
            is_destructive=is_destructive,
            icon=icon,
        )
        return dlg.exec() == QDialog.DialogCode.Accepted

    # ────────────────────────────────────────────────────────────
    def _build_content(self, message: str, icon: str) -> None:
        # Icon + message side by side
        row = QHBoxLayout()
        row.setSpacing(t.SPACE_4)
        row.setContentsMargins(0, t.SPACE_3, 0, t.SPACE_3)

        # Icon
        icon_label = QLabel(icon)
        icon_label.setFixedSize(56, 56)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(
            f"background-color: {t.PRIMARY_LIGHT};"
            f"color: {t.PRIMARY};"
            f"border-radius: 28px;"
            f"font-size: 24px;"
        )
        row.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignTop)

        # Message
        msg = QLabel(message)
        msg.setWordWrap(True)
        msg.setStyleSheet(
            f"color: {t.TEXT_PRIMARY};"
            f"font-size: {t.FONT_SIZE_BASE}px;"
            f"background: transparent;"
            f"padding-top: 8px;"
        )
        row.addWidget(msg, stretch=1)

        self.content_layout.addLayout(row)
        self.content_layout.addStretch()

    def _build_footer_buttons(
            self, confirm_text: str, cancel_text: str, is_destructive: bool
    ) -> None:
        self.add_footer_button(
            SecondaryButton(cancel_text, on_click=self.reject)
        )

        if is_destructive:
            confirm_btn = DangerButton(confirm_text, on_click=self.accept)
        else:
            confirm_btn = PrimaryButton(confirm_text, on_click=self.accept)
        self.add_footer_button(confirm_btn)