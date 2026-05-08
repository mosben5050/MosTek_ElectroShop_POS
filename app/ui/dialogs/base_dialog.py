"""BaseDialog — the foundation every modal in the app inherits from.

Provides:
  - Automatic centering on the parent window
  - Maximum size constraint (never larger than 90% of screen)
  - Consistent margins and spacing
  - A modal flag that's correctly set
  - A standard "header + content + footer" layout helper

Usage:
    class AddCustomerDialog(BaseDialog):
        def __init__(self, parent=None):
            super().__init__(parent, title="Add Customer")
            # build self.content_layout here
"""
from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QApplication, QWidget,
)

from app.resources.styles import tokens as t


class BaseDialog(QDialog):
    """Standard dialog with header, content area, and footer."""

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        title: str = "",
        min_width: int = 480,
        min_height: int = 280,
    ):
        super().__init__(parent)

        # --- window flags & behaviour ---
        self.setWindowTitle(title)
        self.setModal(True)
        # Remove the small "?" help button on Windows title bars
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowContextHelpButtonHint
        )

        # --- size constraints ---
        self.setMinimumSize(min_width, min_height)
        self._apply_max_size_constraint()

        # --- root layout: header / content / footer ---
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Header
        header = self._build_header(title)
        root.addWidget(header)

        # Content area (subclasses fill self.content_layout)
        content_wrapper = QWidget()
        self.content_layout = QVBoxLayout(content_wrapper)
        self.content_layout.setContentsMargins(
            t.SPACE_6, t.SPACE_6, t.SPACE_6, t.SPACE_6
        )
        self.content_layout.setSpacing(t.SPACE_3)
        root.addWidget(content_wrapper, stretch=1)

        # Footer (subclasses can add buttons via add_footer_button)
        self._footer = self._build_footer()
        root.addWidget(self._footer)

    # ────────────────────────────────────────────────────────────
    # Layout helpers
    # ────────────────────────────────────────────────────────────
    def _build_header(self, title: str) -> QWidget:
        header = QFrame()
        # Use objectName + global stylesheet rule instead of inline styling
        header.setObjectName("DialogHeader")

        layout = QHBoxLayout(header)
        layout.setContentsMargins(t.SPACE_6, t.SPACE_4, t.SPACE_6, t.SPACE_4)

        title_label = QLabel(title)
        title_label.setProperty("role", "section")
        layout.addWidget(title_label)
        layout.addStretch()

        return header

    def _build_footer(self) -> QWidget:
        footer = QFrame()
        # Use objectName + global stylesheet rule instead of inline styling
        footer.setObjectName("DialogFooter")

        self._footer_layout = QHBoxLayout(footer)
        self._footer_layout.setContentsMargins(
            t.SPACE_6, t.SPACE_3, t.SPACE_6, t.SPACE_3
        )
        self._footer_layout.setSpacing(t.SPACE_2)
        self._footer_layout.addStretch()
        return footer

    def add_footer_button(self, button: QPushButton) -> None:
        """Append a button to the right side of the footer."""
        self._footer_layout.addWidget(button)

    # ────────────────────────────────────────────────────────────
    # Size & position
    # ────────────────────────────────────────────────────────────
    def _apply_max_size_constraint(self) -> None:
        """Cap the dialog at 90% of the available screen size."""
        screen = QApplication.primaryScreen()
        if screen:
            geo = screen.availableGeometry()
            self.setMaximumSize(int(geo.width() * 0.9), int(geo.height() * 0.9))

    def showEvent(self, event):
        """Centre the dialog on the parent (or screen) every time it opens."""
        super().showEvent(event)
        self._center_on_parent()

    def _center_on_parent(self) -> None:
        parent = self.parent()
        if parent is not None and hasattr(parent, "geometry"):
            ref_geo = parent.geometry()
        else:
            screen = QApplication.primaryScreen()
            ref_geo = screen.availableGeometry() if screen else self.geometry()

        x = ref_geo.x() + (ref_geo.width() - self.width()) // 2
        y = ref_geo.y() + (ref_geo.height() - self.height()) // 2
        self.move(x, y)