from kitchen_ledger.common.exceptions import KitchenLedgerError

class PurchaseError(KitchenLedgerError):
    pass

class ImportError(PurchaseError):
    pass

class UnknownFileTypeError(ImportError):
    pass

class UnknownVendorError(ImportError):
    pass

class DuplicatePurchaseError(PurchaseError):
    pass
