from sqlalchemy.orm import Session
from typing import Sequence

from kitchen_ledger.ingredients.models import IngredientCategory
from kitchen_ledger.ingredients.repositories.category_repo import IngredientCategoryRepo

class IngredientCategoryService:

    def __init__(self, session: Session):
        self.repo = IngredientCategoryRepo(session)

    def create(self, name: str) -> IngredientCategory:
        existing = self.repo.get(name)
        if existing is not None:
            return existing
        cat = self.repo.create(name)
        return cat

    def get_all(self) -> Sequence[IngredientCategory]:
        return self.repo.get_all()