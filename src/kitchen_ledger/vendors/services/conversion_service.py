from sqlalchemy.orm import Session
from typing import Sequence
from decimal import Decimal

from kitchen_ledger.vendors.models import VendorItem, VendorItemConversion
from kitchen_ledger.vendors.repositories.conversion_repo import VendorItemConversionRepo
from kitchen_ledger.vendors.enum import ConversionSource
from kitchen_ledger.units.models import Unit

class VendorItemConversionService:

    def __init__(self, session: Session):
        self.repo = VendorItemConversionRepo(session)

    def get_by_item(self, item: VendorItem) -> Sequence[VendorItemConversion]:
        return self.repo.get_by_item(item)