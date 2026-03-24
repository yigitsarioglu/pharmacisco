import sys
import os
import ctypes

# Create missing packages if needed
for d in ['utils', 'printer', 'input', 'drug_matcher', 'ocr']:
    if not os.path.exists(d):
        os.makedirs(d)
        with open(os.path.join(d, '__init__.py'), 'w') as f:
            pass

from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtGui import QIcon
from PySide6.QtCore import qInstallMessageHandler
from ui.main_window import MainWindow
from ui.license_dialog import LicenseDialog
from ui.setup_dialog import SetupDialog
from licence.license_manager import check_license_status

def qt_message_handler(mode, context, message):
    if "QWin32PrintEngine" in message or "QPainter::begin" in message:
        return # Suppress printer cancellation warnings
    # Print other Qt warnings
    print(f"Qt Message: {message}")

def main():
    qInstallMessageHandler(qt_message_handler)
    app = QApplication(sys.argv)
    
    # Set Windows Taskbar Icon explicitly
    try:
        myappid = 'pharmacisco.desktop.app.1' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except:
        pass
        
    app.setWindowIcon(QIcon("icons/pharmacisco.ico"))
    
    # 1. License Check
    status = check_license_status()
    if not status.get("valid"):
        dialog = LicenseDialog()
        result = dialog.exec()
        if result != QDialog.Accepted:
            sys.exit(0)
        # License activation successful, show the Initial Profile Setup
        setup_dialog = SetupDialog()
        setup_dialog.exec()

    # 2. Main Window
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
