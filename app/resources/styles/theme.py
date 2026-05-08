"""Theme system: fonts, stylesheet, and design tokens.

Call apply_theme(app) once at startup, after creating QApplication.
"""
from pathlib import Path
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtWidgets import QApplication

from app.resources.styles.stylesheet import build_stylesheet
from app.resources.styles import tokens as t

# Folder containing the .ttf files we bundled
FONTS_DIR = Path(__file__).resolve().parent.parent / "fonts"

FONT_FILES = [
    "Inter-Regular.ttf",
    "Inter-Medium.ttf",
    "Inter-SemiBold.ttf",
    "Inter-Bold.ttf",
]


def _load_fonts() -> bool:
    """Register every bundled font file with Qt's font database."""
    loaded_any = False
    for filename in FONT_FILES:
        path = FONTS_DIR / filename
        if not path.exists():
            print(f"[Theme] WARNING: font file missing: {path}")
            continue

        font_id = QFontDatabase.addApplicationFont(str(path))
        if font_id == -1:
            print(f"[Theme] WARNING: failed to load font: {filename}")
        else:
            loaded_any = True

    return loaded_any


def apply_theme(app: QApplication) -> None:
    """Apply the app-wide theme: fonts + global stylesheet."""
    # 1. Load fonts
    fonts_ok = _load_fonts()
    family = t.FONT_FAMILY if fonts_ok else "Segoe UI"
    app.setFont(QFont(family, t.FONT_SIZE_BASE))

    if fonts_ok:
        print(f"[Theme] Inter loaded. Base size: {t.FONT_SIZE_BASE}px")
    else:
        print(f"[Theme] Inter NOT loaded. Falling back to Segoe UI.")

    # 2. Apply global stylesheet
    app.setStyleSheet(build_stylesheet())
    print("[Theme] Stylesheet applied.")