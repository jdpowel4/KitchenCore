from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kitchen_ledger.units.models import Unit, UnitCategory

class Base(DeclarativeBase):
    pass

class TimestampMixin:

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)