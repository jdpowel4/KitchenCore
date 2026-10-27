from kitchen_ledger.common.exceptions import KitchenLedgerError

class VendorError(KitchenLedgerError):
    pass

class VendorItemError(VendorError):
    pass

class MissingVendorItemError(VendorItemError):
    pass
