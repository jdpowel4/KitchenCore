from sqlalchemy.orm import Session
from typing import Sequence

from kitchen_ledger.ingredients.models import Ingredient, IngredientCategory, IngredientSubcategory
from kitchen_ledger.ingredients.exceptions import UnknownIngredientError
from kitchen_ledger.ingredients.repositories.category_repo import IngredientCategoryRepo
from kitchen_ledger.ingredients.repositories.subcategory_repo import IngredientSubcategoryRepo
from kitchen_ledger.ingredients.repositories.ingredient_repo import IngredientRepo
from kitchen_ledger.ingredients.dto import IngredientUpdate
from kitchen_ledger.items.services.item_service import ItemService
from kitchen_ledger.items.enums import ItemType
from kitchen_ledger.units.models import Unit
from kitchen_ledger.units.services.unit_service import UnitService


class IngredientService:

    def __init__(self, session: Session):
        self.repo = IngredientRepo(session)
        self.item_service = ItemService(session)
        self.category_repo = IngredientCategoryRepo(session)
        self.subcategory_repo = IngredientSubcategoryRepo(session)
        self.unit_service = UnitService(session)

    def get(self, id: int) -> Ingredient:
        ing = self.repo.get(id)
        if ing is None:
            raise UnknownIngredientError("No Ingredient Found")
        return ing

    def get_all(self) -> Sequence[Ingredient]:
        return self.repo.get_all()


    def create(self, name: str, category: IngredientCategory | str, subcategory: IngredientSubcategory | str, base_unit: Unit | str) -> Ingredient:
        existing = self.repo.get(name)
        if existing is not None:
            return existing

        cat = self._resolve_category(category)        
        sub = self._resolve_subcategory(subcategory)
        base = self._resolve_unit(base_unit)

        item = self.item_service.create(name=name, item_type=ItemType.INGREDIENT)

        ingredient = Ingredient(item=item, category=cat, subcategory=sub, base_unit=base)
        return self.repo.create(ingredient)
    
    def update(self, ingredient_id: int, data: IngredientUpdate):
        ingredient = self.repo.get(ingredient_id)
        if ingredient is None:
            raise UnknownIngredientError(f"Ingredient {ingredient_id} does not exist.")

        ingredient.item.name = data.name
        ingredient.category_id = data.category_id
        ingredient.subcategory_id = data.subcategory_id
        ingredient.base_unit_id = data.base_unit_id

    def _resolve_category(
            self,
            name: IngredientCategory | str
    ) -> IngredientCategory:
        if isinstance(name, IngredientCategory):
            return name
        else:
            cat = self.category_repo.get(name)
            if cat is None:
                raise
            return cat

    def _resolve_subcategory(
            self,
            name: IngredientSubcategory | str
    ) -> IngredientSubcategory:
        if isinstance(name, IngredientSubcategory):
            return name
        else:
            sub = self.subcategory_repo.get(name)
            if sub is None:
                raise
            return sub

    def _resolve_unit(
            self,
            name: Unit | str
    ) -> Unit | None:
        if isinstance(name, Unit):
            return name
        else:
            return self.unit_service.get_by_name_or_abbv(name)