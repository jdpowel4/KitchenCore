from sqlalchemy.orm import Session
from decimal import Decimal

from kitchen_ledger.ingredients.models import Ingredient, IngredientCategory, IngredientSubcategory
from kitchen_ledger.ingredients.services.ingredient_service import IngredientService
from kitchen_ledger.ingredients.services.category_service import IngredientCategoryService
from kitchen_ledger.ingredients.services.subcategory_service import IngredientSubcategoryService
from kitchen_ledger.units.services.unit_service import UnitService

STARTER_INGREDIENTS = (
    ("All-Purpose Flour", "Pantry", "Flour"),
    ("Granulated Sugar", "Pantry", "Sugar"),
    ("Salt", "Pantry", "Seasonings"),
    ("Butter", "Dairy", "Butter"),
    ("Chicken Breast", "Protein", "Poultry"),
)

def seed_starter_ingredients(session: Session):
    unit_service = UnitService(session)
    ingredient_service = IngredientService(session)
    category_service = IngredientCategoryService(session)
    subcategory_service = IngredientSubcategoryService(session)

    ounce = unit_service.get_by_name("Ounce")

    categories: dict[str, IngredientCategory] = {}
    subcategories: dict[tuple[str, str], IngredientSubcategory] = {}

    for _, category_name, subcategory_name in STARTER_INGREDIENTS:
        if category_name not in categories:
            category = category_service.create(category_name)
            categories[category_name] = category
        key = (category_name, subcategory_name)
        if key not in subcategories:
            subcategory = subcategory_service.create(subcategory_name, category_name)
            subcategories[key] = subcategory

    for name, category, subcategory in STARTER_INGREDIENTS:
        ingredient_service.create(name=name, category=categories[category], subcategory=subcategories[(category, subcategory)], base_unit=ounce)