from kitchen_ledger.common.exceptions import KitchenLedgerError

class UnitError(KitchenLedgerError):
    pass

class UnknownUnitError(UnitError):
    pass