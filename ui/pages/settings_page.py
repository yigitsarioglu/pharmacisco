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
        self.inp_address = QLineEdit()
        
        form_layout.addRow("Eczane Adı:", self.inp_pharmacy)
        form_layout.addRow("Telefon:", self.inp_phone)
        form_layout.addRow("Eczacı Adı:", self.inp_pharmacist)
        form_layout.addRow("Adres:", self.inp_address)
        
        layout.addWidget(form_frame)
        
        # Save Button
        btn_save = QPushButton("Ayarları Kaydet")
        btn_save.setStyleSheet("""
            QPushButton { background-color: #28a745; color: white; border: none; padding: 10px; border-radius: 4px; font-weight: bold; }
            QPushButton:hover { background-color: #218838; }
        """)
        btn_save.clicked.connect(self.save_settings)
        layout.addWidget(btn_save)
        
        layout.addSpacing(20)
        
        # --- License Info Container ---
        lbl_license = QLabel("Lisans Bilgileri")
        lbl_license.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 5px;")
        layout.addWidget(lbl_license)
        
        lic_frame = QFrame()
        lic_frame.setStyleSheet("background-color: #E8F4F8; border-radius: 5px; padding: 10px; border: 1px solid #BCE8F1;")
        lic_layout = QFormLayout(lic_frame)
        
        from licence.license_manager import check_license_status
        status = check_license_status()
        
        self.lbl_lic_cust = QLabel(status.get("customer_name", "Yok"))
        self.lbl_lic_key = QLabel(status.get("license_key", "Yok"))
        self.lbl_lic_exp = QLabel(status.get("expiry_date", "Yok"))
        
        # Style the labels
        for lbl in [self.lbl_lic_cust, self.lbl_lic_key, self.lbl_lic_exp]:
            lbl.setStyleSheet("font-weight: bold; color: #31708F;")
            
        lic_layout.addRow("Müşteri/Eczane:", self.lbl_lic_cust)
        lic_layout.addRow("Lisans Anahtarı:", self.lbl_lic_key)
        lic_layout.addRow("Bitiş Tarihi:", self.lbl_lic_exp)
        
        layout.addWidget(lic_frame)
        
        layout.addStretch()

    def load_settings(self):
        self.inp_pharmacy.setText(cfg.get("pharmacy_name"))
        self.inp_phone.setText(cfg.get("pharmacy_phone"))
        self.inp_pharmacist.setText(cfg.get("pharmacist_name") or "")
        self.inp_address.setText(cfg.get("pharmacy_address") or "")

    def save_settings(self):
        cfg.set("pharmacy_name", self.inp_pharmacy.text())
        cfg.set("pharmacy_phone", self.inp_phone.text())
        cfg.set("pharmacist_name", self.inp_pharmacist.text())
        cfg.set("pharmacy_address", self.inp_address.text())
        
        QMessageBox.information(self, "Başarılı", "Ayarlar kaydedildi.")
