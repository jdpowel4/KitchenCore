from sqlalchemy.orm import Session

from kitchen_ledger.infrastructure.logging import get_logger, log_operation, LogLevels
from kitchen_ledger.vendors.models import Vendor
from kitchen_ledger.vendors.repositories.vendor_repo import VendorRepo

logger = get_logger(__name__)

class VendorService:

    def __init__(self, session: Session):

        self.vendor_repo = VendorRepo(session)

    def get_or_create(
            self,
            name: str
    ) -> Vendor:
        exists = self.vendor_repo.get_by_name(name)

        if exists is not None:
            return exists
        logger.debug(
            f"Creating '{name}' Vendor"
        )
        vendor = Vendor(name=name)
        return self.vendor_repo.create(vendor)

    def get_all(self):
        return self.vendor_repo.get_all()

    def get(self, id: int):
        return self.vendor_repo.get(id)