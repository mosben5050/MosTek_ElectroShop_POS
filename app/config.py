"""App-wide constants and paths."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (if present)
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

APP_NAME = "MosTek ElectroPOS"
APP_VERSION = "0.1.0"
COMPANY_NAME = "MosTek Solutions"

# Paths
DATA_DIR = BASE_DIR / "data"
BACKUP_DIR = BASE_DIR / "backups"
LOGS_DIR = BASE_DIR / "logs"
RESOURCES_DIR = BASE_DIR / "app" / "resources"

DB_PATH = DATA_DIR / "electropos.db"

# Environment-driven settings (with sensible defaults)
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
