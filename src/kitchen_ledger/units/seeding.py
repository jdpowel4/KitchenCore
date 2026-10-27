from sqlalchemy.orm import Session
from decimal import Decimal

from kitchen_ledger.units.models import UnitCategory, Unit
from kitchen_ledger.units.services.unit_service import UnitService
from kitchen_ledger.units.services.category_service import UnitCategoryService
from kitchen_ledger.infrastructure.logging import get_logger, setup_logging

logger = get_logger(__name__)

UNIT_SEED_DATA = (
    ("Ounce", "oz", "Weight", "1"),
    ("Pound", "lb", "Weight", "16"),
    ("Gram", "g", "Weight", "0.0352739619"),
    ("Kilogram", "kg", "Weight", "35.2739619"),

    ("Teaspoon", "tsp", "Volume", "0.1666666667"),
    ("Tablespoon", "tbsp", "Volume", "0.5"),
    ("Fluid Ounce", "floz", "Volume", "1"),
    ("Cup", "cup", "Volume", "8"),
    ("Pint", "pt", "Volume", "16"),
    ("Quart", "qt", "Volume", "32"),
    ("Gallon", "gal", "Volume", "128"),
    ("Milliliter", "ml", "Volume", "0.0338140227"),
    ("Liter", "l", "Volume", "33.8140227"),

    ("Each", "ea", "Count", "1"),
    ("Dozen", "dz", "Count", "12")
)

def seed_units(session: Session):
    category_service = UnitCategoryService(session)
    unit_service = UnitService(session)

    categories: dict[str, UnitCategory] = {}

    for category_name in ("Weight", "Volume", "Count"):
        logger.debug(f"Seeding Unit Category '{category_name}'")
        categories[category_name] = category_service.get_or_create(category_name)

    for name, abbreviation, category_name, factor in UNIT_SEED_DATA:
        logger.debug(f"Seeding Unit '{name}'")
        unit_service.create(name=name, abbv=abbreviation, category=categories[category_name], factor=Decimal(factor), allow=True)

    session.commit()