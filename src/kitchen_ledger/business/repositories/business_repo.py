from sqlalchemy.orm import Session

from kitchen_ledger.business.models import Business

class BusinessRepo:

    def __init__(self, session: Session):
        self.session = session

    def get(self) -> Business | None:
        return self.session.get(Business, 1)

    def create(self, business: Business) -> Business:
        if business.id is None:
            business.id = 1
        self.session.add(business)
        self.session.flush()
        return business