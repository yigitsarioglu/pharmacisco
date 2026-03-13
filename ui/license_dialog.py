from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                               QPushButton, QMessageBox, QHBoxLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from licence.license_manager import activate_license

class LicenseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pharmacisco Lisans Aktivasyonu")
        self.setFixedSize(400, 250)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        lbl_title = QLabel("Pharmacisco'ya Hoş Geldiniz")
        font = QFont("Arial", 14, QFont.Bold)
        lbl_title.setFont(font)
        lbl_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_title)
        
        lbl_desc = QLabel("Programı kullanabilmek için lütfen \nlisans bilgilerinizi giriniz.")
        lbl_desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_desc)
        
        layout.addSpacing(10)
        
        # Customer Name
        h_customer = QHBoxLayout()
        lbl_customer = QLabel("Müşteri/Eczane Adı:")
        lbl_customer.setFixedWidth(120)
        self.inp_customer = QLineEdit()
        self.inp_customer.setPlaceholderText("Örn: Eczane Yıldız")
        h_customer.addWidget(lbl_customer)
        h_customer.addWidget(self.inp_customer)
        layout.addLayout(h_customer)
        
        # License Key
        h_key = QHBoxLayout()
        lbl_key = QLabel("Lisans Anahtarı:")
        lbl_key.setFixedWidth(120)
        self.inp_key = QLineEdit()
        self.inp_key.setPlaceholderText("Örn: ECZ-XYZ12345")
        h_key.addWidget(lbl_key)
        h_key.addWidget(self.inp_key)
        layout.addLayout(h_key)
        
        layout.addSpacing(10)
        
        # Activate Button
        self.btn_activate = QPushButton("Aktivasyon Yap ve Başla")
        self.btn_activate.setFixedHeight(40)
        self.btn_activate.setStyleSheet("background-color: #28a745; color: white; font-weight: bold; border-radius: 5px;")
        self.btn_activate.clicked.connect(self.on_activate)
        layout.addWidget(self.btn_activate)
        
    def on_activate(self):
        customer = self.inp_customer.text().strip()
        key = self.inp_key.text().strip()
        
        if not customer or not key:
            QMessageBox.warning(self, "Hata", "Lütfen Eczane Adı ve Lisans Anahtarını boş bırakmayın.")
            return
            
        self.btn_activate.setEnabled(False)
        self.btn_activate.setText("Doğrulanıyor, Lütfen Bekleyin...")
        # Force UI update
        self.repaint()
        
        success, message = activate_license(key, customer)
        
        if success:
            QMessageBox.information(self, "Başarılı", message)
            self.accept()
        else:
            QMessageBox.critical(self, "Hata", message)
            self.btn_activate.setEnabled(True)
            self.btn_activate.setText("Aktivasyon Yap ve Başla")
