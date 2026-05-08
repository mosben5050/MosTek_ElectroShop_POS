"""Style showcase — visual reference of every component.

This page exists for two reasons:
  1. As a quick visual test that the theme is rendering correctly
     on whatever machine we're running on.
  2. As a reference for future devs (and future-you) showing every
     component, every colour, and every text size in one place.

Open it on a low-end machine first when validating new builds —
if it looks right here, it'll look right everywhere.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QComboBox,
)

from app.resources.styles import tokens as t
from app.ui.pages.base_page import BasePage
from app.ui.widgets.buttons import (
    PrimaryButton, SecondaryButton, DangerButton, GhostButton,
)
from app.ui.widgets.inputs import TextField, PasswordField, SearchField


class ShowcasePage(BasePage):
    """One page that exercises every component in the design system."""

    def __init__(self, parent=None):
        super().__init__(
            title="Style Showcase",
            subtitle="Every component, colour, and text size in one place",
            parent=parent,
        )

        # Header actions
        self.add_header_action(SecondaryButton("Refresh"))
        self.add_header_action(PrimaryButton("Primary Action"))

        # Sections
        self.content_layout.addWidget(self._typography_section())
        self.content_layout.addWidget(self._buttons_section())
        self.content_layout.addWidget(self._inputs_section())
        self.content_layout.addWidget(self._search_section())
        self.content_layout.addStretch()

    # ────────────────────────────────────────────────────────────
    # Sections
    # ────────────────────────────────────────────────────────────
    def _typography_section(self) -> QWidget:
        card = QGroupBox("Typography")
        layout = QVBoxLayout(card)
        layout.setSpacing(t.SPACE_2)

        # We use direct styling here instead of "role" properties so the
        # demo labels don't conflict with the GroupBox's own QSS rules.
        samples = [
            ("Page Title — 24px Bold", t.FONT_SIZE_2XL, t.FONT_WEIGHT_BOLD,     t.TEXT_PRIMARY),
            ("Section Heading — 20px SemiBold", t.FONT_SIZE_XL, t.FONT_WEIGHT_SEMIBOLD, t.TEXT_PRIMARY),
            ("Subtitle — 16px Medium", t.FONT_SIZE_LG, t.FONT_WEIGHT_MEDIUM, t.TEXT_SECONDARY),
            ("Body text — 14px Regular (default for most UI)", t.FONT_SIZE_BASE, t.FONT_WEIGHT_REGULAR, t.TEXT_PRIMARY),
            ("Muted text — 13px (labels, captions, hints)", t.FONT_SIZE_SM, t.FONT_WEIGHT_REGULAR, t.TEXT_MUTED),
        ]

        for text, size, weight, color in samples:
            lbl = QLabel(text)
            lbl.setStyleSheet(
                f"font-size: {size}px;"
                f"font-weight: {weight};"
                f"color: {color};"
                f"background: transparent;"
            )
            layout.addWidget(lbl)

        return card
    def _buttons_section(self) -> QWidget:
        card = QGroupBox("Buttons")
        layout = QHBoxLayout(card)
        layout.setSpacing(t.SPACE_3)

        layout.addWidget(PrimaryButton("Primary"))
        layout.addWidget(SecondaryButton("Secondary"))
        layout.addWidget(DangerButton("Danger"))
        layout.addWidget(GhostButton("Ghost"))

        disabled_btn = PrimaryButton("Disabled")
        disabled_btn.setEnabled(False)
        layout.addWidget(disabled_btn)

        layout.addStretch()
        return card

    def _inputs_section(self) -> QWidget:
        card = QGroupBox("Form Inputs")
        layout = QVBoxLayout(card)
        layout.setSpacing(t.SPACE_3)

        # Two-column row
        row = QHBoxLayout()
        row.setSpacing(t.SPACE_4)

        name = TextField(
            label="Full name",
            placeholder="e.g. Kwame Mensah",
            required=True,
        )
        row.addWidget(name)

        phone = TextField(
            label="Phone number",
            placeholder="e.g. 0244 123 456",
            required=True,
        )
        phone.set_error("Phone number is required")
        row.addWidget(phone)

        layout.addLayout(row)

        # Password + dropdown row
        row2 = QHBoxLayout()
        row2.setSpacing(t.SPACE_4)

        pin = PasswordField(label="PIN", placeholder="4–6 digits")
        row2.addWidget(pin)

        category_box = QWidget()
        cat_layout = QVBoxLayout(category_box)
        cat_layout.setContentsMargins(0, 0, 0, 0)
        cat_layout.setSpacing(t.SPACE_1)

        cat_label = QLabel("Category")
        cat_label.setStyleSheet(
            f"color: {t.TEXT_SECONDARY};"
            f"font-size: {t.FONT_SIZE_SM}px;"
            f"font-weight: {t.FONT_WEIGHT_MEDIUM};"
        )
        cat_layout.addWidget(cat_label)

        combo = QComboBox()
        combo.addItems(["Phones", "Laptops", "Accessories", "Repairs"])
        cat_layout.addWidget(combo)

        row2.addWidget(category_box)

        layout.addLayout(row2)
        return card

    def _search_section(self) -> QWidget:
        card = QGroupBox("Search")
        layout = QVBoxLayout(card)

        search = SearchField(placeholder="Search products, customers, repairs...")
        layout.addWidget(search)

        return card