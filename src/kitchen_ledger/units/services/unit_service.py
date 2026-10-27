from sqlalchemy import select
from sqlalchemy.orm import Session
from decimal import Decimal
from typing import Sequence

from kitchen_ledger.infrastructure.logging import get_logger, log_operation, LogLevels
from kitchen_ledger.units.exceptions import UnitError, UnknownUnitError
from kitchen_ledger.units.repositories.unit_repo import UnitRepo
from kitchen_ledger.units.models import Unit, UnitCategory

logger = get_logger(__name__)

class UnitService:

    def __init__(self, session: Session):
        self.unit_repo = UnitRepo(session)

    def get_all(self) -> Sequence[Unit]:
        return self.unit_repo.get_all()

    def get_by_name(self, name: str) -> Unit:
        unit = self.unit_repo.get_by_name(name)
        if unit is None:
            raise UnknownUnitError(name)
        return unit

    def get_by_abbv(self, abbv: str) -> Unit:
        unit = self.unit_repo.get_by_abbv(abbv)
        if unit is None:
            raise UnknownUnitError(abbv)
        return unit

    def get_by_name_or_abbv(self, value: str) -> Unit:
        unit = self.unit_repo.get_by_name_or_abbv(value)
        if unit is None:
            raise UnknownUnitError(value)
        return unit

    def get(self, id: int) -> Unit:
        unit = self.unit_repo.get(id)
        if unit is None:
            raise UnknownUnitError(id)
        return unit

    def create(self, name: str, category: UnitCategory, factor: Decimal, allow: bool, abbv: str | None = None) -> Unit:
        existing = self.unit_repo.get_by_name(name)
        if existing is not None:
            return existing
        unit = Unit(
            name=name,
            abbreviation=abbv,
            category=category,
            factor=factor,
            allow_global_conversions=bool(allow))
        return self.unit_repo.create(unit)