import sys
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                               QListWidget, QStackedWidget, QLabel, QPushButton, QFrame, QSizePolicy, QMessageBox)
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PySide6.QtCore import Qt, QSize, QRectF, QTimer

from licence.license_manager import check_license_status

from ui.pages.manual_page import ManualPage
from ui.pages.ocr_page import OCRPage
from ui.pages.settings_page import SettingsPage
from ui.pages.drug_manager_page import DrugManagerPage
from ui.pages.drug_manager_page_en import DrugManagerPageEN
from ui.pages.browser_page import BrowserPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pharmacisco - Profesyonel Eczane Asistanı")
        self.resize(1200, 800)
        
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        
        # Main Layout (HBox: Sidebar | Content)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- SIDEBAR ---
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("background-color: #2C3E50; color: white;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        
        # 1. Logo Area
        logo_area = QFrame()
        logo_area.setFixedHeight(150)
        logo_area.setStyleSheet("background-color: #1A252F;")
        logo_layout = QVBoxLayout(logo_area)
        
        # Load Custom Logo
        lbl_logo = QLabel()
        lbl_logo.setAlignment(Qt.AlignCenter)
        
        logo_pix = QPixmap("icons/pharmacisco.png")
        if not logo_pix.isNull():
            lbl_logo.setPixmap(logo_pix.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            lbl_logo.setText("LOGO")
            lbl_logo.setStyleSheet("color: white; font-weight: bold; font-size: 24px;")
        
        lbl_app = QLabel("PHARMACISCO")
        lbl_app.setAlignment(Qt.AlignCenter)
        lbl_app.setStyleSheet("font-weight: bold; font-size: 16px; margin-top: 10px;")
        
        logo_layout.addWidget(lbl_logo)
        logo_layout.addWidget(lbl_app)
        sidebar_layout.addWidget(logo_area)
        
        # 2. Navigation Buttons
        self.btn_manual = self.create_nav_btn("Manuel Etiket")
        self.btn_manager = self.create_nav_btn("İlaç Yönetimi (TR)")
        self.btn_manager_en = self.create_nav_btn("İlaç Yönetimi (EN)")
        self.btn_browser = self.create_nav_btn("Otomatik Browser")
        self.btn_ocr = self.create_nav_btn("Otomatik (OCR)")
        self.btn_settings = self.create_nav_btn("Ayarlar")
        
        sidebar_layout.addWidget(self.btn_manual)
        sidebar_layout.addWidget(self.btn_manager)
        sidebar_layout.addWidget(self.btn_manager_en)
        sidebar_layout.addWidget(self.btn_browser)
        sidebar_layout.addWidget(self.btn_ocr)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.btn_settings)
        
        # --- CONTENT AREA ---
        self.stack = QStackedWidget()
        self.page_manual = ManualPage()
        self.page_manager = DrugManagerPage()
        self.page_manager_en = DrugManagerPageEN()
        self.page_browser = BrowserPage()
        self.page_ocr = OCRPage()
        self.page_settings = SettingsPage()
        
        self.stack.addWidget(self.page_manual)      # 0
        self.stack.addWidget(self.page_manager)     # 1
        self.stack.addWidget(self.page_manager_en)  # 2
        self.stack.addWidget(self.page_browser)     # 3
        self.stack.addWidget(self.page_ocr)         # 4
        self.stack.addWidget(self.page_settings)    # 5
        
        # Connections
        self.btn_manual.clicked.connect(lambda: self.switch_page(0))
        self.btn_manager.clicked.connect(lambda: self.switch_page(1))
        self.btn_manager_en.clicked.connect(lambda: self.switch_page(2))
        self.btn_browser.clicked.connect(lambda: self.switch_page(3))
        self.btn_ocr.clicked.connect(lambda: self.switch_page(4))
        self.btn_settings.clicked.connect(lambda: self.switch_page(5))
        
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack)

        # Start at Manual
        self.switch_page(0)
        
        # --- BACKGROUND LICENSE MONITORING ---
        self.license_timer = QTimer(self)
        self.license_timer.timeout.connect(self.monitor_license)
        # Check every 5 minutes (5 * 60 * 1000 ms)
        self.license_timer.start(300000)

    def monitor_license(self):
        """Runs every 5 minutes in the background to ensure license is still valid."""
        status = check_license_status()
        if not status.get("valid"):
            self.license_timer.stop()
            QMessageBox.critical(self, "Lisans İhlali", 
                "Lisansınızın süresi dolmuş veya geçerliliğini yitirmiş.\n"
                "Program güvenlik nedeniyle kapatılacaktır."
            )
            self.close()

    def create_nav_btn(self, text):
        btn = QPushButton(text)
        btn.setFixedHeight(50)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #BDC3C7;
                border: none;
                text-align: left;
                padding-left: 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #34495E;
                color: white;
            }
            QPushButton:checked {
                background-color: #2980B9;
                color: white;
                border-left: 5px solid #E74C3C;
            }
        """)
        btn.setCheckable(True)
        btn.setAutoExclusive(True)
        return btn

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)
        # Handle button styling
        btns = [self.btn_manual, self.btn_manager, self.btn_manager_en, self.btn_browser, self.btn_ocr, self.btn_settings]
        for i, btn in enumerate(btns):
            btn.setChecked(i == index)


