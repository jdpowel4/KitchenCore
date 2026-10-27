from PySide6.QtWidgets import QMainWindow, QMdiArea

from kitchen_ledger.app.context import AppContext
from kitchen_ledger.gui.windows.window_manager import WindowManager

class MainWindow(QMainWindow):

    def __init__(self, context: AppContext):
        super().__init__()

        business = context.business
        if business is None:
            raise RuntimeError("Cannot open MainWindow before business setup.")
                
        self.context = context
        self._business = business
        self._build_menus()
        self._build_toolbar()
        self._build_ui()
        self._connect_signals()

    def _build_menus(self):
        menu_bar = self.menuBar()
        app_menu = menu_bar.addMenu("App")
        # First Submenu
        app_new_menu = app_menu.addMenu("New")
        self.new_inventory = app_new_menu.addAction("Item")
        self.new_purchase = app_new_menu.addAction("Purchase")
        self.new_recipe = app_new_menu.addAction("Recipe")
        app_new_menu.addSeparator()
        self.new_vendor = app_new_menu.addAction("Vendor")
        self.new_unit = app_new_menu.addAction("Unit")
        # Second submenu
        app_open = app_menu.addMenu("Open")
        self.open_inventory = app_open.addAction("Items")
        self.open_purchases = app_open.addAction("Purchases")
        self.open_recipes = app_open.addAction("Recipes")
    
    def _build_toolbar(self):
        """
        Build the applications main toolbar.
        """
        pass

    def _build_ui(self):
        self.setWindowTitle(self._business.name)
        self.resize(1400,900)           
        self.mdi_area = QMdiArea()
        self.setCentralWidget(self.mdi_area)
        self.window_manager = WindowManager(mdi_area=self.mdi_area, context=self.context)

    def _connect_signals(self):
        self.new_recipe.triggered.connect(self.window_manager.open_new_recipe)
        self.open_inventory.triggered.connect(self.window_manager.open_ingredients)
        self.new_purchase.triggered.connect(self.window_manager.open_new_purchase)
        self.open_purchases.triggered.connect(self.window_manager.open_purchases)
        self.open_recipes.triggered.connect(self.window_manager.open_recipes)