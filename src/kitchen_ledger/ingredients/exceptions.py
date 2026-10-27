from kitchen_ledger.common.exceptions import KitchenLedgerError

class IngredientError(KitchenLedgerError):
    pass

class UnknownIngredientError(IngredientError):
    pass

class NoCostDataError(IngredientError):
    pass