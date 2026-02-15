from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, 
                               QPushButton, QLabel, QMessageBox, QFrame)
from config.settings import cfg

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        lbl_head = QLabel("Eczane Ayarları")
        lbl_head.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(lbl_head)
        
        # Form Container
        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: white; border-radius: 5px; padding: 10px;")
        form_layout = QFormLayout(form_frame)
        
        self.inp_pharmacy = QLineEdit()
        self.inp_phone = QLineEdit()
        self.inp_pharmacist = QLineEdit()
        
        form_layout.addRow("Eczane Adı:", self.inp_pharmacy)
        form_layout.addRow("Telefon:", self.inp_phone)
        form_layout.addRow("Eczacı Adı:", self.inp_pharmacist)
        
        layout.addWidget(form_frame)
        
        # Save Button
        btn_save = QPushButton("Ayarları Kaydet")
        btn_save.setStyleSheet("""
            QPushButton { background-color: #28a745; color: white; border: none; padding: 10px; border-radius: 4px; font-weight: bold; }
            QPushButton:hover { background-color: #218838; }
        """)
        btn_save.clicked.connect(self.save_settings)
        layout.addWidget(btn_save)
        
        layout.addStretch()

    def load_settings(self):
        self.inp_pharmacy.setText(cfg.get("pharmacy_name"))
        self.inp_phone.setText(cfg.get("pharmacy_phone"))
        self.inp_pharmacist.setText(cfg.get("pharmacist_name") or "")

    def save_settings(self):
        cfg.set("pharmacy_name", self.inp_pharmacy.text())
        cfg.set("pharmacy_phone", self.inp_phone.text())
        cfg.set("pharmacist_name", self.inp_pharmacist.text())
        
        QMessageBox.information(self, "Başarılı", "Ayarlar kaydedildi.")
