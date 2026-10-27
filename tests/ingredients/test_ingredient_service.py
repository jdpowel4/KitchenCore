from sqlalchemy.orm import Session

from kitchen_ledger.ingredients.models import Ingredient, IngredientSubcategory, IngredientCategory
from kitchen_ledger.ingredients.services.ingredient_service import IngredientService
from kitchen_ledger.units.models import Unit

def test_create_ingredient_returns_ingredient(session: Session, food_category: IngredientCategory, condiment_subcategory: IngredientSubcategory, fluid_ounce: Unit):
    service = IngredientService(session)
    result = service.create("Mayo", food_category, condiment_subcategory, fluid_ounce)

    assert result in session
    assert result.id is not None
