"""FeatureRow — used on the login page to display product features.

Layout:
    [icon]   Title
             Description text here

Supports two visual modes via the on_dark parameter:
  on_dark=False (default) — for light backgrounds
  on_dark=True            — for dark backgrounds (login page over photo)
"""
from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel

from app.resources.styles import tokens as t


class FeatureRow(QWidget):
    """A single icon + title + description row."""

    def __init__(
        self,
        icon: str,
        title: str,
        description: str,
        on_dark: bool = False,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)

        # Choose colours based on background type
        if on_dark:
            icon_bg     = "rgba(255, 255, 255, 0.1)"
            icon_border = t.ACCENT
            title_color = t.TEXT_INVERSE
            desc_color  = "rgba(255, 255, 255, 0.7)"
        else:
            icon_bg     = t.BG_CARD
            icon_border = t.ACCENT
            title_color = t.TEXT_PRIMARY
            desc_color  = t.TEXT_MUTED

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(t.SPACE_4)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # ── Icon ────────────────────────────────────────────────
        icon_label = QLabel(icon)
        icon_label.setFixedSize(48, 48)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(
            f"background-color: {icon_bg};"
            f"border: 1px solid {icon_border};"
            f"border-radius: {t.RADIUS_LG}px;"
            f"font-size: 22px;"
        )
        layout.addWidget(icon_label)

        # ── Text block (title + description) ────────────────────
        text_box = QVBoxLayout()
        text_box.setContentsMargins(0, 0, 0, 0)
        text_box.setSpacing(2)

        title_label = QLabel(title)
        title_label.setStyleSheet(
            f"color: {title_color};"
            f"font-size: {t.FONT_SIZE_LG}px;"
            f"font-weight: {t.FONT_WEIGHT_SEMIBOLD};"
            f"background: transparent;"
        )
        text_box.addWidget(title_label)

        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet(
            f"color: {desc_color};"
            f"font-size: {t.FONT_SIZE_SM}px;"
            f"background: transparent;"
        )
        text_box.addWidget(desc_label)

        layout.addLayout(text_box, stretch=1)