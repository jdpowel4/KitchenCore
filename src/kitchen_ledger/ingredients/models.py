from sqlalchemy import String, ForeignKey, Numeric, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kitchen_ledger.units.models import Unit
    from kitchen_ledger.items.models import Item
    from kitchen_ledger.inventory.models import InventoryLocation, InventoryLot
    from kitchen_ledger.vendors.models import VendorItem

from kitchen_ledger.common.models import Base, TimestampMixin

class Ingredient(Base, TimestampMixin):

    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), unique=True, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("ingredient_categories.id"))
    subcategory_id: Mapped[int] = mapped_column(ForeignKey("ingredient_subcategories.id"))
    location_id: Mapped[int | None] = mapped_column(ForeignKey("inventory_locations.id"), nullable=True)
    base_unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"))
    usable_factor: Mapped[Decimal] = mapped_column(Numeric(21,20), default=1.00)

    __table_args__ = (
        CheckConstraint(
            "usable_factor > 0 AND usable_factor <= 1",
            name = "ck_ingredient_usable_factor_range"
        ),
    )

    item: Mapped["Item"] = relationship(back_populates="ingredient")
    category: Mapped["IngredientCategory"] = relationship(back_populates="ingredients")
    subcategory: Mapped["IngredientSubcategory"] = relationship(back_populates="ingredients")
    location: Mapped["InventoryLocation"] = relationship(back_populates="ingredients")
    base_unit: Mapped["Unit"] = relationship()
    vendor_items: Mapped[list["VendorItem"]] = relationship(back_populates="ingredient", uselist=True)
    lots: Mapped[list["InventoryLot"]] = relationship(back_populates="ingredient", uselist=True)

    def __repr__(self):
        return f"<Ingredient(name='{self.item.name}')>"
    def __str__(self):
        return self.item.name

class IngredientCategory(Base):

    __tablename__ = "ingredient_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    sort_order: Mapped[int | None] = mapped_column(nullable=True)

    subcategory: Mapped[list["IngredientSubcategory"]] = relationship(back_populates="category", cascade="all, delete-orphan", uselist=True)
    ingredients: Mapped[list["Ingredient"]] = relationship(back_populates="category", uselist=True)

    def __repr__(self):
        return f"<IngredientCategory(name='{self.name}')>"
    def __str__(self):
        return self.name

class IngredientSubcategory(Base):

    __tablename__ = "ingredient_subcategories"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("ingredient_categories.id"), nullable=False)
    sort_order: Mapped[int | None] = mapped_column(nullable=True)

    category: Mapped["IngredientCategory"] = relationship(back_populates="subcategory")
    ingredients: Mapped[list["Ingredient"]] = relationship(back_populates="subcategory", uselist=True)

    def __repr__(self):
        return f"<IngredientSubcategory(name='{self.name}')>"
    def __str__(self):
        return self.name

