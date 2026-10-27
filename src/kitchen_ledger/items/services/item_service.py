from sqlalchemy.orm import Session
from typing import Sequence

from kitchen_ledger.items.models import Item
from kitchen_ledger.items.repositories.item_repo import ItemRepo
from kitchen_ledger.items.exceptions import UnknownItemError
from kitchen_ledger.items.enums import ItemType

class ItemService:

    def __init__(self, session: Session):
        self.repo = ItemRepo(session)

    def get(self, id: int | str) -> Item:
        item = self.repo.get(id)
        if item is None:
            raise UnknownItemError("No Item Found")
        return item

    def create(self, name: str, item_type: ItemType) -> Item:
        existing = self.repo.get(name)
        if existing is not None:
            return existing
        item = Item(name=name, item_type=item_type)
        return self.repo.create(item)

    def get_all(self) -> Sequence[Item]:
        return self.repo.get_all()