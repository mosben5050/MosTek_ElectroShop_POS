"""TaxCurrencyTab — currency and tax configuration.

Tax registration is presented as 3 selectable cards (none / flat-rate / VAT)
rather than a dropdown — easier to scan, harder to misclick. When VAT is
selected, the detailed rate inputs appear below.
"""
from typing import Optional, Dict, Any
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame,
    QSizePolicy, QComboBox, QDoubleSpinBox, QPushButton,
)

from app.resources.styles import tokens as t
from app.repositories.shop_settings_repo import ShopSettingsRepository
from app.ui.widgets.buttons import PrimaryButton, SecondaryButton


class TaxCurrencyTab(QWidget):
    """Form for editing currency symbol and tax registration."""

    saved = Signal()

    CURRENCY_OPTIONS = [
        ("GHS", "Ghanaian Cedi (GHS)"),
        ("GH₵", "Ghanaian Cedi (GH₵)"),
        ("NGN", "Nigerian Naira (NGN)"),
        ("USD", "US Dollar (USD)"),
        ("EUR", "Euro (EUR)"),
        ("GBP", "British Pound (GBP)"),
    ]

    TAX_MODES = [
        {
            "key": "none",
            "icon": "🚫",
            "title": "Not Registered",
            "desc": "No tax added — small shop or below VAT threshold.",
        },
        {
            "key": "flat_rate",
            "icon": "📊",
            "title": "Flat Rate (3%)",
            "desc": "Simplified scheme for shops earning ≤ GHS 500K/yr.",
        },
        {
            "key": "vat_standard",
            "icon": "🏛️",
            "title": "Full VAT",
            "desc": "Standard VAT + NHIL + GETFund + COVID levy.",
        },
    ]

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self._repo = ShopSettingsRepository()
        self._original_values: Dict[str, Any] = {}
        self._tax_mode_buttons: Dict[str, QPushButton] = {}
        self._current_tax_mode: str = "none"

        self._build()
        self._load_current_values()
        self._wire_dirty_tracking()

    # ────────────────────────────────────────────────────────────
    # Build
    # ────────────────────────────────────────────────────────────
    def _build(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(t.SPACE_4, t.SPACE_5, t.SPACE_4, 0)
        outer.setSpacing(0)

        form_card = self._build_form_card()
        outer.addWidget(form_card, stretch=1)

        outer.addSpacing(t.SPACE_4)

        action_bar = self._build_action_bar()
        outer.addWidget(action_bar)

    def _build_form_card(self) -> QFrame:
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

        # ── Section header ──
        header_row = QHBoxLayout()
        header_row.setSpacing(t.SPACE_4)
        header_row.setContentsMargins(0, 0, 0, 0)

        icon_circle = QLabel("💰")
        icon_circle.setFixedSize(56, 56)
        icon_circle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_circle.setStyleSheet(
            f"background-color: {t.PRIMARY_LIGHT};"
            f"border-radius: 28px;"
            f"font-size: 24px;"
        )
        header_row.addWidget(icon_circle, alignment=Qt.AlignmentFlag.AlignTop)

        text_box = QVBoxLayout()
        text_box.setSpacing(2)
        text_box.setContentsMargins(0, 4, 0, 0)

        title_label = QLabel("Tax & Currency")
        title_label.setStyleSheet(
            f"color: {t.TEXT_PRIMARY};"
            f"font-size: {t.FONT_SIZE_XL}px;"
            f"font-weight: {t.FONT_WEIGHT_SEMIBOLD};"
            f"background: transparent;"
        )
        text_box.addWidget(title_label)

        sub_label = QLabel(
            "Configure how prices, taxes, and totals are calculated "
            "across the app."
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

        # ── Currency section ──
        layout.addWidget(self._make_field_label("Currency"))

        self._currency_combo = QComboBox()
        for code, label in self.CURRENCY_OPTIONS:
            self._currency_combo.addItem(label, userData=code)
        self._currency_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        self._currency_combo.setFixedHeight(t.INPUT_HEIGHT_COMPACT)
        layout.addWidget(self._currency_combo)

        layout.addSpacing(t.SPACE_4)

        # ── Tax registration section ──
        layout.addWidget(self._make_field_label("Tax registration"))

        tax_modes_row = QHBoxLayout()
        tax_modes_row.setSpacing(t.SPACE_3)
        tax_modes_row.setContentsMargins(0, 0, 0, 0)

        for mode in self.TAX_MODES:
            btn = self._make_tax_mode_card(mode)
            self._tax_mode_buttons[mode["key"]] = btn
            tax_modes_row.addWidget(btn, stretch=1)

        layout.addLayout(tax_modes_row)

        layout.addSpacing(t.SPACE_4)

        # ── VAT details (shown only when VAT mode selected) ──
        self._vat_panel = self._build_vat_panel()
        layout.addWidget(self._vat_panel)
        self._vat_panel.hide()  # hidden by default

        # ── Footer info ──
        layout.addStretch()

        info = QLabel(
            "ℹ  Tax settings affect new sales only — existing receipts are "
            "preserved as-is. For VAT registration, contact GRA at 0302-686-700."
        )
        info.setWordWrap(True)
        info.setStyleSheet(
            f"color: {t.TEXT_SECONDARY};"
            f"font-size: {t.FONT_SIZE_SM}px;"
            f"background-color: {t.PRIMARY_LIGHT};"
            f"border-radius: {t.RADIUS_MD}px;"
            f"padding: 12px 16px;"
        )
        layout.addWidget(info)

        return card

    def _build_vat_panel(self) -> QFrame:
        """The 4 VAT rate inputs — only visible when VAT mode is selected."""
        panel = QFrame()
        panel.setStyleSheet(
            f"background-color: {t.BG_HOVER};"
            f"border-radius: {t.RADIUS_MD}px;"
        )

        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(t.SPACE_5, t.SPACE_4, t.SPACE_5, t.SPACE_4)
        panel_layout.setSpacing(t.SPACE_3)

        title = QLabel("VAT rates (Ghana standard)")
        title.setStyleSheet(
            f"color: {t.TEXT_PRIMARY};"
            f"font-size: {t.FONT_SIZE_BASE}px;"
            f"font-weight: {t.FONT_WEIGHT_SEMIBOLD};"
            f"background: transparent;"
        )
        panel_layout.addWidget(title)

        # Grid of 4 percentage inputs (2 columns)
        grid = QGridLayout()
        grid.setHorizontalSpacing(t.SPACE_5)
        grid.setVerticalSpacing(t.SPACE_3)

        self._vat_rate = self._make_percent_input(default=15.0)
        self._nhil_rate = self._make_percent_input(default=2.5)
        self._getfund_rate = self._make_percent_input(default=2.5)
        self._covid_rate = self._make_percent_input(default=1.0)

        grid.addLayout(self._wrap_with_label("VAT", self._vat_rate), 0, 0)
        grid.addLayout(self._wrap_with_label("NHIL", self._nhil_rate), 0, 1)
        grid.addLayout(self._wrap_with_label("GETFund", self._getfund_rate), 1, 0)
        grid.addLayout(self._wrap_with_label("COVID levy", self._covid_rate), 1, 1)

        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        panel_layout.addLayout(grid)

        return panel

    def _make_percent_input(self, default: float) -> QDoubleSpinBox:
        """A spin box that reads as a percentage (0.0 – 100.0)."""
        spin = QDoubleSpinBox()
        spin.setRange(0.0, 100.0)
        spin.setSingleStep(0.5)
        spin.setDecimals(2)
        spin.setSuffix(" %")
        spin.setValue(default)
        spin.setFixedHeight(t.INPUT_HEIGHT_COMPACT)
        spin.setCursor(Qt.CursorShape.IBeamCursor)
        return spin

    def _wrap_with_label(self, label_text: str, widget: QWidget) -> QVBoxLayout:
        """Wrap an input widget with a label above it."""
        box = QVBoxLayout()
        box.setSpacing(t.SPACE_1)
        box.setContentsMargins(0, 0, 0, 0)

        label = QLabel(label_text)
        label.setStyleSheet(
            f"color: {t.TEXT_SECONDARY};"
            f"font-size: {t.FONT_SIZE_SM}px;"
            f"font-weight: {t.FONT_WEIGHT_MEDIUM};"
            f"background: transparent;"
        )
        box.addWidget(label)
        box.addWidget(widget)
        return box

    @staticmethod
    def _make_field_label(text: str) -> QLabel:
        label = QLabel(text)
        label.setStyleSheet(
            f"color: {t.TEXT_SECONDARY};"
            f"font-size: {t.FONT_SIZE_SM}px;"
            f"font-weight: {t.FONT_WEIGHT_MEDIUM};"
            f"background: transparent;"
        )
        return label

    def _make_tax_mode_card(self, mode: Dict[str, str]) -> QPushButton:
        """A selectable card for one tax mode."""
        btn = QPushButton()
        btn.setObjectName("TaxModeCard")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(120)
        btn.setCheckable(True)
        btn.setProperty("selected", False)

        # Build the inner layout
        inner = QVBoxLayout(btn)
        inner.setContentsMargins(t.SPACE_4, t.SPACE_3, t.SPACE_4, t.SPACE_3)
        inner.setSpacing(t.SPACE_1)
        inner.setAlignment(Qt.AlignmentFlag.AlignTop)

        icon = QLabel(mode["icon"])
        icon.setStyleSheet(
            "font-size: 24px; background: transparent;"
        )
        icon.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        inner.addWidget(icon)

        title = QLabel(mode["title"])
        title.setStyleSheet(
            f"color: {t.TEXT_PRIMARY};"
            f"font-size: {t.FONT_SIZE_BASE}px;"
            f"font-weight: {t.FONT_WEIGHT_SEMIBOLD};"
            f"background: transparent;"
        )
        title.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        inner.addWidget(title)

        desc = QLabel(mode["desc"])
        desc.setWordWrap(True)
        desc.setStyleSheet(
            f"color: {t.TEXT_MUTED};"
            f"font-size: {t.FONT_SIZE_SM}px;"
            f"background: transparent;"
        )
        desc.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        inner.addWidget(desc)

        inner.addStretch()

        btn.clicked.connect(lambda: self._select_tax_mode(mode["key"]))
        return btn

    def _select_tax_mode(self, key: str) -> None:
        """Highlight the chosen card and show/hide VAT panel as needed."""
        self._current_tax_mode = key

        for k, btn in self._tax_mode_buttons.items():
            btn.setProperty("selected", k == key)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        # Show VAT details only for VAT mode
        self._vat_panel.setVisible(key == "vat_standard")

        self._check_dirty()

    def _build_action_bar(self) -> QFrame:
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

        # Currency
        currency = s.get("currency_symbol") or "GHS"
        for i in range(self._currency_combo.count()):
            if self._currency_combo.itemData(i) == currency:
                self._currency_combo.setCurrentIndex(i)
                break

        # Tax mode
        tax_mode = s.get("tax_mode") or "none"
        self._select_tax_mode(tax_mode)

        # VAT rates
        self._vat_rate.setValue(float(s.get("vat_pct") or 15.0))
        self._nhil_rate.setValue(float(s.get("nhil_pct") or 2.5))
        self._getfund_rate.setValue(float(s.get("getfund_pct") or 2.5))
        self._covid_rate.setValue(float(s.get("covid_pct") or 1.0))

        self._original_values = self._current_values()
        self._save_btn.setEnabled(False)

    def _wire_dirty_tracking(self) -> None:
        self._currency_combo.currentIndexChanged.connect(self._check_dirty)
        for spin in [
            self._vat_rate, self._nhil_rate,
            self._getfund_rate, self._covid_rate,
        ]:
            spin.valueChanged.connect(self._check_dirty)
        # Tax mode dirty check is wired via _select_tax_mode

    def _current_values(self) -> Dict[str, Any]:
        return {
            "currency_symbol": self._currency_combo.currentData(),
            "tax_mode":        self._current_tax_mode,
            "vat_pct":         self._vat_rate.value(),
            "nhil_pct":        self._nhil_rate.value(),
            "getfund_pct":     self._getfund_rate.value(),
            "covid_pct":       self._covid_rate.value(),
        }

    def _check_dirty(self) -> None:
        is_dirty = self._current_values() != self._original_values
        self._save_btn.setEnabled(is_dirty)

    # ────────────────────────────────────────────────────────────
    # Action handlers
    # ────────────────────────────────────────────────────────────
    def _on_cancel(self) -> None:
        self._load_current_values()

    def _on_save(self) -> None:
        values = self._current_values()
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
        msg.setText("Tax & currency settings saved successfully.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        QTimer.singleShot(2000, msg.accept)
        msg.exec()