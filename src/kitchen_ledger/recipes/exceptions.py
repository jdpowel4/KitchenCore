from kitchen_ledger.common.exceptions import KitchenLedgerError

class RecipeError(KitchenLedgerError):
    pass

class UnknownRecipeError(RecipeError):
    pass

class DuplicateRecipeComponentError(RecipeError):
    pass

class DuplicateRecipeError(RecipeError):
    pass