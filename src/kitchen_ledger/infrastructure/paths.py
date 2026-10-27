from kitchen_ledger.infrastructure.config import ASSET_DIR, BACKUP_DIR, EXPORT_DIR, IMPORTS_DIR, INSTANCE_DIR, INVOICE_DIR, LOG_DIR

def ensure_runtime_directories():
    directories = (
        INSTANCE_DIR,
        IMPORTS_DIR,
        ASSET_DIR,
        INVOICE_DIR,
        EXPORT_DIR,
        BACKUP_DIR,
        LOG_DIR
    )
    for dir in directories:
        dir.mkdir(parents=True, exist_ok=True)