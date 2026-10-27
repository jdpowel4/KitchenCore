from enum import Enum

class ItemType(str, Enum):
    INGREDIENT = "ingredient"
    RECIPE = "recipe"
    MENU_ITEM = "menu_item"