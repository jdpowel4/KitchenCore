from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from kitchen_ledger.infrastructure.database import SessionLocal, engine
from kitchen_ledger.business.services.business_service import BusinessService
from kitchen_ledger.business.dto import BusinessInfo
from kitchen_ledger.units.services.unit_service import UnitService

class AppContext:

    def __init__(self, database_engine: Engine = engine, session_factory: sessionmaker[Session] = SessionLocal):
        
        self.engine = database_engine
        self.session_factory = session_factory
        self.business: BusinessInfo | None = None

        self.reload_business()

    @property
    def is_configured(self) -> bool:
        return self.business is not None

    def reload_business(self):
        with self.session_factory() as session:
            service = BusinessService(session)
            self.business = service.get_business_if_configured()

    def load_unit_service(self, session: Session) -> UnitService:
        return UnitService(session)
    