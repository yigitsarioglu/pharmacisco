import sys
import os

# Create missing packages if needed
for d in ['utils', 'printer', 'input', 'drug_matcher', 'ocr']:
    if not os.path.exists(d):
        os.makedirs(d)
        with open(os.path.join(d, '__init__.py'), 'w') as f:
            pass

from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
