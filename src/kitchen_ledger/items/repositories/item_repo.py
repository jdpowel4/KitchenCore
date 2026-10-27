from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Sequence

from kitchen_ledger.items.models import Item

class ItemRepo:

    def __init__(self, session: Session):
        self.session = session

    def get(self, id: int | str) -> Item | None:
        if isinstance(id, int):
            return self.session.get(Item, id)
        if isinstance(id, str):
            item = select(Item).where(Item.name == id)
            return self.session.scalar(item)

    def create(self, item: Item) -> Item:
        self.session.add(item)
        self.session.flush()
        return item

    def get_all(self) -> Sequence[Item]:
        stmt = select(Item).order_by(Item.name)
        return list(self.session.scalars(stmt))
    