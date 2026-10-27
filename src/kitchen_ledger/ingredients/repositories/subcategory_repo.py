from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Sequence

from kitchen_ledger.ingredients.models import IngredientSubcategory

class IngredientSubcategoryRepo:

    def __init__(self, session: Session):
        self.session = session

    def get(self, id: int | str) -> IngredientSubcategory | None:
        if isinstance(id, int):
            return self.session.get(IngredientSubcategory, id)
        if isinstance(id, str):
            sub = select(IngredientSubcategory).where(IngredientSubcategory.name == id)
            return self.session.scalar(sub)

    def create(self, subcategory: IngredientSubcategory) -> IngredientSubcategory:
        self.session.add(subcategory)
        self.session.flush()
        return subcategory

    def get_all(self) -> Sequence[IngredientSubcategory]:
        stmt = select(IngredientSubcategory).order_by(IngredientSubcategory.category_id, IngredientSubcategory.name)
        return list(self.session.scalars(stmt))