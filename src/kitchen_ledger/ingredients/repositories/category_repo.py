from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Sequence

from kitchen_ledger.ingredients.models import IngredientCategory

class IngredientCategoryRepo:

    def __init__(self, session: Session):
        self.session = session

    def get(self, id: int | str) -> IngredientCategory | None:
        if isinstance(id, int):
            return self.session.get(IngredientCategory, id)
        if isinstance(id, str):
            cat = select(IngredientCategory).where(IngredientCategory.name == id)
            return self.session.scalar(cat)

    def create(self, name: str) -> IngredientCategory:
        cat = IngredientCategory(name=name)
        self.session.add(cat)
        self.session.flush()
        return cat

    def get_all(self) -> Sequence[IngredientCategory]:
        stmt = select(IngredientCategory).order_by(IngredientCategory.name)
        return list(self.session.scalars(stmt))
    