from PySide6.QtWidgets import (
    QMdiArea,
    QMdiSubWindow,
    QWidget
)

from kitchen_ledger.app.context import AppContext
from kitchen_ledger.ingredients.gui.ingredient_list import IngredientPage
from kitchen_ledger.recipes.gui.recipe_list import RecipePage
from kitchen_ledger.recipes.gui.recipe_editor import RecipeEditor
from kitchen_ledger.purchases.gui.purchases_list import PurchasePage
from kitchen_ledger.purchases.gui.purchase_editor import NewPurchaseDialog, PurchaseEditor

class WindowManager:
    """
    Manages Windows displayed inside the app's QMdiArea
    """

    def __init__(
        self,
        mdi_area: QMdiArea,
        context: AppContext
    ):
        self.mdi_area = mdi_area
        self.context = context

    def open(
        self,
        widget: QWidget,
        title: str
    ) -> QMdiSubWindow:
        subwindow = self.mdi_area.addSubWindow(widget)
        subwindow.setWindowTitle(title)
        subwindow.show()
        return subwindow

    def open_ingredients(self):
        self.open(IngredientPage(self.context), "Ingredients")

    def open_recipes(self):
        self.open(RecipePage(self.context), "Recipes")

    def open_new_recipe(self):
        self.open(RecipeEditor(self.context), "New Recipe")

    def open_purchases(self):
        self.open(PurchasePage(self.context), "Purchases")

    def open_new_purchase(self):
        dialog = NewPurchaseDialog(self.context)
        #dialog.new_vendor.connect(self.open_new_vendor)
        dialog.purchase_created.connect(self.open_purchase_editor)
        dialog.exec()

    def open_purchase_editor(self, purchase_id: int):
        self.open(PurchaseEditor(self.context, purchase_id), "New Purchase")