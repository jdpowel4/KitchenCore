from sqlalchemy.orm import Session
from decimal import Decimal

from kitchen_ledger.ingredients.models import Ingredient, IngredientCategory, IngredientSubcategory
from kitchen_ledger.units.models import Unit, UnitCategory
from kitchen_ledger.vendors.models import Vendor, VendorItem 
from kitchen_ledger.items.enums import ItemType
from kitchen_ledger.items.models import Item

class UnitCategoryFactory:

    @staticmethod
    def create(session: Session, *, name: str) -> UnitCategory:
        category = UnitCategory(name=name)
        session.add(category)
        session.flush()
        return category

class UnitFactory:
    """Create Unit objects for tests."""

    @staticmethod
    def create(
            session: Session, *, name: str = "Test Unit", abbreviation: str =    "test", category: UnitCategory, factor: Decimal, allow: bool = True) -> Unit:

        unit = Unit(name=name, abbreviation=abbreviation, category=category, factor=factor, allow_global_conversions=allow)
        session.add(unit)
        session.flush()
        return unit
    
class ItemFactory:

    @staticmethod
    def create(
            session: Session, *, name: str, type: ItemType) -> Item:
        item = Item(name=name, item_type=type)
        session.add(item)
        session.flush()
        return item

class IngredientFactory:

    @staticmethod
    def create_ingredient(
            session: Session, *, name: str, category: IngredientCategory, subcategory: IngredientSubcategory, base_unit: Unit, usable_factor: Decimal = Decimal("1"))-> Ingredient:
        item = ItemFactory.create(session, name=name, type=ItemType.INGREDIENT)
        ingredient = Ingredient(item=item, category=category, subcategory=subcategory, base_unit=base_unit, usable_factor=usable_factor)
        session.add(ingredient)
        session.flush()
        return ingredient

    @staticmethod
    def create_ingredient_category(
            session: Session, *, name: str = "Test Category") -> IngredientCategory:
        category = IngredientCategory(name=name)
        session.add(category)
        session.flush()
        return category

    @staticmethod
    def create_ingredient_subcategory(
            session: Session, *, name: str = "Test Subcategory", category: IngredientCategory) -> IngredientSubcategory:
        subcategory = IngredientSubcategory(name=name, category=category)
        session.add(subcategory)
        session.flush()
        return subcategory