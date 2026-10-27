from PySide6.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QFormLayout, QCheckBox, QDialogButtonBox, QMessageBox

from kitchen_ledger.app.context import AppContext
from kitchen_ledger.infrastructure.logging import get_logger
from kitchen_ledger.business.dto import BusinessSetupData
from kitchen_ledger.business.services.business_service import BusinessService
from kitchen_ledger.ingredients.seeding import seed_starter_ingredients

class InitialSetup(QDialog):

    field_definitions = (
        ("legal_name", "Legal business name", True),
        ("dba_name", "Operating name / DBA", True),
        ("phone", "Phone", True),
        ("email", "Email", True),
        ("website", "Website", False),
        ("address1", "Address", True),
        ("address2", "Address line 2", False),
        ("city", "City", True),
        ("state", "State", True),
        ("zip_code", "ZIP code", True),
        ("country", "Country", True),
        ("sales_tax_rate", "Sales tax rate", False)
    )

    def __init__(self, context: AppContext):
        super().__init__()

        self.logger = get_logger(__name__)
        self.context = context
        self.setWindowTitle("Welcome to Kitchen Ledger")
        self.setMinimumWidth(460)

        self.fields: dict[str, QLineEdit] = {}

        self._build_ui()

    def _build_ui(self):

        layout = QVBoxLayout(self)        
        form = QFormLayout()

        for key, label, required in self.field_definitions:
            field = QLineEdit()
            field.setPlaceholderText("Required" if required else "Optional")
            self.fields[key] = field
            form.addRow(f"{label}:", field)

        self.load_starter_data = QCheckBox("Load example ingredients")

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._save)
        buttons.rejected.connect(self.reject)

        layout.addLayout(form)
        layout.addWidget(self.load_starter_data)
        layout.addWidget(buttons)

    def _save(self):

        values = {
            key: field.text().strip()
            for key, field in self.fields.items()
        }

        required_fields = (
            "legal_name",
            "dba_name",
            "phone",
            "email",
            "address1",
            "city",
            "state",
            "zip_code",
            "country",
        )

        missing = [
            key for key in required_fields
            if not values[key]
        ]

        if missing:
            QMessageBox.warning(self, "Missing Information", "Please complete all required fields.")
            return

        data = BusinessSetupData(
            legal_name=values["legal_name"],
            dba_name=values["dba_name"],
            phone=values["phone"],
            email=values["email"],
            website=values["website"] or None,
            address1=values["address1"],
            address2=values["address2"] or None,
            city=values["city"],
            state=values["state"],
            zip_code=values["zip_code"],
            country=values["country"],
            sales_tax_rate=values["sales_tax_rate"] or None
        )

        try:
            with self.context.session_factory.begin() as session:
                service = BusinessService(session)
                service.create_business(data)

                if self.load_starter_data.isChecked():
                    seed_starter_ingredients(session)

        except Exception:
            
            self.logger.exception("Initial business setup failed.")

            QMessageBox.critical(self, "Setup Failed", "The initial setup could not be saved. Check the application log for details.")
            return

        self.accept()
        