from sqlalchemy import select
from sqlalchemy.orm import Session

from kitchen_ledger.items.models import Item, ItemUnitConversion
from kitchen_ledger.units.models import Unit

class ItemConversionRepo:

    def __init__(self, session: Session):
        self.session = session

    def get_conversions(self, item: Item) -> list[ItemUnitConversion]:
        stmt = select(ItemUnitConversion).where(ItemUnitConversion.item_id == item.id)
        return list(self.session.scalars(stmt))
    