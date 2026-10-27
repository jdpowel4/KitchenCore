from kitchen_ledger.common.exceptions import KitchenLedgerError

class ItemError(KitchenLedgerError):
    pass

class UnknownItemError(ItemError):
    pass