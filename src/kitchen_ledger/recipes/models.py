from sqlalchemy import Boolean, ForeignKey, String, Numeric, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kitchen_ledger.units.models import Unit
    from kitchen_ledger.items.models import Item

from kitchen_ledger.common.models import Base, TimestampMixin

class Recipe(Base, TimestampMixin):

    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("recipe_categories.id"))
    yield_qty: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    yield_unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"))
    serving_qty: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    serving_unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    locked: Mapped[bool] = mapped_column(Boolean, default=False)
    costing_method: Mapped[str] = mapped_column(String, default="most_recent_cost")

    item: Mapped["Item"] = relationship(back_populates="recipe")
    category: Mapped["RecipeCategory"] = relationship(back_populates="recipes")
    yield_unit: Mapped["Unit"] = relationship(foreign_keys=[yield_unit_id])
    serving_unit: Mapped["Unit"] = relationship(foreign_keys=[serving_unit_id])
    components: Mapped[list["RecipeComponent"]] = relationship(back_populates="recipe", cascade="all, delete-orphan", uselist=True)

    def __repr__(self) -> str:
        return f"<Recipe(name='{self.item.name}')>"

class RecipeCategory(Base):

    __tablename__ = "recipe_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    recipes: Mapped[list["Recipe"]] = relationship(back_populates="category", cascade="all, delete-orphan", uselist=True)

class RecipeComponent(Base):

    __tablename__ = "recipe_components"

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"))
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"))
    pre_instructions: Mapped[str | None] = mapped_column(Text, nullable=True)
    post_instructions: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int | None] = mapped_column(nullable=True)

    recipe: Mapped["Recipe"] = relationship(back_populates="components")
    item: Mapped["Item"] = relationship()
    unit: Mapped["Unit"] = relationship()

    def __repr__(self) -> str:
        return f"<RecipeComponent(name='{self.item.name}')>"

class RecipeProduction(Base, TimestampMixin):

    __tablename__ = "recipe_productions"

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"))
    quantity_produced: Mapped[Decimal] = mapped_column(Numeric(18, 6))

    recipe: Mapped["Recipe"] = relationship()