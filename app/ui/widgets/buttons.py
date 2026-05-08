"""Standard button widgets.

All buttons in the app should use one of these classes rather than
QPushButton directly. This guarantees consistent styling and gives us
one place to evolve button behaviour (loading states, icons, etc.).

Variants:
  PrimaryButton    — main call-to-action (Save, Submit, Confirm)
  SecondaryButton  — neutral action (Cancel, Close)
  DangerButton     — destructive action (Delete, Void, Remove)
  GhostButton      — minimal / link-style (Learn more, View details)
"""
from typing import Callable, Optional
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QWidget


class _BaseButton(QPushButton):
    """Internal base — sets up text, click handler, optional icon."""

    VARIANT: str = ""  # subclasses override

    def __init__(
        self,
        text: str = "",
        on_click: Optional[Callable] = None,
        parent: Optional[QWidget] = None,
        icon: Optional[QIcon] = None,
    ):
        super().__init__(parent)

        # Set the variant property and force Qt to re-evaluate styles
        if self.VARIANT:
            self.setProperty("variant", self.VARIANT)

        self.setText(text)

        if icon is not None:
            self.setIcon(icon)
            self.setIconSize(QSize(16, 16))

        if on_click is not None:
            self.clicked.connect(on_click)

        # Pointing-hand cursor on hover (web-app feel)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Force Qt to re-apply styles now that the variant property is set
        self.style().unpolish(self)
        self.style().polish(self)


class PrimaryButton(_BaseButton):
    VARIANT = "primary"


class SecondaryButton(_BaseButton):
    VARIANT = ""  # default QPushButton style is the secondary look


class DangerButton(_BaseButton):
    VARIANT = "danger"


class GhostButton(_BaseButton):
    VARIANT = "ghost"