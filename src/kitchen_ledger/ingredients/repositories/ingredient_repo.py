from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Sequence

from kitchen_ledger.ingredients.models import Ingredient
from kitchen_ledger.items.models import Item

class IngredientRepo:

    def __init__(self, session: Session):
        self.session = session

    def get(self, id: int | str) -> Ingredient | None:
        if isinstance(id, int):
            return self.session.get(Ingredient, id)
        if isinstance(id, str):
            stmt = select(Ingredient).join(Ingredient.item).where(Item.name.ilike(id))
            return self.session.scalar(stmt)

    def get_all(self) -> Sequence[Ingredient]:
        stmt = select(Ingredient).join(Ingredient.item).order_by(Item.name)
        return list(self.session.scalars(stmt))

    def create(self, ingredient: Ingredient) -> Ingredient:
        self.session.add(ingredient)
        self.session.flush()
        return ingredient

    