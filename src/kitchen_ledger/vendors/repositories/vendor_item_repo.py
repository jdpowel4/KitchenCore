from sqlalchemy import select
from sqlalchemy.orm import Session

from kitchen_ledger.vendors.models import Vendor, VendorItem
from kitchen_ledger.vendors.exceptions import MissingVendorItemError

class VendorItemRepo:

        def __init__(self, session: Session):
             
             self.session = session

        def create(
                self,
                item: VendorItem
        ) -> VendorItem:
            self.session.add(item)
            return item


        def get_by_sku(
                self,
                vendor: Vendor,
                sku: str
        ) -> VendorItem:
            stmt = select(VendorItem).where(
                VendorItem.vendor_sku==sku,
                VendorItem.vendor == vendor
            )
            item = self.session.scalar(stmt)
            if item is None:
                raise MissingVendorItemError
            return item

