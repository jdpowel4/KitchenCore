from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Sequence

from kitchen_ledger.inventory.models import InventoryLocation

class InventoryLocationRepo:

    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> Sequence[InventoryLocation]:
        stmt = select(InventoryLocation).order_by(InventoryLocation.name)
        return list(self.session.scalars(stmt))