from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                               QPushButton, QMessageBox, QHBoxLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from config.settings import cfg

class SetupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("İlk Kurulum - Eczane Bilgileri")
        self.setFixedSize(450, 350)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        lbl_title = QLabel("Eczane Profilini Oluştur")
        font = QFont("Arial", 14, QFont.Bold)
        lbl_title.setFont(font)
        lbl_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_title)
        
        lbl_desc = QLabel("Lütfen etiketlerde ve sistemde kullanılacak\neczane bilgilerinizi doldurun.")
        lbl_desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_desc)
        
        layout.addSpacing(10)
        
        # Pharmacy Name
        h_name = QHBoxLayout()
        lbl_name = QLabel("Eczane Adı:")
        lbl_name.setFixedWidth(120)
        self.inp_name = QLineEdit()
        self.inp_name.setText(cfg.get("pharmacy_name") or "")
        h_name.addWidget(lbl_name)
        h_name.addWidget(self.inp_name)
        layout.addLayout(h_name)
        
        # Phone
        h_phone = QHBoxLayout()
        lbl_phone = QLabel("Telefon:")
        lbl_phone.setFixedWidth(120)
        self.inp_phone = QLineEdit()
        self.inp_phone.setPlaceholderText("Örn: 0212 123 45 67")
        self.inp_phone.setText(cfg.get("pharmacy_phone") or "")
        h_phone.addWidget(lbl_phone)
        h_phone.addWidget(self.inp_phone)
        layout.addLayout(h_phone)
        
        # Pharmacist Name
        h_pharmacist = QHBoxLayout()
        lbl_pharmacist = QLabel("Eczacı Adı:")
        lbl_pharmacist.setFixedWidth(120)
        self.inp_pharmacist = QLineEdit()
        self.inp_pharmacist.setPlaceholderText("Ad Soyad")
        self.inp_pharmacist.setText(cfg.get("pharmacist_name") or "")
        h_pharmacist.addWidget(lbl_pharmacist)
        h_pharmacist.addWidget(self.inp_pharmacist)
        layout.addLayout(h_pharmacist)

        # Pharmacy Address
        h_address = QHBoxLayout()
        lbl_address = QLabel("Adres:")
        lbl_address.setFixedWidth(120)
        self.inp_address = QLineEdit()
        self.inp_address.setPlaceholderText("Eczane Adresi")
        self.inp_address.setText(cfg.get("pharmacy_address") or "")
        h_address.addWidget(lbl_address)
        h_address.addWidget(self.inp_address)
        layout.addLayout(h_address)
        
        layout.addSpacing(10)
        
        # Save Button
        self.btn_save = QPushButton("Bilgileri Kaydet ve Devam Et")
        self.btn_save.setFixedHeight(40)
        self.btn_save.setStyleSheet("background-color: #28a745; color: white; font-weight: bold; border-radius: 5px;")
        self.btn_save.clicked.connect(self.on_save)
        layout.addWidget(self.btn_save)
        
    def on_save(self):
        name = self.inp_name.text().strip()
        phone = self.inp_phone.text().strip()
        pharmacist = self.inp_pharmacist.text().strip()
        address = self.inp_address.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Hata", "Eczane adını boş bırakamazsınız.")
            return
            
        cfg.set("pharmacy_name", name)
        cfg.set("pharmacy_phone", phone)
        cfg.set("pharmacist_name", pharmacist)
        cfg.set("pharmacy_address", address)
        
        QMessageBox.information(self, "Başarılı", "Eczane bilgileriniz başarıyla kaydedildi!")
        self.accept()
