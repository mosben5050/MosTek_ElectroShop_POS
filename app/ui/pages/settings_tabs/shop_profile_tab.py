"""ShopProfileTab — full-width form with two-column layout and anchored action bar.

Inspired by modern POS settings designs that use the entire content area
rather than a centred narrow card.
"""
from typing import Optional, Dict
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame,
    QSizePolicy,
)

from app.resources.styles import tokens as t
from app.repositories.shop_settings_repo import ShopSettingsRepository
from app.ui.widgets.inputs import TextField
from app.ui.widgets.buttons import PrimaryButton, SecondaryButton


class ShopProfileTab(QWidget):
    """Form for editing the shop's basic profile information."""

    saved = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self._repo = ShopSettingsRepository()
        self._original_values: Dict[str, str] = {}

        self._build()
        self._load_current_values()
        self._wire_dirty_tracking()

    # ────────────────────────────────────────────────────────────
    # Build
    # ────────────────────────────────────────────────────────────
    def _build(self) -> None:
        # Outer layout: form on top fills available space, action bar at bottom
        outer = QVBoxLayout(self)
        outer.setContentsMargins(t.SPACE_4, t.SPACE_5, t.SPACE_4, 0)
        outer.setSpacing(0)

        # Form card — fills the full width AND stretches vertically
        form_card = self._build_form_card()
        outer.addWidget(form_card, stretch=1)

        # Small spacer
        outer.addSpacing(t.SPACE_4)

        # Anchored action bar
        action_bar = self._build_action_bar()
        outer.addWidget(action_bar)

    def _build_form_card(self) -> QFrame:
        """The big card holding all the form fields."""
        card = QFrame()
        card.setObjectName("SettingsFormCard")
        card.setStyleSheet(
            f"QFrame#SettingsFormCard {{"
            f"  background-color: {t.BG_CARD};"
            f"  border: 1px solid {t.BORDER};"
            f"  border-radius: {t.RADIUS_LG}px;"
            f"}}"
        )
        card.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        layout = QVBoxLayout(card)
        layout.setContentsMargins(t.SPACE_8, t.SPACE_6, t.SPACE_8, t.SPACE_6)
        layout.setSpacing(t.SPACE_4)

        # ── Section header (icon + text in horizontal row) ──
        header_row = QHBoxLayout()
        header_row.setSpacing(t.SPACE_4)
        header_row.setContentsMargins(0, 0, 0, 0)

        # Big circular icon on the left
        icon_circle = QLabel("🏪")
        icon_circle.setFixedSize(56, 56)
        icon_circle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_circle.setStyleSheet(
            f"background-color: {t.PRIMARY_LIGHT};"
            f"border-radius: 28px;"
            f"font-size: 24px;"
        )
        header_row.addWidget(icon_circle, alignment=Qt.AlignmentFlag.AlignTop)

        # Title + subtitle stacked vertically
        text_box = QVBoxLayout()
        text_box.setSpacing(2)
        text_box.setContentsMargins(0, 4, 0, 0)

        title_label = QLabel("Shop Information")
        title_label.setStyleSheet(
            f"color: {t.TEXT_PRIMARY};"
            f"font-size: {t.FONT_SIZE_XL}px;"
            f"font-weight: {t.FONT_WEIGHT_SEMIBOLD};"
            f"background: transparent;"
        )
        text_box.addWidget(title_label)

        sub_label = QLabel(
            "Your shop's identity. These details appear on receipts, "
            "the dashboard, and the sidebar."
        )
        sub_label.setStyleSheet(
            f"color: {t.TEXT_MUTED};"
            f"font-size: {t.FONT_SIZE_SM}px;"
            f"background: transparent;"
        )
        sub_label.setWordWrap(True)
        text_box.addWidget(sub_label)

        header_row.addLayout(text_box, stretch=1)
        layout.addLayout(header_row)

        # Divider
        divider = QFrame()
        divider.setFixedHeight(1)
        divider.setStyleSheet(f"background-color: {t.BORDER}; border: none;")
        layout.addWidget(divider)
        layout.addSpacing(t.SPACE_2)

        # ── Form fields in a grid for two-column layout ──
        grid = QGridLayout()
        grid.setHorizontalSpacing(t.SPACE_5)
        grid.setVerticalSpacing(t.SPACE_3)

        # Row 0: Shop name (full width — most important field)
        self._shop_name_field = TextField(
            label="Shop name",
            placeholder="e.g. Albedida Electronics",
            required=True,
            icon="🏪",
            compact=True,
        )
        grid.addWidget(self._shop_name_field, 0, 0, 1, 2)

        # Row 1: Phone | Email (two columns)
        self._phone_field = TextField(
            label="Phone number",
            placeholder="e.g. 0244 123 456",
            required=True,
            icon="📞",
            compact=True,
        )
        grid.addWidget(self._phone_field, 1, 0)

        self._email_field = TextField(
            label="Email (optional)",
            placeholder="e.g. info@albedida.com",
            icon="✉️",
            compact=True,
        )
        grid.addWidget(self._email_field, 1, 1)

        # Row 2: Address (full width)
        self._address_field = TextField(
            label="Address (optional)",
            placeholder="e.g. Asylum Down, Accra",
            icon="📍",
            compact=True,
        )
        grid.addWidget(self._address_field, 2, 0, 1, 2)

        # Row 3: GhanaPost code (left column only — short field)
        self._ghanapost_field = TextField(
            label="GhanaPost digital address (optional)",
            placeholder="e.g. GA-543-0234",
            icon="🗺️",
            compact=True,
        )
        grid.addWidget(self._ghanapost_field, 3, 0)

        # Even column stretch
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        layout.addLayout(grid)

        # ── Footer note ──
        layout.addSpacing(t.SPACE_2)
        note = QLabel(
            "ℹ  Required fields are marked with *. Changes apply across "
            "the app immediately after saving."
        )
        note.setWordWrap(True)
        note.setStyleSheet(
            f"color: {t.TEXT_SECONDARY};"
            f"font-size: {t.FONT_SIZE_SM}px;"
            f"background-color: {t.PRIMARY_LIGHT};"
            f"border-radius: {t.RADIUS_MD}px;"
            f"padding: 12px 16px;"
        )
        layout.addWidget(note)

        # Push content to the top, fill remaining vertical space
        layout.addStretch()

        return card

    def _build_action_bar(self) -> QFrame:
        """Anchored bar at the bottom with Cancel + Save buttons."""
        bar = QFrame()
        bar.setObjectName("SettingsActionBar")
        bar.setFixedHeight(80)
        bar.setStyleSheet(
            f"QFrame#SettingsActionBar {{"
            f"  background-color: {t.BG_CARD};"
            f"  border-top: 1px solid {t.BORDER};"
            f"}}"
        )

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(t.SPACE_6, t.SPACE_3, t.SPACE_6, t.SPACE_3)
        layout.setSpacing(t.SPACE_2)
        layout.addStretch()

        self._cancel_btn = SecondaryButton(
            "Cancel Changes", on_click=self._on_cancel
        )
        layout.addWidget(self._cancel_btn)

        self._save_btn = PrimaryButton(
            "💾  Save Changes", on_click=self._on_save
        )
        self._save_btn.setEnabled(False)
        layout.addWidget(self._save_btn)

        return bar

    # ────────────────────────────────────────────────────────────
    # Load / Save
    # ────────────────────────────────────────────────────────────
    def _load_current_values(self) -> None:
        s = self._repo.get()

        shop_name = s.get("shop_name") or ""
        if shop_name.strip().lower() == "my shop":
            shop_name = ""

        self._shop_name_field.set_text(shop_name)
        self._phone_field.set_text(s.get("phone") or "")
        self._email_field.set_text(s.get("email") or "")
        self._address_field.set_text(s.get("address") or "")
        self._ghanapost_field.set_text(s.get("ghanapost_code") or "")

        self._original_values = {
            "shop_name":      shop_name,
            "phone":          s.get("phone") or "",
            "email":          s.get("email") or "",
            "address":        s.get("address") or "",
            "ghanapost_code": s.get("ghanapost_code") or "",
        }

    def _wire_dirty_tracking(self) -> None:
        for field in [
            self._shop_name_field, self._phone_field,
            self._email_field, self._address_field,
            self._ghanapost_field,
        ]:
            field.text_changed.connect(self._check_dirty)

    def _current_values(self) -> Dict[str, str]:
        return {
            "shop_name":      self._shop_name_field.text().strip(),
            "phone":          self._phone_field.text().strip(),
            "email":          self._email_field.text().strip(),
            "address":        self._address_field.text().strip(),
            "ghanapost_code": self._ghanapost_field.text().strip(),
        }

    def _check_dirty(self) -> None:
        is_dirty = self._current_values() != self._original_values
        self._save_btn.setEnabled(is_dirty)

    # ────────────────────────────────────────────────────────────
    # Action handlers
    # ────────────────────────────────────────────────────────────
    def _on_cancel(self) -> None:
        self._load_current_values()
        self._shop_name_field.clear_error()
        self._phone_field.clear_error()
        self._save_btn.setEnabled(False)

    def _on_save(self) -> None:
        self._shop_name_field.clear_error()
        self._phone_field.clear_error()

        values = self._current_values()

        has_error = False
        if not values["shop_name"]:
            self._shop_name_field.set_error("Shop name is required")
            has_error = True
        if not values["phone"]:
            self._phone_field.set_error("Phone number is required")
            has_error = True

        if has_error:
            return

        self._repo.update(**values)

        self._original_values = values
        self._save_btn.setEnabled(False)

        self._show_success_toast()
        self.saved.emit()

    def _show_success_toast(self) -> None:
        from PySide6.QtCore import QTimer
        from PySide6.QtWidgets import QMessageBox
        msg = QMessageBox(self)
        msg.setWindowTitle("Saved")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("Shop information saved successfully.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        QTimer.singleShot(2000, msg.accept)
        msg.exec()