from sqlalchemy import String, Enum, ForeignKey, Numeric, UniqueConstraint, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kitchen_ledger.recipes.models import Recipe
    from kitchen_ledger.ingredients.models import Ingredient
    from kitchen_ledger.units.models import Unit

from kitchen_ledger.common.models import Base, TimestampMixin
from kitchen_ledger.items.enums import ItemType


class Item(Base, TimestampMixin):

    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    item_type: Mapped[ItemType] = mapped_column(Enum(ItemType, native_enum=False), nullable=False)
    sku: Mapped[int] = mapped_column(nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    ingredient: Mapped["Ingredient | None"] = relationship(back_populates="item")
    recipe: Mapped["Recipe | None"] = relationship(back_populates="item")

    def __repr__(self):
        return f"<Item(name='{self.name}')>"
    def __str__(self):
        return self.name

class ItemUnitConversion(Base):

    __tablename__ = "item_unit_conversions"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), nullable=False)
    from_unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"), nullable=False)
    to_unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"), nullable=False)
    multiplier: Mapped[Decimal] = mapped_column(Numeric(25, 20), nullable=False)

    item: Mapped["Item"] = relationship()
    from_unit: Mapped["Unit"] = relationship(foreign_keys=[from_unit_id])
    to_unit: Mapped["Unit"] = relationship(foreign_keys=[to_unit_id])

    __table_args__ = (UniqueConstraint("item_id", "from_unit_id", "to_unit_id", name="uq_item_unit_conversion"),)

    def __repr__(self):
        return (
            f"<ItemConversion: item='{self.item.name}' "
            f"{self.from_unit.name} -> {self.to_unit.name} X {self.multiplier}"
        )