"""MosTek ElectroPOS — application entry point."""
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from app.database.connection import ensure_database_exists
from app.resources.styles.theme import apply_theme
from app.resources.assets import app_icon_path
from app.services.auth_service import AuthService
from app.ui.pages.login_page import LoginPage
from app.ui.dialogs.first_run_dialog import FirstRunDialog


def configure_high_dpi():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )


def run_first_run_setup_if_needed(parent_window: QMainWindow) -> bool:
    """If no users exist yet, force creation of the first admin user.

    Shop configuration is NOT done at startup — that happens in the
    Settings page once the user is in the app. This keeps the startup
    flow short and frictionless.

    Returns True if the app should continue, False if the user cancelled.
    """
    auth = AuthService()
    if auth.has_any_users():
        return True

    print("[Startup] No users found — launching first-run setup")
    admin_dlg = FirstRunDialog(parent=parent_window)
    result = admin_dlg.exec()

    if result != QDialog.DialogCode.Accepted or admin_dlg.created_user is None:
        print("[Startup] First-run setup cancelled — quitting")
        return False

    print(f"[Startup] First admin created: {admin_dlg.created_user.username}")
    return True

def main():
    configure_high_dpi()
    ensure_database_exists()

    app = QApplication(sys.argv)
    app.setApplicationName("MosTek ElectroPOS")

    app_icon = QIcon(app_icon_path())
    app.setWindowIcon(app_icon)

    apply_theme(app)

    window = QMainWindow()
    window.setWindowTitle("MosTek ElectroPOS")
    window.setWindowIcon(app_icon)
    window.setMinimumSize(1024, 600)
    window.showMaximized()

    # First-run check BEFORE showing the login page
    if not run_first_run_setup_if_needed(window):
        return  # user cancelled — quit cleanly

        # Set up the login page and wire its success signal to swap to the
        # main app shell. For now we just show a placeholder.
    login_page = LoginPage()
    login_page.login_succeeded.connect(
        lambda user: _on_login_success(window, user)
    )
    window.setCentralWidget(login_page)

    sys.exit(app.exec())


def _on_login_success(window: QMainWindow, user) -> None:
    """Temporary handler — replaces the login page with a placeholder.

    Will be replaced by the real main window shell in the next step.
    """
    from PySide6.QtWidgets import QLabel
    from PySide6.QtCore import Qt as _Qt

    print(f"[App] Loading main app for {user.display_name}")
    placeholder = QLabel(
        f"✓ Login successful!\n\n"
        f"Welcome, {user.display_name}\n"
        f"Role: {user.role}\n\n"
        f"(Main window coming next…)"
    )
    placeholder.setAlignment(_Qt.AlignmentFlag.AlignCenter)
    placeholder.setStyleSheet("font-size: 18px; padding: 40px;")
    window.setCentralWidget(placeholder)


if __name__ == "__main__":
    main()