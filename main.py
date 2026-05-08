"""MosTek ElectroPOS — application entry point."""
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from app.database.connection import ensure_database_exists
from app.resources.styles.theme import apply_theme
from app.resources.assets import app_icon_path
from app.ui.pages.login_page import LoginPage


def configure_high_dpi():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )


def main():
    configure_high_dpi()
    ensure_database_exists()

    app = QApplication(sys.argv)
    app.setApplicationName("MosTek ElectroPOS")

    # Set the application-wide icon — appears in title bar, taskbar, alt-tab
    app_icon = QIcon(app_icon_path())
    app.setWindowIcon(app_icon)

    apply_theme(app)

    window = QMainWindow()
    window.setWindowTitle("MosTek ElectroPOS")
    window.setWindowIcon(app_icon)  # explicit icon for the main window
    window.setMinimumSize(1024, 600)
    window.setCentralWidget(LoginPage())
    window.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()