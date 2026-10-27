from sqlalchemy.orm import Session
from decimal import Decimal

from kitchen_ledger.common.conversions.exceptions import MissingConversionError
from kitchen_ledger.units.models import Unit
from kitchen_ledger.units.services.unit_service import UnitService
from kitchen_ledger.items.models import Item
from kitchen_ledger.vendors.models import VendorItem
from kitchen_ledger.common.conversions.graph_builder import GraphBuilder

class ConversionEngine:

    def __init__(self, session: Session):
        self.session = session
        self.unit_service = UnitService(session)

    def convert(
            self,
            quantity: Decimal,
            from_unit: Unit | int,
            to_unit: Unit | int,
            item: Item | None,
            vendor_item: VendorItem | None) -> Decimal:  
          
        if isinstance(from_unit, int):
            from_unit = self.unit_service.get(from_unit)
        if isinstance(to_unit, int):
            to_unit = self.unit_service.get(to_unit)

        graph = GraphBuilder.build(self.session, item, vendor_item)
        path = graph.find_path(from_unit, to_unit, item, vendor_item) 
        return quantity * path.multiplier
    

    
    def convert_unit_cost(
            self,
            cost: Decimal,
            from_unit: Unit,
            to_unit: Unit,
            item: Item | None,
            vendor_item: VendorItem | None) -> Decimal:
        
        graph = GraphBuilder.build(self.session, item, vendor_item,)
        path = graph.find_path(from_unit, to_unit)
        return cost / path.multiplier