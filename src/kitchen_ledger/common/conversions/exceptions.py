from kitchen_ledger.common.exceptions import KitchenLedgerError

class ConversionError(KitchenLedgerError):
    pass

class MissingConversionError(ConversionError):
    pass

class AmbiguousConversionError(ConversionError):
    pass

class CircularConversionError(ConversionError):
    pass

class InvalidConversionError(ConversionError):
    pass