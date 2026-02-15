import sys
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                               QListWidget, QStackedWidget, QLabel, QPushButton, QFrame, QSizePolicy)
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PySide6.QtCore import Qt, QSize, QRectF

from ui.pages.manual_page import ManualPage
from ui.pages.ocr_page import OCRPage
from ui.pages.settings_page import SettingsPage
from ui.pages.drug_manager_page import DrugManagerPage
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
        
        # Draw Red 'E' Logo programmatically for now
        lbl_logo = QLabel()
        lbl_logo.setAlignment(Qt.AlignCenter)
        logo_pix = self.create_logo_pixmap()
        lbl_logo.setPixmap(logo_pix)
        
        lbl_app = QLabel("PHARMACISCO")
        lbl_app.setAlignment(Qt.AlignCenter)
        lbl_app.setStyleSheet("font-weight: bold; font-size: 16px; margin-top: 10px;")
        
        logo_layout.addWidget(lbl_logo)
        logo_layout.addWidget(lbl_app)
        sidebar_layout.addWidget(logo_area)
        
        # 2. Navigation Buttons
        self.btn_manual = self.create_nav_btn("Manuel Etiket")
        self.btn_manager = self.create_nav_btn("İlaç Yönetimi")
        self.btn_browser = self.create_nav_btn("Otomatik Browser")
        self.btn_ocr = self.create_nav_btn("Otomatik (OCR)")
        self.btn_settings = self.create_nav_btn("Ayarlar")
        
        sidebar_layout.addWidget(self.btn_manual)
        sidebar_layout.addWidget(self.btn_manager)
        sidebar_layout.addWidget(self.btn_browser)
        sidebar_layout.addWidget(self.btn_ocr)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.btn_settings)
        
        # --- CONTENT AREA ---
        self.stack = QStackedWidget()
        self.page_manual = ManualPage()
        self.page_manager = DrugManagerPage()
        self.page_browser = BrowserPage()
        self.page_ocr = OCRPage()
        self.page_settings = SettingsPage()
        
        self.stack.addWidget(self.page_manual)   # 0
        self.stack.addWidget(self.page_manager)  # 1
        self.stack.addWidget(self.page_browser)  # 2
        self.stack.addWidget(self.page_ocr)      # 3
        self.stack.addWidget(self.page_settings) # 4
        
        # Connections
        self.btn_manual.clicked.connect(lambda: self.switch_page(0))
        self.btn_manager.clicked.connect(lambda: self.switch_page(1))
        self.btn_browser.clicked.connect(lambda: self.switch_page(2))
        self.btn_ocr.clicked.connect(lambda: self.switch_page(3))
        self.btn_settings.clicked.connect(lambda: self.switch_page(4))
        
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack)

        # Start at Manual
        self.switch_page(0)

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
        btns = [self.btn_manual, self.btn_manager, self.btn_browser, self.btn_ocr, self.btn_settings]
        for i, btn in enumerate(btns):
            btn.setChecked(i == index)

    def create_logo_pixmap(self):
        # Draw a Pharmacy 'E' Logo (Red E)
        size = 80
        pix = QPixmap(size, size)
        pix.fill(Qt.transparent)
        
        p = QPainter(pix)
        p.setRenderHint(QPainter.Antialiasing)
        
        # Red E styling
        font = QFont("Arial", 60, QFont.Bold)
        p.setFont(font)
        p.setPen(QColor("#E74C3C")) # Red
        p.drawText(QRectF(0, 0, size, size), Qt.AlignCenter, "E")
        p.end()
        return pix
