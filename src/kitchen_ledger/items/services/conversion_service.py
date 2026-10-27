from sqlalchemy.orm import Session
from decimal import Decimal
from typing import Sequence

from kitchen_ledger.items.models import Item, ItemUnitConversion
from kitchen_ledger.items.repositories.conversion_repo import ItemConversionRepo
from kitchen_ledger.items.services.item_service import ItemService

class ItemConversionService:

    def __init__(self, session: Session):
        self.conversion_repo = ItemConversionRepo(session)
        self.item_service = ItemService(session)

    def get_by_item(self, item: Item) -> Sequence[ItemUnitConversion]:
        return self.conversion_repo.get_conversions(item)