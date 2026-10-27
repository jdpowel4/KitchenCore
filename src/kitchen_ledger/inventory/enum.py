from enum import Enum

class EventType(str, Enum):
    PURCHASE = "purchase"
    RECIPE_PRODUCTION = "recipe_production"
    ADJUSTMENT = "adjustment"
    WASTE = "waste"
    COUNT = "count"
    CONSUMPTION = "consumption"