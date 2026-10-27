import sqlite3
import pytest
from collections.abc import Generator
from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from decimal import Decimal

from kitchen_ledger.models import *
from kitchen_ledger.common.models import Base
from tests.factories import UnitCategoryFactory, UnitFactory, IngredientFactory

@pytest.fixture(scope="session")
def engine() -> Generator[Engine, None, None]:

    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection: sqlite3.Connection, connection_record: object) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine)

    yield engine

    Base.metadata.drop_all(engine)
    engine.dispose()

@pytest.fixture
def session(engine: Engine) -> Generator[Session, None, None]:

    with Session(engine) as session:
        try:
            yield session
        finally:
            session.rollback()

@pytest.fixture
def weight_category(session: Session) -> UnitCategory:
    return UnitCategoryFactory.create(session, name="weight")

@pytest.fixture
def volume_category(session: Session) -> UnitCategory:
    return UnitCategoryFactory.create(session, name="volume")

@pytest.fixture
def pound(session: Session, weight_category: UnitCategory) -> Unit:
    return UnitFactory.create(session, name="Pound", abbreviation="lb", category=weight_category, factor=Decimal("16"))

@pytest.fixture
def ounce(session: Session, weight_category: UnitCategory) -> Unit:
    return UnitFactory.create(session, name="Ounce", abbreviation="oz", category=weight_category, factor=Decimal("1"))

@pytest.fixture
def fluid_ounce(session: Session, volume_category: UnitCategory) -> Unit:
    return UnitFactory.create(session, name="Fluid Ounce", abbreviation="floz", category=volume_category, factor=Decimal("1"))

@pytest.fixture
def units(session: Session, weight_category: UnitCategory) -> dict[str, object]:

    volume = UnitCategoryFactory.create(session, name="volume")
    count = UnitCategoryFactory.create(session, name="count")

    ounce = UnitFactory.create(session, name="Ounce", abbreviation="oz", category=weight_category, factor=Decimal("1"))
    pound = UnitFactory.create(session, name="Pound", abbreviation="lb", category=weight_category, factor=Decimal("16"))
    gram = UnitFactory.create(session, name="Gram", abbreviation="g", category=weight_category, factor=Decimal("0.035274"))
    kilogram = UnitFactory.create(session, name="Kilogram", abbreviation="kg", category=weight_category, factor=Decimal("35.274"))

    teaspoon = UnitFactory.create(session, name="Teaspoon", abbreviation="tsp", category=volume, factor=Decimal("0.1667"))
    tablespoon = UnitFactory.create(session, name="Tablespoon", abbreviation="tbsp", category=volume, factor=Decimal("0.5"))
    fluid_ounce = UnitFactory.create(session, name="Fluid Ounce", abbreviation="floz", category=volume, factor=Decimal("1"))
    cup = UnitFactory.create(session, name="Cup", abbreviation="c", category=volume, factor=Decimal("8"))
    pint = UnitFactory.create(session, name="Pint", abbreviation="pt", category=volume, factor=Decimal("16"))
    quart = UnitFactory.create(session, name="Quart", abbreviation="qt", category=volume, factor=Decimal("64"))
    gallon = UnitFactory.create(session, name="Gallon", abbreviation="gal", category=volume, factor=Decimal("128"))
    milliliter = UnitFactory.create(session, name="Milliliter", abbreviation="ml", category=volume, factor=Decimal("0.033814"))
    liter = UnitFactory.create(session, name="Liter", abbreviation="l", category=volume, factor=Decimal("33.814"))

    each = UnitFactory.create(session, name="Each", abbreviation="ea", category=count, factor=Decimal("1"))
    dozen = UnitFactory.create(session, name="Dozen", abbreviation="dz", category=count, factor=Decimal("12"))    

    session.flush()
    return {
        "oz": ounce,
        "lb": pound,
        "g": gram,
        "kg": kilogram,
        "tsp": teaspoon,
        "tbsp": tablespoon,
        "floz": fluid_ounce,
        "c": cup,
        "p": pint,
        "qt": quart,
        "gal": gallon,
        "ml": milliliter,
        "l": liter,
        "ea": each,
        "dz": dozen
    }

@pytest.fixture
def food_category(session) -> IngredientCategory:
    return IngredientFactory.create_ingredient_category(session, name="Food")

@pytest.fixture
def condiment_subcategory(session, food_category: IngredientCategory) -> IngredientSubcategory:
    return IngredientFactory.create_ingredient_subcategory(session, name="Condiments", category=food_category)

@pytest.fixture
def mayo(session: Session, food_category: IngredientCategory, condiment_subcategory: IngredientSubcategory, fluid_ounce: Unit) -> Ingredient:
    return IngredientFactory.create_ingredient(session, name="Mayo", category=food_category, subcategory=condiment_subcategory, base_unit=fluid_ounce)
