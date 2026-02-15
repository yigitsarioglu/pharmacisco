from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QLineEdit, QTextEdit, QPushButton, QFormLayout, QFrame, QMessageBox)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Slot, Qt

from config.settings import cfg
from database.drug_db import db
from label.renderer import LabelRenderer
from datetime import datetime

class ManualPage(QWidget):
    def __init__(self):
        super().__init__()
        
        self.renderer = LabelRenderer()
        
        # Initial Data
        self.data = {
            "drug_name": "",
            "date": datetime.now().strftime("%d.%m.%Y"),
            "category": "",
            "short_instruction": "",
            "full_instruction": "",
            "transaction_id": "1148_NakitSatis"
        }
        
        self.init_ui()
        # We delay initial preview slightly or just call it. 
        # But we need settings loaded first.
        self.refresh_settings()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        
        # --- LEFT: INPUT ---
        left_panel = QFrame()
        left_layout = QVBoxLayout(left_panel)
        
        # Search
        search_layout = QHBoxLayout()
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("İlaç Ara (örn: Yasmin)...")
        self.txt_search.returnPressed.connect(self.do_search)
        btn_search = QPushButton("Ara")
        btn_search.clicked.connect(self.do_search)
        search_layout.addWidget(self.txt_search)
        search_layout.addWidget(btn_search)
        left_layout.addLayout(search_layout)
        
        # Form
        form = QFormLayout()
        
        self.inp_name = QLineEdit()
        self.inp_patient = QLineEdit() # Initialized inp_patient
        self.inp_date = QLineEdit(self.data["date"])
        self.inp_category = QLineEdit()
        self.inp_category.setPlaceholderText("örn: DOĞUM KONTROL İLACI")
        self.inp_short = QLineEdit()
        self.inp_short.setPlaceholderText("örn: GÜNDE 1 DEFA...")
        self.inp_full = QTextEdit()
        self.inp_full.setPlaceholderText("Detaylı açıklama...")
        self.inp_full.setMaximumHeight(100)
        
        # Signals
        for w in [self.inp_name, self.inp_date, self.inp_category, self.inp_short, self.inp_patient]:
            w.textChanged.connect(self.sync_data)
        self.inp_full.textChanged.connect(self.sync_data)
        
        form.addRow("Hasta Adı/Soyadı:", self.inp_patient)
        form.addRow("İlaç Adı:", self.inp_name)
        form.addRow("Tarih:", self.inp_date)
        form.addRow("Kategori:", self.inp_category)
        form.addRow("Kısa Talimat:", self.inp_short)
        form.addRow("Detaylı Talimat:", self.inp_full)
        
        left_layout.addLayout(form)
        left_layout.addStretch()
        
        # --- RIGHT: PREVIEW ---
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #EEE; border-radius: 8px;")
        right_layout = QVBoxLayout(right_panel)
        
        lbl_title = QLabel("CANLI ÖNİZLEME")
        lbl_title.setAlignment(Qt.AlignCenter)
        lbl_title.setStyleSheet("font-weight: bold; color: #333; font-size: 14px; margin-bottom: 10px;")
        
        self.lbl_preview = QLabel()
        self.lbl_preview.setAlignment(Qt.AlignCenter)
        self.lbl_preview.setStyleSheet("border: 2px solid #555; background-color: white;")
        
        btn_print = QPushButton("YAZDIR")
        btn_print.setMinimumHeight(45)
        btn_print.setStyleSheet("""
            QPushButton { background-color: #222; color: #FEF200; font-weight: bold; font-size: 14px; border-radius: 4px; }
            QPushButton:hover { background-color: #444; }
        """)
        btn_print.clicked.connect(self.do_print)
        
        right_layout.addWidget(lbl_title)
        right_layout.addWidget(self.lbl_preview, 1)
        right_layout.addWidget(btn_print)
        
        main_layout.addWidget(left_panel, 4)
        main_layout.addWidget(right_panel, 5)

    def do_search(self):
        q = self.txt_search.text()
        if not q: return
        
        res = db.search(q)
        if res:
            rec = res[0]
            # rec: id, barcode, name, cat, preg, short, full
            # indices: 0, 1, 2, 3, 4, 5, 6
            self.inp_name.setText(rec[2])
            self.inp_category.setText(rec[3])
            self.inp_short.setText(rec[5] if rec[5] else "")
            self.inp_full.setText(rec[6] if rec[6] else "")
        else:
            QMessageBox.information(self, "Bulunamadı", "İlaç bulunamadı.")

    def sync_data(self):
        self.data["drug_name"] = self.inp_name.text()
        self.data["patient_name"] = self.inp_patient.text()
        self.data["date"] = self.inp_date.text()
        self.data["category"] = self.inp_category.text()
        self.data["short_instruction"] = self.inp_short.text()
        self.data["full_instruction"] = self.inp_full.toPlainText()
        self.update_preview()

    def update_preview(self):
        img = self.renderer.render_image(self.data)
        pix = QPixmap.fromImage(img)
        # fit width
        w = self.lbl_preview.width() - 20
        if w > 10:
             self.lbl_preview.setPixmap(pix.scaledToWidth(w, Qt.SmoothTransformation))

    def do_print(self):
        QMessageBox.information(self, "Yazdır", "Etiket yazıcı kuyruğuna gönderildi.")

    def refresh_settings(self):
        # Called when switching to this page or init
        # Nothing specific to pull into UI fields here (pharmacy name is implicit in renderer)
        # But we force a redraw in case settings changed
        self.update_preview()
    
    def showEvent(self, event):
        self.refresh_settings()
        super().showEvent(event)
