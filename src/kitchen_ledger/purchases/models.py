from sqlalchemy import ForeignKey, Date, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kitchen_ledger.vendors.models import Vendor, VendorItem
    from kitchen_ledger.inventory.models import InventoryLot
    from kitchen_ledger.units.models import Unit

from kitchen_ledger.common.models import Base, TimestampMixin

class Purchase(Base, TimestampMixin):

    __tablename__ = "purchases"

    id: Mapped[int] = mapped_column(primary_key=True)
    vendor_id: Mapped[int] = mapped_column(ForeignKey("vendors.id"))
    invoice_number: Mapped[str] = mapped_column(String, nullable=False)
    invoice_date: Mapped[date] = mapped_column(Date)
    tax: Mapped[Decimal] = mapped_column(Numeric(10,2))
    fuel_charge: Mapped[Decimal] = mapped_column(Numeric(10,2))
    total: Mapped[Decimal] = mapped_column(Numeric(10,2))

    __table_args__ = (UniqueConstraint("vendor_id", "invoice_number", name="uq_invoice_number"),)

    vendor: Mapped["Vendor"] = relationship(back_populates="purchases")
    items: Mapped[list["PurchaseItem"]] = relationship(back_populates="purchase", cascade="all, delete-orphan", uselist=True)

    def __repr__(self) -> str:
        return f"<Purchase(date={self.invoice_date}, inv number={self.invoice_number})>"

class PurchaseItem(Base, TimestampMixin):

    __tablename__ = "purchase_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    purchase_id: Mapped[int] = mapped_column(ForeignKey("purchases.id"))
    vendor_item_id: Mapped[int] = mapped_column(ForeignKey("vendor_items.id"))
    purchase_unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"))
    quantity: Mapped[Decimal] = mapped_column(Numeric(18,6), nullable=False)
    case_cost: Mapped[Decimal] = mapped_column(Numeric(12,2), nullable=False)
    extended_cost: Mapped[Decimal] = mapped_column(Numeric(18,8), nullable=False)


    purchase: Mapped["Purchase"] = relationship(back_populates="items")
    vendor_item: Mapped["VendorItem"] = relationship()
    unit: Mapped["Unit"] = relationship()
    lots: Mapped["InventoryLot"] = relationship(back_populates="purchase_item")