from sqlalchemy import select
from sqlalchemy.orm import Session

from kitchen_ledger.units.models import *

class UnitCategoryRepo:

    def __init__(self, session: Session):
        self.session = session

    def get_by_name(self, name: str) -> UnitCategory | None:
        stmt = select(UnitCategory).where(UnitCategory.name == name)
        return self.session.scalar(stmt)

    def create(self, category: UnitCategory) -> UnitCategory:
        self.session.add(category)
        self.session.flush()
        return category