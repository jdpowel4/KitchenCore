from sqlalchemy.orm import Session
from decimal import Decimal

from kitchen_ledger.units.models import Unit
from kitchen_ledger.common.conversions.conversion_engine import ConversionEngine

class TestConversionEngine:

    def test_conversion_from_pounds_to_ounces(
            self, session: Session, pound: Unit, ounce: Unit):
        engine = ConversionEngine(session)
        result = engine.convert(Decimal("1"), pound, ounce, None, None)
        assert result is not None
        assert result == Decimal("16")

    def test_conversion_from_ounce_to_pound(
            self, session: Session, ounce: Unit, pound: Unit
    ):
        engine = ConversionEngine(session)
        result = engine.convert(Decimal("16"), ounce, pound, None, None)
        assert result is not None
        assert result == Decimal("1")

    