from dataclasses import dataclass

@dataclass(frozen=True)
class BusinessInfo:
    name: str
    logo_path: str | None
    address: str
    phone: str
    email: str

@dataclass(frozen=True)
class BusinessSetupData:
    legal_name: str
    dba_name: str
    phone: str
    email: str
    website: str | None
    address1: str
    address2: str | None
    city: str
    state: str
    zip_code: str
    country: str
    logo_path: str | None = None
    sales_tax_rate: str | None = None