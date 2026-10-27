from dataclasses import dataclass

from kitchen_ledger.ingredients.models import Ingredient


@dataclass
class MatchResult:
    name: str
    ingredient: Ingredient
    score: int