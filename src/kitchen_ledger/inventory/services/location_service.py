from sqlalchemy.orm import Session
from typing import Sequence

from kitchen_ledger.inventory.models import InventoryLocation
from kitchen_ledger.inventory.repositories.location_repo import InventoryLocationRepo

class InventoryLocationService:

    def __init__(self, session: Session):

        self.repo = InventoryLocationRepo(session)

    def get_all(self) -> Sequence[InventoryLocation]:
        return self.repo.get_all()
    