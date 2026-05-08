"""
MosTek ElectroPOS — Project scaffolder
Run once from the project root to create the full folder structure.
Safe to re-run: it will not overwrite existing files.
"""
from pathlib import Path

# Project root = folder where this script lives
ROOT = Path(__file__).resolve().parent

# ──────────────────────────────────────────────────────────────
# Folders to create (relative to project root)
# ──────────────────────────────────────────────────────────────
FOLDERS = [
    "app",
    "app/database",
    "app/database/migrations",
    "app/models",
    "app/repositories",
    "app/services",
    "app/ui",
    "app/ui/widgets",
    "app/ui/pages",
    "app/ui/dialogs",
    "app/utils",
    "app/resources",
    "app/resources/icons",
    "app/resources/images",
    "app/resources/styles",
    "data",
    "backups",
    "tests",
    "logs",
]

# Folders that need an __init__.py (Python packages)
PACKAGES = [
    "app",
    "app/database",
    "app/models",
    "app/repositories",
    "app/services",
    "app/ui",
    "app/ui/widgets",
    "app/ui/pages",
    "app/ui/dialogs",
    "app/utils",
    "tests",
]

# Top-level files with starter content
FILES = {
    ".gitignore": """# Python
__pycache__/
*.pyc
*.pyo
.venv/
venv/
*.egg-info/

# IDE
.idea/
.vscode/

# App data
data/*.db
data/*.db-journal
backups/
logs/
*.log

# Build artifacts
build/
dist/
*.spec

# OS
.DS_Store
Thumbs.db
""",
    "requirements.txt": "PySide6>=6.6.0\n",
    "README.md": "# MosTek ElectroPOS\n\nPoint of Sale system for electronics and repair shops.\n\n"
                 "Built with PySide6 + SQLite.\n",
    "main.py": '''"""MosTek ElectroPOS — application entry point."""
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtCore import Qt


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("MosTek ElectroPOS")

    window = QMainWindow()
    window.setWindowTitle("MosTek ElectroPOS")
    window.resize(1024, 700)

    label = QLabel("ElectroPOS — coming soon")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    window.setCentralWidget(label)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
''',
    "app/config.py": '''"""App-wide constants and paths."""
from pathlib import Path

APP_NAME = "MosTek ElectroPOS"
APP_VERSION = "0.1.0"
COMPANY_NAME = "MosTek Solutions"

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
BACKUP_DIR = BASE_DIR / "backups"
LOGS_DIR = BASE_DIR / "logs"
RESOURCES_DIR = BASE_DIR / "app" / "resources"

DB_PATH = DATA_DIR / "electropos.db"
''',
}


def create_folders():
    print("Creating folders...")
    for folder in FOLDERS:
        path = ROOT / folder
        path.mkdir(parents=True, exist_ok=True)
        print(f"  [OK] {folder}/")


def create_init_files():
    print("\nCreating __init__.py files...")
    for pkg in PACKAGES:
        init_file = ROOT / pkg / "__init__.py"
        if not init_file.exists():
            init_file.touch()
            print(f"  [OK] {pkg}/__init__.py")
        else:
            print(f"  [skip] {pkg}/__init__.py (already exists)")


def create_files():
    print("\nCreating starter files...")
    for relpath, content in FILES.items():
        path = ROOT / relpath
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            print(f"  [OK] {relpath}")
        else:
            print(f"  [skip] {relpath} (already exists)")


def create_gitkeeps():
    """Add .gitkeep to empty folders so Git tracks them."""
    print("\nAdding .gitkeep to empty folders...")
    keep_in = [
        "data", "backups", "logs",
        "app/database/migrations",
        "app/resources/icons",
        "app/resources/images",
        "app/resources/styles",
    ]
    for folder in keep_in:
        path = ROOT / folder / ".gitkeep"
        if not path.exists():
            path.touch()
            print(f"  [OK] {folder}/.gitkeep")


if __name__ == "__main__":
    print(f"Scaffolding project at: {ROOT}\n")
    create_folders()
    create_init_files()
    create_files()
    create_gitkeeps()
    print("\nDone! Project structure is ready.")
    print("\nNext steps:")
    print("  1. Run main.py to verify the blank window appears.")
    print("  2. Then we'll set up the database connection and schema.")