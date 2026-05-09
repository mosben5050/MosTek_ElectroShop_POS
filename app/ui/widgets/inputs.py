"""Form input widgets.

Wrappers around QLineEdit that bundle a label + input + error text
into one composite widget.

Classes:
  TextField     — labelled single-line text input (with optional prefix icon)
  PasswordField — labelled password input (masks characters)
  SearchField   — input with a search icon prefix, no label
"""
from typing import Optional
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSizePolicy, QFrame,
)

from app.resources.styles import tokens as t


# ════════════════════════════════════════════════════════════════
# TextField
# ════════════════════════════════════════════════════════════════
class TextField(QWidget):
    """A labelled text input with optional inline error message and prefix icon.

    When an icon is provided, we build a "fake input": a styled QFrame
    that contains the icon + a borderless QLineEdit side by side.

    Set compact=True for use inside dialogs and dense forms (40px tall).
    Default is the premium 52px height used on the login screen.
    """

    text_changed = Signal(str)

    def __init__(
        self,
        label: str = "",
        placeholder: str = "",
        required: bool = False,
        icon: str = "",
        compact: bool = False,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(t.SPACE_1)

        # ── Label (optional) ─────────────────────────────────────
        self._label = None
        if label:
            label_text = f"{label} *" if required else label
            self._label = QLabel(label_text)
            self._label.setStyleSheet(
                f"color: {t.TEXT_SECONDARY};"
                f"font-size: {t.FONT_SIZE_SM}px;"
                f"font-weight: {t.FONT_WEIGHT_MEDIUM};"
                f"background: transparent;"
            )
            layout.addWidget(self._label)

        # Determine the height we'll use everywhere below
        input_height = t.INPUT_HEIGHT_COMPACT if compact else t.INPUT_HEIGHT

        # ── Input (with or without icon) ─────────────────────────
        if icon:
            self._frame = QFrame()
            self._frame.setObjectName("InputFrame")
            self._frame.setFixedHeight(input_height)
            self._frame.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
            )

            frame_layout = QHBoxLayout(self._frame)
            frame_layout.setContentsMargins(18, 0, 18, 0)
            frame_layout.setSpacing(14)
            frame_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

            # Icon — fixed size, vertically centred
            self._icon_label = QLabel(icon)
            self._icon_label.setFixedSize(20, 20)
            self._icon_label.setAlignment(
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter
            )
            self._icon_label.setStyleSheet(
                f"color: {t.TEXT_MUTED};"
                f"font-size: 16px;"
                f"background: transparent;"
                f"border: none;"
                f"padding: 0;"
                f"margin: 0;"
            )
            frame_layout.addWidget(self._icon_label, alignment=Qt.AlignmentFlag.AlignVCenter)

            # Borderless input — frame provides the border
            self._input = QLineEdit()
            self._input.setPlaceholderText(placeholder)
            self._input.textChanged.connect(self.text_changed.emit)
            self._input.setStyleSheet(
                "QLineEdit {"
                "  background: transparent;"
                "  border: none;"
                "  padding: 0;"
                "  margin: 0;"
                f"  color: {t.TEXT_PRIMARY};"
                f"  font-size: {t.INPUT_FONT_SIZE}px;"
                f"  font-weight: {t.FONT_WEIGHT_MEDIUM};"
                "  min-height: 0;"
                "}"
            )
            frame_layout.addWidget(self._input, stretch=1)

            layout.addWidget(self._frame)
        else:
            self._frame = None
            self._icon_label = None
            self._input = QLineEdit()
            self._input.setPlaceholderText(placeholder)
            self._input.textChanged.connect(self.text_changed.emit)
            if compact:
                self._input.setFixedHeight(input_height)
            layout.addWidget(self._input)

        # ── Error label ──────────────────────────────────────────
        self._error_label = QLabel("")
        self._error_label.setStyleSheet(
            f"color: {t.DANGER};"
            f"font-size: {t.FONT_SIZE_XS}px;"
            f"background: transparent;"
            f"padding-top: 4px;"
        )
        self._error_label.setMinimumHeight(22)
        self._error_label.setWordWrap(True)
        self._error_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        self._error_label.hide()
        layout.addWidget(self._error_label)

    # ────────────────────────────────────────────────────────────
    # Public API
    # ────────────────────────────────────────────────────────────
    def text(self) -> str:
        return self._input.text()

    def set_text(self, value: str) -> None:
        self._input.setText(value)

    def set_placeholder(self, value: str) -> None:
        self._input.setPlaceholderText(value)

    def set_error(self, message: Optional[str]) -> None:
        target = self._frame if self._frame is not None else self._input

        if message:
            self._error_label.setText(message)
            self._error_label.show()
            target.setProperty("state", "error")
        else:
            self._error_label.hide()
            target.setProperty("state", "")

        target.style().unpolish(target)
        target.style().polish(target)

    def clear_error(self) -> None:
        self.set_error(None)

    def set_focus(self) -> None:
        self._input.setFocus()

    @property
    def line_edit(self) -> QLineEdit:
        return self._input


# ════════════════════════════════════════════════════════════════
# PasswordField
# ════════════════════════════════════════════════════════════════
class PasswordField(TextField):
    """Labelled password input (characters masked)."""

    def __init__(
        self,
        label: str = "Password",
        placeholder: str = "",
        required: bool = False,
        icon: str = "",
        compact: bool = False,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(label, placeholder, required, icon, compact, parent)
        self._input.setEchoMode(QLineEdit.EchoMode.Password)


# ════════════════════════════════════════════════════════════════
# SearchField
# ════════════════════════════════════════════════════════════════
class SearchField(QWidget):
    """Single search input with a magnifier icon prefix."""

    text_changed = Signal(str)

    def __init__(
        self,
        placeholder: str = "Search...",
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)

        self._input = QLineEdit()
        self._input.textChanged.connect(self.text_changed.emit)
        self._input.setMinimumWidth(280)
        self._input.setPlaceholderText(f"\U0001F50D  {placeholder}")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._input)

    def text(self) -> str:
        return self._input.text()

    def set_text(self, value: str) -> None:
        self._input.setText(value)

    def clear(self) -> None:
        self._input.clear()

    @property
    def line_edit(self) -> QLineEdit:
        return self._input