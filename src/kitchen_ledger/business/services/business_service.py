from sqlalchemy.orm import Session

from kitchen_ledger.business.exceptions import BusinessError
from kitchen_ledger.business.models import Business
from kitchen_ledger.business.dto import BusinessInfo, BusinessSetupData
from kitchen_ledger.business.repositories.business_repo import BusinessRepo

class BusinessService:

    def __init__(self, session: Session):
        self.repo = BusinessRepo(session)

    

    @staticmethod
    def _to_info(business: Business) -> BusinessInfo:
        address_parts = [
            business.address1,
            business.address2,
            f"{business.city}, {business.state} {business.zip_code}",
            business.country
        ]
        return BusinessInfo(name=business.dba_name, logo_path=business.logo_path, address=", ".join(part.strip() for part in address_parts if part and part.strip()), phone=business.phone, email=business.email)

    def get_business_if_configured(self) -> BusinessInfo | None:
        business = self.repo.get()
        if business is None:
            return None
        return self._to_info(business)
    
    def get_business(self) -> BusinessInfo:
        business = self.get_business_if_configured()
        if business is None:
            raise BusinessError("No business has been configured.")
        return business

    def create_business(self, data: BusinessSetupData) -> BusinessInfo:
        if self.repo.get() is not None:
            raise BusinessError("A business has already been configured.")

        business = Business(
            id=1,
            legal_name=data.legal_name.strip(),
            dba_name=data.dba_name.strip(),
            phone=data.phone.strip(),
            email=data.email.strip(),
            website=data.website,
            address1=data.address1.strip(),
            address2=data.address2,
            city=data.city.strip(),
            state=data.state.strip(),
            zip_code=data.zip_code.strip(),
            country=data.country.strip(),
            logo_path=data.logo_path,
            sales_tax_rate=data.sales_tax_rate
        )
        self.repo.create(business)
        return self._to_info(business)