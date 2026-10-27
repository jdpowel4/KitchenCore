from sqlalchemy.orm import Session

from kitchen_ledger.business.models import Business
from kitchen_ledger.business.services.business_service import BusinessService
from kitchen_ledger.business.dto import BusinessInfo

class BusinessProvider:

    def __init__(self, service: BusinessService):
        self._business: BusinessInfo | None = None
        self.service = service

    def load(self) -> None:
        self._business = self.service.get_business()

    @property
    def business(self) -> BusinessInfo:
        if self._business is None:
            raise RuntimeError("Business has not been loaded")
        return self._business

    def refresh(self) -> None:
        self._business = self.service.get_business()
