import os
from pathlib import Path
from dotenv import load_dotenv

KITCHENCORE_ROOT = Path(__file__).resolve().parents[3]

load_dotenv(KITCHENCORE_ROOT / ".env", override=True)

INSTANCE_DIR = KITCHENCORE_ROOT / "instance"

DATABASE_PATH = INSTANCE_DIR / "kitchen_core.db"

IMPORTS_DIR = INSTANCE_DIR / "imports"
ASSET_DIR = IMPORTS_DIR / "assets"
INVOICE_DIR = IMPORTS_DIR / "invoices"

EXPORT_DIR = INSTANCE_DIR / "exports"
BACKUP_DIR = INSTANCE_DIR / "backups"
LOG_DIR = INSTANCE_DIR / "logs"

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATABASE_PATH.as_posix()}")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

DEBUG = os.getenv("DEBUG", "false").lower() == "true"