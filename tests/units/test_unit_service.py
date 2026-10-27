from sqlalchemy.orm import Session
from decimal import Decimal

from kitchen_ledger.units.models import Unit, UnitCategory
from kitchen_ledger.units.services.unit_service import UnitService
from tests.factories import UnitFactory

class TestUnitService:

    def test_get_all_returns_list_of_units(self, session: Session, pound: Unit, ounce: Unit):
        service = UnitService(session)
        result = service.get_all()

        assert result is not None
        assert len(result) == 2
        assert set(result) == {pound, ounce}

    def test_get_by_name_returns_unit(self, session: Session, pound: Unit, weight_category: UnitCategory):
        service = UnitService(session)
        result = service.get_by_name("Pound")
        assert result is not None
        assert result.id == pound.id
        assert result.name == "Pound"
        assert result.category_id == weight_category.id