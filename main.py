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
    Settings page once the user is in the app.

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
    window.setMinimumSize(1280, 720)
    window.showMaximized()

    # First-run check BEFORE showing the login page
    if not run_first_run_setup_if_needed(window):
        return  # user cancelled — quit cleanly

    # Set up the login page and wire its success signal to swap to the
    # main app shell.
    login_page = LoginPage()
    login_page.login_succeeded.connect(
        lambda user: _on_login_success(window, user)
    )
    window.setCentralWidget(login_page)

    sys.exit(app.exec())


def _on_login_success(window: QMainWindow, user) -> None:
    """Build the main app shell: TopBar + Sidebar + DashboardPage."""
    from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
    from app.ui.widgets.top_bar import TopBar
    from app.ui.widgets.sidebar import Sidebar
    from app.ui.pages.dashboard_page import DashboardPage

    print(f"[App] Loading main app for {user.display_name}")

    # Outer container: top bar on top, body (sidebar + content) below
    container = QWidget()
    outer = QVBoxLayout(container)
    outer.setContentsMargins(0, 0, 0, 0)
    outer.setSpacing(0)

    # ── Top bar ──
    # ── Top bar ──
    top_bar = TopBar(user)
    top_bar.user_pill_clicked.connect(
        lambda: _show_user_menu(window, top_bar, user)
    )
    outer.addWidget(top_bar)

    # ── Body row ──
    body = QWidget()
    body_layout = QHBoxLayout(body)
    body_layout.setContentsMargins(0, 0, 0, 0)
    body_layout.setSpacing(0)

    sidebar = Sidebar(user)
    sidebar.set_active("dashboard")
    sidebar.sign_out_clicked.connect(
        lambda: _on_sign_out(window)
    )
    top_bar.toggle_sidebar_clicked.connect(sidebar.toggle_collapsed)
    body_layout.addWidget(sidebar)

    # ── Content area: a stack of pages we swap between ──
    from PySide6.QtWidgets import QStackedWidget
    pages = QStackedWidget()

    # Build pages once — only Dashboard and Settings for now,
    # other menu items will be wired up as we build them
    dashboard = DashboardPage(user)
    settings_page = _build_settings_page_if_admin(user, top_bar, sidebar)

    pages.addWidget(dashboard)  # index 0
    if settings_page is not None:
        pages.addWidget(settings_page)  # index 1

    body_layout.addWidget(pages, stretch=1)

    # Wire sidebar item clicks to swap pages
    def on_nav(key: str):
        print(f"[Nav] User clicked: {key}")
        if key == "dashboard":
            pages.setCurrentWidget(dashboard)
            top_bar.set_heading(
                f"Welcome back, {user.display_name}",
                "Here's a quick overview of your shop today.",
            )
        elif key == "settings" and settings_page is not None:
            pages.setCurrentWidget(settings_page)
            top_bar.set_heading(
                "Settings",
                "Configure your shop, taxes, receipts, and more.",
            )
        else:
            # Other menu items not built yet — for now, just print
            print(f"[Nav] '{key}' page not built yet")

    sidebar.item_selected.connect(on_nav)

    outer.addWidget(body, stretch=1)

    window.setCentralWidget(container)


def _on_sign_out(window: QMainWindow) -> None:
    """Confirm with the user, then return to the login page."""
    from app.ui.dialogs.confirm_dialog import ConfirmDialog

    confirmed = ConfirmDialog.ask(
        parent=window,
        title="Sign Out?",
        message=(
            "You'll need to sign in again to continue using the app. "
            "Make sure you've saved any pending work."
        ),
        confirm_text="Sign Out",
        cancel_text="Stay Signed In",
        is_destructive=True,
        icon="🚪",
    )

    if not confirmed:
        print("[App] Sign out cancelled")
        return

    print("[App] Signing out — returning to login")

    login_page = LoginPage()
    login_page.login_succeeded.connect(
        lambda user: _on_login_success(window, user)
    )
    window.setCentralWidget(login_page)


def _show_user_menu(window: QMainWindow, top_bar, user) -> None:
    """Pop the user dropdown menu under the user pill."""
    from app.ui.widgets.user_menu import UserMenu

    print("[UserMenu] Opening dropdown...")
    menu = UserMenu(parent=window)
    menu.action_selected.connect(
        lambda action: _handle_user_menu_action(window, action)
    )
    menu.show_below(top_bar.user_pill)


def _handle_user_menu_action(window: QMainWindow, action: str) -> None:
    """Route user menu items to the right action."""
    if action == "sign_out":
        _on_sign_out(window)
    elif action == "profile":
        print("[UserMenu] My Profile — coming soon")
    elif action == "change_password":
        print("[UserMenu] Change Password — coming soon")
    elif action == "preferences":
        print("[UserMenu] Preferences — coming soon")
    elif action == "about":
        print("[UserMenu] About — coming soon")

def _build_settings_page_if_admin(user, top_bar, sidebar):
    """Build the Settings page, but only if the user is an admin.

    Returns None for non-admins (cashiers/technicians shouldn't see it).
    """
    if not user.is_admin:
        return None

    from app.ui.pages.settings_page import SettingsPage
    page = SettingsPage(user)

    # When Shop Profile saves, the sidebar re-reads shop info from DB
    # (currently a no-op since we removed the store info block, but
    # the wiring is here for when we add it back or use it elsewhere).
    page.shop_info_updated.connect(
        lambda: _on_shop_info_changed(sidebar)
    )

    return page


def _on_shop_info_changed(sidebar) -> None:
    """Called after Shop Profile saves so UI components can refresh."""
    print("[Settings] Shop info updated — refreshing UI")
    sidebar.refresh_store_info()

if __name__ == "__main__":
    main()