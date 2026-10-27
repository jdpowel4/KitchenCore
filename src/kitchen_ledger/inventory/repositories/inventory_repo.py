from sqlalchemy.orm import Session

from kitchen_ledger.inventory.models import InventoryEvent, InventoryLot, InventoryTransaction
class InventoryRepo:

    def __init__(
            self,
            session: Session,
    ):
        
        self.session = session

    def create_event(
            self,
            event: InventoryEvent
    ) -> InventoryEvent:
        self.session.add(event)
        return event

    def create_lot(
            self,
            lot: InventoryLot
    ) -> InventoryLot:
        self.session.add(lot)
        return lot

    def create_transaction(
            self,
            transaction: InventoryTransaction
    ) -> InventoryTransaction:
        self.session.add(transaction)
        return transaction
    
    def get_latest_cost_lot(
            self,
            ingredient_id: int
    ) -> InventoryLot | None:
        return self.session.query(InventoryLot).filter(InventoryLot.ingredient_id == ingredient_id).order_by(InventoryLot.created_at.desc()).first()
    