from alembic import command
from alembic.config import Config

from kitchen_ledger.app.context import AppContext
from kitchen_ledger.infrastructure.config import KITCHENCORE_ROOT
from kitchen_ledger.units.seeding import seed_units
from kitchen_ledger.infrastructure.logging import get_logger

logger = get_logger(__name__)

def apply_database_migrations():
    try:
        logger.debug("Applying Database Migrations")
        alembic_config = Config(str(KITCHENCORE_ROOT / "alembic.ini"))
        alembic_config.attributes["configure_logger"] = False
        command.upgrade(alembic_config, "head")
        logger.debug("Database migrations completed.")
    except Exception:
        logger.exception("Database migration failed.")

def seed_reference_data():
    logger.info("Seeding reference data.")
    context = AppContext()
    with context.session_factory() as session:
        seed_units(session)

def bootstrap_application() -> AppContext:
    apply_database_migrations()
    seed_reference_data()
    return AppContext()