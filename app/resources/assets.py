"""Asset helpers — locate files inside app/resources/ reliably.

Use these functions instead of hardcoding paths anywhere in the app.
This way, when we eventually package the app with PyInstaller, we have
one place to adjust path resolution.
"""
from pathlib import Path

# The resources/ folder itself
RESOURCES_DIR = Path(__file__).resolve().parent

IMAGES_DIR = RESOURCES_DIR / "images"
ICONS_DIR  = RESOURCES_DIR / "icons"
FONTS_DIR  = RESOURCES_DIR / "fonts"
STYLES_DIR = RESOURCES_DIR / "styles"


def image_path(filename: str) -> str:
    """Return the absolute path to an image file in resources/images/."""
    return str(IMAGES_DIR / filename)


def icon_path(filename: str) -> str:
    """Return the absolute path to an icon file in resources/icons/."""
    return str(ICONS_DIR / filename)


# ── Common assets used in multiple places ────────────────────────────
# .ico is for the title bar / taskbar (Windows uses small embedded sizes)
# .png is for in-app display where we need a crisp large image
LOGO_ICO = "mostek_logo.ico"
LOGO_PNG = "mostek_logo.png"


def app_icon_path() -> str:
    """Return the path to the .ico file used as the OS-level app icon."""
    return image_path(LOGO_ICO)


def logo_path() -> str:
    """Return the path to the high-resolution PNG logo for in-app display."""
    return image_path(LOGO_PNG)
# Login screen background
LOGIN_BACKGROUND = "login_background.jpg"


def login_background_path() -> str:
    """Return the path to the login screen background image."""
    return image_path(LOGIN_BACKGROUND)