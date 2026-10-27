from sqlalchemy import String, Boolean, ForeignKey, Numeric, Enum, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kitchen_ledger.purchases.models import Purchase
    from kitchen_ledger.units.models import Unit
    from kitchen_ledger.ingredients.models import Ingredient

from kitchen_ledger.common.models import Base, TimestampMixin
from kitchen_ledger.vendors.enum import ConversionSource

class Vendor(Base):

    __tablename__ = "vendors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    account_number: Mapped[int] = mapped_column(nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    notes: Mapped[str] = mapped_column(String, nullable=True)

    purchases: Mapped[list["Purchase"]] = relationship(back_populates="vendor", uselist=True)
    vendor_items: Mapped[list["VendorItem"]] = relationship(back_populates="vendor", uselist=True)
    contacts: Mapped[list["VendorContact"]] = relationship(back_populates="vendor", uselist=True)

    def __repr__(self) -> str:
        return f"<Vendor(name='{self.name}')>"
    def __str__(self) -> str:
        return self.name

class VendorContact(Base):

    __tablename__ = "vendor_contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    vendor_id: Mapped[int] = mapped_column(ForeignKey("vendors.id"))
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    vendor: Mapped["Vendor"] = relationship(back_populates="contacts")

class VendorItem(Base, TimestampMixin):

    __tablename__ = "vendor_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    vendor_id: Mapped[int] = mapped_column(ForeignKey("vendors.id"))
    ingredient_id: Mapped[int | None] = mapped_column(ForeignKey("ingredients.id"), nullable=True)
    vendor_sku: Mapped[str] = mapped_column(String)
    vendor_description: Mapped[str] = mapped_column(String)
    pack_size: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    pack_unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"))
    most_recent_price: Mapped[Decimal] = mapped_column(Numeric(15,10), nullable=False)
    
    ingredient: Mapped["Ingredient"] = relationship(back_populates="vendor_items")
    pack_unit: Mapped["Unit"] = relationship()
    vendor: Mapped["Vendor"] = relationship(back_populates="vendor_items")
    conversions: Mapped[list["VendorItemConversion"]] = relationship(back_populates="vendor_item")

    def __repr__(self) -> str:
        return f"<VendorItem(name='{self.vendor_description}')>"

class VendorItemConversion(Base):

    __tablename__ = "vendor_item_conversions"

    id: Mapped[int] = mapped_column(primary_key=True)
    vendor_item_id: Mapped[int] = mapped_column(ForeignKey("vendor_items.id"))
    from_unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"))
    to_unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"))
    multiplier: Mapped[Decimal] = mapped_column(Numeric(18, 6), nullable=False)
    source: Mapped[ConversionSource] = mapped_column(Enum(ConversionSource, native_enum=False), nullable=False)
    notes: Mapped[str] = mapped_column(String, nullable=True)

    vendor_item: Mapped["VendorItem"] = relationship(back_populates="conversions")
    from_unit: Mapped["Unit"] = relationship(foreign_keys=[from_unit_id])
    to_unit: Mapped["Unit"] = relationship(foreign_keys=[to_unit_id])

    def __repr__(self) -> str:
        return f"<VendorItemConversion(item='{self.vendor_item.vendor_description}': {self.from_unit.name} -> {self.to_unit.name} multiplier:{self.multiplier})"