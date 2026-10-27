from sqlalchemy.orm import Session
from decimal import Decimal
from typing import Sequence

from kitchen_ledger.recipes.exceptions import DuplicateRecipeComponentError
from kitchen_ledger.recipes.repositories.component_repo import RecipeComponentRepo
from kitchen_ledger.recipes.models import Recipe, RecipeComponent
from kitchen_ledger.recipes.dto import RecipeComponentInput
from kitchen_ledger.items.models import Item
from kitchen_ledger.items.services.item_service import ItemService
from kitchen_ledger.units.models import Unit
from kitchen_ledger.units.services.unit_service import UnitService


class RecipeComponentService:

    def __init__(
            self,
            session: Session
    ):
        self.session = session
        self.component_repo = RecipeComponentRepo(session)
        self.item_service = ItemService(session)
        self.unit_service = UnitService(session)
        

    def create(
            self,
            recipe: Recipe,
            item: Item,
            quantity: Decimal,
            unit: Unit,
    ) -> RecipeComponent:

        existing = self.component_repo.get_component(recipe, item)

        if existing is not None:
            raise DuplicateRecipeComponentError(f"Recipe Component '{item.name}' already exists in Recipe '{recipe.item.name}'.")

        component = RecipeComponent(
            recipe=recipe,
            item=item,
            quantity=quantity,
            unit=unit
        )

        return self.component_repo.create(component)


    def create_by_name(
            self,
            recipe: Recipe,
            item: str,
            quantity: Decimal,
            unit: str
    ) -> RecipeComponent:
        
        # Grabbing ORM Objects from respective services.
        item_obj = self.item_service.get(item)
        unit_obj = self.unit_service.get_by_name(unit)

        return self.create(recipe, item_obj, quantity, unit_obj)

    def get_components(
            self,
            recipe: Recipe
    ) -> Sequence[RecipeComponent]:
        return self.component_repo.get_components(recipe)

    def create_from_input(
        self,
        recipe: Recipe,
        data: RecipeComponentInput
    ) -> RecipeComponent:
        item_obj = self.item_service.get(data.item_id)
        unit_obj = self.unit_service.get(data.unit_id)

        return self.create(recipe, item_obj, data.quantity, unit_obj)