from sqlalchemy.orm import Session
from typing import Sequence

from kitchen_ledger.ingredients.models import IngredientCategory, IngredientSubcategory
from kitchen_ledger.ingredients.repositories.subcategory_repo import IngredientSubcategoryRepo
from kitchen_ledger.ingredients.repositories.category_repo import IngredientCategoryRepo

class IngredientSubcategoryService:

    def __init__(self, session: Session):
        self.repo = IngredientSubcategoryRepo(session)
        self.category_repo = IngredientCategoryRepo(session)

    def create(self, name: str, category: str | IngredientCategory) -> IngredientSubcategory:
        existing = self.repo.get(name)
        if existing is not None:
            return existing

        if isinstance(category, str):
            cat = self.category_repo.get(category)
            if cat is None:
                raise
            category = cat

        sub = IngredientSubcategory(name=name, category=category)
        return self.repo.create(sub)

    def get_all(self) -> Sequence[IngredientSubcategory]:
        return self.repo.get_all()