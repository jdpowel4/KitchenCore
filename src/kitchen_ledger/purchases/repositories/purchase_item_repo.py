from sqlalchemy import select
from sqlalchemy.orm import Session

from kitchen_ledger.purchases.models import PurchaseItem

class PurchaseItemRepo:
    
    def __init__(self, session: Session):

        self.session = session

    def create(
            self,
            purchase_item: PurchaseItem
    ) -> PurchaseItem:
        self.session.add(purchase_item)
        return purchase_item