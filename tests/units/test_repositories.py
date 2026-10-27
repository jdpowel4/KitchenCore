from sqlalchemy.orm import Session
from decimal import Decimal

from kitchen_ledger.units.models import Unit, UnitCategory
from kitchen_ledger.units.repositories.unit_repo import UnitRepo
from tests.factories import UnitFactory

def test_get_returns_existing_unit(session: Session, weight_category: UnitCategory, pound: Unit):
    repo = UnitRepo(session)
    result = repo.get(pound.id)
    assert result is not None
    assert result.name == pound.name
    assert result.category_id == weight_category.id

def test_get_returns_none_for_missing_unit(session):
    repo = UnitRepo(session)
    result = repo.get(99999999)
    assert result is None

def test_get_by_name_returns_existing_unit(session: Session, weight_category: UnitCategory, pound: Unit) -> None:
    repo = UnitRepo(session)
    result = repo.get_by_name("Pound")
    assert result is not None
    assert result.id == pound.id
    assert result.name == "Pound"
    assert result.category_id == weight_category.id

def test_get_by_name_returns_none_for_missing_unit(session):
    repo = UnitRepo(session)
    result = repo.get_by_name("Unit that does not exist")
    assert result is None

def test_get_by_abbv_returns_existing_unit(session: Session, weight_category: UnitCategory, pound: Unit) -> None:
    repo = UnitRepo(session)
    result = repo.get_by_abbv("lb")
    assert result is not None
    assert result.id == pound.id
    assert result.name == "Pound"
    assert result.category_id == weight_category.id

def test_get_by_abbv_returns_none_for_missing_unit(session):
    repo = UnitRepo(session)
    result = repo.get_by_abbv("Abbreviation that does not exist.")
    assert result is None

def test_get_all_returns_all_units(session: Session, weight_category: UnitCategory):
    pound = UnitFactory.create(session, name="Pound", abbreviation="lb", category=weight_category, factor=Decimal("16"))
    ounce = UnitFactory.create(session, name="Ounce", abbreviation="oz", category=weight_category, factor=Decimal("1"))
    repo = UnitRepo(session)
    result = repo.get_all()
    assert len(result) == 2
    assert set(result) == {pound, ounce}

def test_create_adds_unit(session: Session, weight_category: UnitCategory):
    unit = Unit(name="Pound", abbreviation="lb", category=weight_category, factor=Decimal("1"))
    repo = UnitRepo(session)
    result = repo.create(unit)
    assert result is unit
    assert unit in session
    assert unit.id is not None

def test_get_by_name_or_abbv_returns_existing_unit_when_giving_name(session: Session, weight_category: UnitCategory, pound: Unit):
    repo = UnitRepo(session)
    result = repo.get_by_name_or_abbv("Pound")
    assert result is not None
    assert result.id == pound.id
    assert result.abbreviation == pound.abbreviation
    assert result.category_id == weight_category.id