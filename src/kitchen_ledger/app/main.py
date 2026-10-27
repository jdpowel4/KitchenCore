import sys
from PySide6.QtWidgets import QApplication, QMessageBox

from kitchen_ledger.app.context import AppContext
from kitchen_ledger.app.bootstrap import bootstrap_application
from kitchen_ledger.gui.windows.initial_setup_window import InitialSetup
from kitchen_ledger.gui.windows.main_window import MainWindow
from kitchen_ledger.infrastructure.logging import get_logger, setup_logging
from kitchen_ledger.infrastructure.paths import ensure_runtime_directories

def main() -> int:

    ensure_runtime_directories()
    setup_logging()

    logger = get_logger(__name__)
    logger.info("Starting Kitchen Ledger")

    app = QApplication(sys.argv)
    app.setApplicationName("KitchenLedger")
    app.setOrganizationName("KitchenCore")

    try:
        context = bootstrap_application()
    except Exception:
        logger.critical("Application initialization failed.")

        QMessageBox.critical(None, "Startup Error", "Kitchen Ledger could not initalize.\nCheck the application log for details.")
        return 1

    try:
        if not context.is_configured:
            logger.info("No business configured. Starting Onboarding.")

            setup_window = InitialSetup(context)

            if setup_window.exec() != setup_window.DialogCode.Accepted:
                logger.info("Initial setup was canceled.")
                return 0

            context.reload_business()

        if not context.is_configured:
            logger.error("Setup completed without a configured business.")
            return 1
        
        window = MainWindow(context)
        window.show()

        logger.info("Kitchen Ledger startup completed.")

        return app.exec()

    except Exception:
        logger.exception("Application startup failed.")

        QMessageBox.critical(None, "Application Error", "KitcenLedger encountered an unexpected error.\nCheck the application log for details.")
        return 1

    finally:
        context.engine.dispose()


if __name__ == "__main__":
    raise SystemExit(main())
