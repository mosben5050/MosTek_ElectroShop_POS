"""Global QSS stylesheet builder.

Builds the application-wide stylesheet by injecting design tokens
into a QSS template. Called once at startup by theme.apply_theme().

QSS reference: https://doc.qt.io/qt-6/stylesheet-reference.html
"""
from app.resources.styles import tokens as t


def build_stylesheet() -> str:
    """Return the full QSS stylesheet for the application."""
    return f"""
/* ════════════════════════════════════════════════════════════════
   GLOBAL — every widget inherits these
   ════════════════════════════════════════════════════════════════ */
* {{
    font-family: "{t.FONT_FAMILY}", "Segoe UI", system-ui, sans-serif;
    font-size: {t.FONT_SIZE_BASE}px;
    color: {t.TEXT_PRIMARY};
    outline: none;
}}

QWidget {{
    background-color: {t.BG_APP};
    color: {t.TEXT_PRIMARY};
}}

QMainWindow {{
    background-color: {t.BG_APP};
}}

/* ════════════════════════════════════════════════════════════════
   LABELS
   ════════════════════════════════════════════════════════════════ */
QLabel {{
    background-color: transparent;
    color: {t.TEXT_PRIMARY};
}}

QLabel[role="title"] {{
    font-size: {t.FONT_SIZE_2XL}px;
    font-weight: {t.FONT_WEIGHT_BOLD};
    color: {t.TEXT_PRIMARY};
}}

QLabel[role="subtitle"] {{
    font-size: {t.FONT_SIZE_LG}px;
    font-weight: {t.FONT_WEIGHT_MEDIUM};
    color: {t.TEXT_SECONDARY};
}}

QLabel[role="muted"] {{
    color: {t.TEXT_MUTED};
    font-size: {t.FONT_SIZE_SM}px;
}}

QLabel[role="section"] {{
    font-size: {t.FONT_SIZE_XL}px;
    font-weight: {t.FONT_WEIGHT_SEMIBOLD};
    color: {t.TEXT_PRIMARY};
}}

/* ════════════════════════════════════════════════════════════════
   BUTTONS — default = secondary style
   ════════════════════════════════════════════════════════════════ */
QPushButton {{
    background-color: {t.BG_CARD};
    color: {t.TEXT_PRIMARY};
    border: 1px solid {t.BORDER_STRONG};
    border-radius: {t.RADIUS_MD}px;
    padding: 8px 16px;
    min-height: {t.BUTTON_HEIGHT}px;
    font-weight: {t.FONT_WEIGHT_MEDIUM};
}}

QPushButton:hover {{
    background-color: {t.BG_HOVER};
    border-color: {t.TEXT_MUTED};
}}

QPushButton:pressed {{
    background-color: {t.BG_ACTIVE};
}}

QPushButton:disabled {{
    background-color: {t.BG_DISABLED};
    color: {t.TEXT_DISABLED};
    border-color: {t.BORDER};
}}

/* Primary button — main call-to-action */
QPushButton[variant="primary"] {{
    background-color: {t.PRIMARY};
    color: {t.PRIMARY_TEXT};
    border: 1px solid {t.PRIMARY};
}}

QPushButton[variant="primary"]:hover {{
    background-color: {t.PRIMARY_HOVER};
    border-color: {t.PRIMARY_HOVER};
}}

QPushButton[variant="primary"]:pressed {{
    background-color: {t.PRIMARY_ACTIVE};
    border-color: {t.PRIMARY_ACTIVE};
}}

QPushButton[variant="primary"]:disabled {{
    background-color: {t.BORDER_STRONG};
    color: {t.TEXT_INVERSE};
    border-color: {t.BORDER_STRONG};
}}

/* Danger button — delete, void */
QPushButton[variant="danger"] {{
    background-color: {t.DANGER};
    color: {t.DANGER_TEXT};
    border: 1px solid {t.DANGER};
}}

QPushButton[variant="danger"]:hover {{
    background-color: {t.DANGER_HOVER};
    border-color: {t.DANGER_HOVER};
}}

/* Ghost / link button — minimal styling */
QPushButton[variant="ghost"] {{
    background-color: transparent;
    color: {t.PRIMARY};
    border: 1px solid transparent;
}}

QPushButton[variant="ghost"]:hover {{
    background-color: {t.PRIMARY_LIGHT};
}}

/* ════════════════════════════════════════════════════════════════
   TEXT INPUTS
   ════════════════════════════════════════════════════════════════ */
QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox,
QDateEdit, QDateTimeEdit, QComboBox {{
    background-color: {t.BG_INPUT};
    color: {t.TEXT_PRIMARY};
    border: 1.5px solid {t.BORDER_STRONG};
    border-radius: {t.RADIUS_MD}px;
    padding: 6px 10px;
    min-height: {t.INPUT_HEIGHT}px;
    font-size: {t.INPUT_FONT_SIZE}px;
    font-weight: {t.FONT_WEIGHT_MEDIUM};
    selection-background-color: {t.PRIMARY_LIGHT};
    selection-color: {t.TEXT_PRIMARY};
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus,
QSpinBox:focus, QDoubleSpinBox:focus, QDateEdit:focus,
QDateTimeEdit:focus, QComboBox:focus {{
    border: 2px solid {t.BORDER_FOCUS};
    padding: 5px 9px;
}}

/* Error state — set on inputs via setProperty("state", "error") */
QLineEdit[state="error"], QTextEdit[state="error"], QPlainTextEdit[state="error"],
QSpinBox[state="error"], QDoubleSpinBox[state="error"], QComboBox[state="error"] {{
    border: 1px solid {t.DANGER};
}}

QLineEdit[state="error"]:focus, QTextEdit[state="error"]:focus,
QPlainTextEdit[state="error"]:focus, QSpinBox[state="error"]:focus,
QDoubleSpinBox[state="error"]:focus, QComboBox[state="error"]:focus {{
    border: 2px solid {t.DANGER};
    padding: 5px 9px;
}}

QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled,
QSpinBox:disabled, QDoubleSpinBox:disabled, QComboBox:disabled {{
    background-color: {t.BG_DISABLED};
    color: {t.TEXT_DISABLED};
}}

QLineEdit::placeholder {{
    color: {t.TEXT_MUTED};
}}

/* ════════════════════════════════════════════════════════════════
   COMBOBOX dropdown — restore arrow indicator using CSS
   ════════════════════════════════════════════════════════════════ */
QComboBox {{
    padding-right: 32px;  /* space for the dropdown arrow */
}}

QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 28px;
    border-left: 1px solid {t.BORDER};
    border-top-right-radius: {t.RADIUS_MD}px;
    border-bottom-right-radius: {t.RADIUS_MD}px;
    background-color: transparent;
}}

QComboBox::drop-down:hover {{
    background-color: {t.BG_HOVER};
}}

/* Triangle arrow drawn with CSS borders — no image file needed */
QComboBox::down-arrow {{
    width: 0;
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid {t.TEXT_MUTED};
    margin-right: 4px;
}}

QComboBox::down-arrow:hover {{
    border-top-color: {t.TEXT_PRIMARY};
}}

QComboBox QAbstractItemView {{
    background-color: {t.BG_CARD};
    border: 1px solid {t.BORDER_STRONG};
    border-radius: {t.RADIUS_MD}px;
    selection-background-color: {t.PRIMARY_LIGHT};
    selection-color: {t.TEXT_PRIMARY};
    padding: 4px;
}}

/* ════════════════════════════════════════════════════════════════
   CHECKBOX — properly styled box with checkmark
   ════════════════════════════════════════════════════════════════ */
QCheckBox {{
    spacing: 8px;
    background-color: transparent;
    color: {t.TEXT_SECONDARY};
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 1.5px solid {t.BORDER_STRONG};
    border-radius: 4px;
    background-color: {t.BG_CARD};
}}

QCheckBox::indicator:hover {{
    border-color: {t.PRIMARY};
}}

QCheckBox::indicator:checked {{
    background-color: {t.PRIMARY};
    border-color: {t.PRIMARY};
    image: none;
}}

QCheckBox::indicator:checked:hover {{
    background-color: {t.PRIMARY_HOVER};
    border-color: {t.PRIMARY_HOVER};
}}

/* ════════════════════════════════════════════════════════════════
   RADIO BUTTON
   ════════════════════════════════════════════════════════════════ */
QRadioButton {{
    spacing: 8px;
    background-color: transparent;
    color: {t.TEXT_SECONDARY};
}}

QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    border: 1.5px solid {t.BORDER_STRONG};
    border-radius: 9px;
    background-color: {t.BG_CARD};
}}

QRadioButton::indicator:checked {{
    background-color: {t.PRIMARY};
    border-color: {t.PRIMARY};
}}

/* ════════════════════════════════════════════════════════════════
   INPUT FRAME — used by TextField when an icon is present
   The frame provides the visible border, while the QLineEdit inside
   it is borderless. This gives us pixel-perfect icon positioning.
   ════════════════════════════════════════════════════════════════ */
QFrame#InputFrame {{
    background-color: {t.BG_INPUT};
    border: 1.5px solid {t.BORDER_STRONG};
    border-radius: {t.RADIUS_MD}px;
}}

QFrame#InputFrame:focus-within {{
    border: 2px solid {t.BORDER_FOCUS};
}}

QFrame#InputFrame[state="error"] {{
    border: 1.5px solid {t.DANGER};
}}

/* ════════════════════════════════════════════════════════════════
   TABLE
   ════════════════════════════════════════════════════════════════ */
QTableView, QTableWidget {{
    background-color: {t.BG_CARD};
    alternate-background-color: {t.BG_HOVER};
    gridline-color: {t.BORDER};
    border: 1px solid {t.BORDER};
    border-radius: {t.RADIUS_LG}px;
    selection-background-color: {t.PRIMARY_LIGHT};
    selection-color: {t.TEXT_PRIMARY};
}}

QTableView::item, QTableWidget::item {{
    padding: 8px;
    border: none;
}}

QHeaderView::section {{
    background-color: {t.BG_HOVER};
    color: {t.TEXT_SECONDARY};
    font-weight: {t.FONT_WEIGHT_SEMIBOLD};
    font-size: {t.FONT_SIZE_SM}px;
    padding: 10px 8px;
    border: none;
    border-bottom: 1px solid {t.BORDER};
    border-right: 1px solid {t.BORDER};
}}

/* ════════════════════════════════════════════════════════════════
   SCROLLBARS — slim, modern
   ════════════════════════════════════════════════════════════════ */
QScrollBar:vertical {{
    background: transparent;
    width: 10px;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background: {t.BORDER_STRONG};
    border-radius: 5px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: {t.TEXT_MUTED};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
    background: transparent;
}}

QScrollBar:horizontal {{
    background: transparent;
    height: 10px;
    margin: 0;
}}

QScrollBar::handle:horizontal {{
    background: {t.BORDER_STRONG};
    border-radius: 5px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {t.TEXT_MUTED};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
    background: transparent;
}}

/* ════════════════════════════════════════════════════════════════
   TABS
   ════════════════════════════════════════════════════════════════ */
QTabWidget::pane {{
    background-color: {t.BG_CARD};
    border: 1px solid {t.BORDER};
    border-radius: {t.RADIUS_LG}px;
    top: -1px;
}}

QTabBar::tab {{
    background-color: transparent;
    color: {t.TEXT_MUTED};
    padding: 10px 20px;
    border: none;
    font-weight: {t.FONT_WEIGHT_MEDIUM};
}}

QTabBar::tab:selected {{
    color: {t.PRIMARY};
    border-bottom: 2px solid {t.PRIMARY};
}}

QTabBar::tab:hover:!selected {{
    color: {t.TEXT_PRIMARY};
}}

/* ════════════════════════════════════════════════════════════════
   GROUPBOX — used as cards
   ════════════════════════════════════════════════════════════════ */
QGroupBox {{
    background-color: {t.BG_CARD};
    border: 1px solid {t.BORDER};
    border-radius: {t.RADIUS_LG}px;
    margin-top: 16px;
    padding: 16px;
    font-weight: {t.FONT_WEIGHT_SEMIBOLD};
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    color: {t.TEXT_SECONDARY};
}}

/* ════════════════════════════════════════════════════════════════
   MENUS
   ════════════════════════════════════════════════════════════════ */
QMenu {{
    background-color: {t.BG_CARD};
    border: 1px solid {t.BORDER};
    border-radius: {t.RADIUS_MD}px;
    padding: 4px;
}}

QMenu::item {{
    padding: 8px 16px;
    border-radius: {t.RADIUS_SM}px;
}}

QMenu::item:selected {{
    background-color: {t.PRIMARY_LIGHT};
    color: {t.TEXT_PRIMARY};
}}

QMenu::separator {{
    height: 1px;
    background: {t.BORDER};
    margin: 4px 8px;
}}

/* ════════════════════════════════════════════════════════════════
   TOOLTIPS
   ════════════════════════════════════════════════════════════════ */
QToolTip {{
    background-color: {t.TEXT_PRIMARY};
    color: {t.TEXT_INVERSE};
    border: none;
    border-radius: {t.RADIUS_SM}px;
    padding: 6px 10px;
    font-size: {t.FONT_SIZE_SM}px;
}}

/* ════════════════════════════════════════════════════════════════
   STATUS BAR
   ════════════════════════════════════════════════════════════════ */
QStatusBar {{
    background-color: {t.BG_CARD};
    border-top: 1px solid {t.BORDER};
    color: {t.TEXT_MUTED};
    font-size: {t.FONT_SIZE_SM}px;
}}

/* ════════════════════════════════════════════════════════════════
   PAGE HEADER — used by BasePage
   ════════════════════════════════════════════════════════════════ */
QFrame#PageHeader {{
    background-color: {t.BG_CARD};
    border-bottom: 1px solid {t.BORDER};
}}

/* ════════════════════════════════════════════════════════════════
   LOGIN PAGE — two-column layout over background image
   Both panels use semi-transparent backgrounds so the image shows through.
   ════════════════════════════════════════════════════════════════ */
/* Left panel uses a horizontal gradient so the right edge fades into
   the background image instead of cutting off in a hard line. */
QFrame#LoginLeftPanel {{
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0   rgba(15, 23, 42, 0.65),
        stop: 0.7 rgba(15, 23, 42, 0.50),
        stop: 1   rgba(15, 23, 42, 0.20)
    );
}}

QFrame#LoginRightPanel {{
    background-color: transparent;
}}

QFrame#LoginCard {{
    background-color: rgba(255, 255, 255, 0.97);
    border-radius: 20px;
}}

QFrame#LoginCardBorder {{
    border-radius: 22px;
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #2563EB,
        stop: 0.5 #C9A961,
        stop: 1 #2563EB
    );
}}


/* ════════════════════════════════════════════════════════════════
   DIALOG HEADER & FOOTER — used by BaseDialog
   ════════════════════════════════════════════════════════════════ */
QFrame#DialogHeader {{
    background-color: {t.BG_CARD};
    border-bottom: 1px solid {t.BORDER};
}}

QFrame#DialogFooter {{
    background-color: {t.BG_HOVER};
    border-top: 1px solid {t.BORDER};
}}

/* ════════════════════════════════════════════════════════════════
   DIALOGS — modal overlay style
   ════════════════════════════════════════════════════════════════ */
QDialog {{
    background-color: {t.BG_CARD};
}}

/* ════════════════════════════════════════════════════════════════
   PROGRESS BAR
   ════════════════════════════════════════════════════════════════ */
QProgressBar {{
    background-color: {t.BG_HOVER};
    border: none;
    border-radius: {t.RADIUS_SM}px;
    height: 8px;
    text-align: center;
}}

QProgressBar::chunk {{
    background-color: {t.PRIMARY};
    border-radius: {t.RADIUS_SM}px;
}}
"""