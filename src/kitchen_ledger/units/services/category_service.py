from sqlalchemy.orm import Session

from kitchen_ledger.units.models import *
from kitchen_ledger.units.repositories.category_repo import UnitCategoryRepo

class UnitCategoryService:

    def __init__(self, session: Session):
        self.category_repo = UnitCategoryRepo(session)

    def get_or_create(self, name: str) -> UnitCategory:
        category = self.category_repo.get_by_name(name)
        if category is not None:
            return category
        category = UnitCategory(name=name)
        return self.category_repo.create(category)
    