from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                               QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFrame,
                               QGroupBox, QRadioButton)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Slot, QTimer
from utils.integration_server import IntegrationServer
from database.drug_db import db
from label.renderer import LabelRenderer
from printer.driver import PrinterManager
from config.settings import cfg
from datetime import datetime

class BrowserPage(QWidget):
    def __init__(self):
        super().__init__()
        self.server = IntegrationServer(port=5500)
        self.server.request_received.connect(self.on_data_received)
        self.renderer = LabelRenderer()
        self.init_ui()
        
        # Auto-start server safely
        self.toggle_server()

    def init_ui(self):
        # MAIN LAYOUT: Split Left (List) and Right (Preview)
        main_layout = QHBoxLayout(self)
        
        # --- LEFT PANEL (Table + Controls) ---
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Top Bar: Status & Control
        top_bar = QFrame()
        top_bar.setStyleSheet("background-color: #EEE; border-radius: 5px; padding: 5px;")
        hbox = QHBoxLayout(top_bar)
        
        self.lbl_status = QLabel("Sunucu Durumu: KAPALI")
        self.lbl_status.setStyleSheet("font-weight: bold; color: gray;")
        
        self.btn_toggle = QPushButton("Sunucuyu Başlat")
        self.btn_toggle.clicked.connect(self.toggle_server)
        
        hbox.addWidget(self.lbl_status)
        hbox.addStretch()
        hbox.addWidget(self.btn_toggle)
        
        left_layout.addWidget(top_bar)
        
        # Instruction Source Selection
        source_group = QGroupBox("Etikete Yazılacak Talimat Kaynağı")
        source_group.setStyleSheet("font-weight: bold; color: #333;")
        source_layout = QHBoxLayout(source_group)
        
        self.radio_doctor = QRadioButton("Doktor Talimatı (Medula)")
        self.radio_db_short = QRadioButton("Veritabanı: Kısa Talimat")
        self.radio_db_full = QRadioButton("Veritabanı: Uzun Talimat")
        
        # Load saved preference
        pref = cfg.get("instruction_source")
        if pref == "db_short":
            self.radio_db_short.setChecked(True)
        elif pref == "db_full":
            self.radio_db_full.setChecked(True)
        else:
            self.radio_doctor.setChecked(True)
            
        self.radio_doctor.toggled.connect(self.on_source_changed)
        self.radio_db_short.toggled.connect(self.on_source_changed)
        self.radio_db_full.toggled.connect(self.on_source_changed)
        
        source_layout.addWidget(self.radio_doctor)
        source_layout.addWidget(self.radio_db_short)
        source_layout.addWidget(self.radio_db_full)
        source_layout.addStretch()
        
        left_layout.addWidget(source_group)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Hasta Adı", "İlaç Adı", "Barkod", "Durum", "Doktor Talimatı", "Talimat (DB Bulunan)"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch) # Drug Name
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch) # Doctor Instruction
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch) # Instruction DB
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.ExtendedSelection)
        self.table.itemSelectionChanged.connect(self.update_preview)
        
        left_layout.addWidget(self.table)
        
        # Bottom Controls
        bottom_layout = QHBoxLayout()
        
        btn_print_all = QPushButton("Listeyi Yazdır (Etiket Bas)")
        btn_print_all.setMinimumHeight(40)
        btn_print_all.setStyleSheet("background-color: #222; color: #FEF200; font-weight: bold;")
        btn_print_all.clicked.connect(self.print_all)
        
        btn_delete = QPushButton("Seçilenleri Sil")
        btn_delete.setMinimumHeight(40)
        btn_delete.setStyleSheet("background-color: #dc3545; color: white; font-weight: bold;")
        btn_delete.clicked.connect(self.delete_selected)
        
        btn_clear = QPushButton("Listeyi Temizle")
        btn_clear.setMinimumHeight(40)
        btn_clear.setStyleSheet("background-color: #6c757d; color: white; font-weight: bold;")
        btn_clear.clicked.connect(self.clear_table)
        
        bottom_layout.addWidget(btn_clear)
        bottom_layout.addWidget(btn_delete)
        bottom_layout.addWidget(btn_print_all, 1)
        
        left_layout.addLayout(bottom_layout)
        
        # Info
        lbl_info = QLabel("Extension bu adrese POST atmalı: http://localhost:5500/print\nJSON Format: {'patient_name': '...', 'drugs': [{'name': '...', 'barcode': '...'}]}")
        lbl_info.setStyleSheet("color: #666; font-size: 11px;")
        left_layout.addWidget(lbl_info)
        
        # --- RIGHT PANEL (Preview) ---
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #EEE; border-radius: 8px;")
        right_panel.setFixedWidth(400) # Fixed width for preview panel
        right_layout = QVBoxLayout(right_panel)
        
        lbl_title = QLabel("CANLI ÖNİZLEME")
        lbl_title.setAlignment(Qt.AlignCenter)
        lbl_title.setStyleSheet("font-weight: bold; color: #333; font-size: 14px; margin-bottom: 10px;")
        
        self.lbl_preview = QLabel()
        self.lbl_preview.setAlignment(Qt.AlignCenter)
        self.lbl_preview.setStyleSheet("border: 2px solid #555; background-color: white;")
        
        right_layout.addWidget(lbl_title)
        right_layout.addWidget(self.lbl_preview, 1)
        right_layout.addStretch()
        
        # Add panels to main
        main_layout.addWidget(left_panel, 7)
        main_layout.addWidget(right_panel, 3)

    def on_source_changed(self):
        if self.radio_doctor.isChecked():
            cfg.set("instruction_source", "doctor")
        elif self.radio_db_short.isChecked():
            cfg.set("instruction_source", "db_short")
        elif self.radio_db_full.isChecked():
            cfg.set("instruction_source", "db_full")
        self.update_preview()

    def toggle_server(self):
        if self.server.running:
            self.server.stop_server()
            self.lbl_status.setText("Sunucu Durumu: KAPALI")
            self.lbl_status.setStyleSheet("font-weight: bold; color: red;")
            self.btn_toggle.setText("Sunucuyu Başlat")
        else:
            success = self.server.start_server()
            if success:
                self.lbl_status.setText("Sunucu Durumu: AÇIK (Port: 5500)")
                self.lbl_status.setStyleSheet("font-weight: bold; color: green;")
                self.btn_toggle.setText("Durdur")
            else:
                QMessageBox.critical(self, "Hata", "Sunucu başlatılamadı (Port meşgul olabilir).")

    @Slot(dict)
    def on_data_received(self, data):
        # This runs on main thread due to Signal/Slot
        patient = data.get("patient_name", "Bilinmeyen Hasta")
        drugs = data.get("drugs", [])
        
        for d in drugs:
            name = d.get("name", "")
            barcode = d.get("barcode", "")
            usage = d.get("usage", "")  # Medula'dan gelen doz/periyot bilgisi
            
            # Lookup in DB
            status = "❌ Bulunamadı"
            instruction = ""
            
            # Match Logic: Barcode or Name
            rec = None
            if barcode:
                rec = db.get_drug_by_barcode(barcode) # Returns row or None
            
            if not rec and name:
                # Search by name
                res = db.search(name)
                if res and len(res) > 0:
                    rec = res[0]
            
            if rec:
                # rec: (id, barcode, name, cat, preg, short, full)
                status = "✅ Eşleşti"
                instruction = rec[5] if rec[5] else ""
            
            self.add_row(patient, name, barcode, status, usage, instruction)
            
    def add_row(self, patient, drug, barcode, status, usage, instruction):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(patient))
        self.table.setItem(row, 1, QTableWidgetItem(drug))
        self.table.setItem(row, 2, QTableWidgetItem(str(barcode)))
        self.table.setItem(row, 3, QTableWidgetItem(status))
        self.table.setItem(row, 4, QTableWidgetItem(usage))
        self.table.setItem(row, 5, QTableWidgetItem(instruction))
        
        # Color status
        if "✅" in status:
            self.table.item(row, 3).setForeground(Qt.darkGreen)
        else:
            self.table.item(row, 3).setForeground(Qt.red)

    def _get_row_data(self, row):
        # Get data from table
        patient = self.table.item(row, 0).text()
        drug_name_table = self.table.item(row, 1).text()
        barcode = self.table.item(row, 2).text()
        doctor_usage = self.table.item(row, 4).text()
        
        # Fetch details from DB for full data (Category, Full Instruction)
        # We need to query again because table only shows short instruction
        rec = None
        if barcode:
            rec = db.get_drug_by_barcode(barcode)
        
        if not rec and drug_name_table:
             # Try search by name if barcode failed
             res = db.search(drug_name_table)
             if res: rec = res[0]
        
        # Construct Data Dict
        data = {
            "drug_name": drug_name_table,
            "patient_name": patient,
            "date": datetime.now().strftime("%d.%m.%Y"),
            "category": "",
            "short_instruction": doctor_usage if doctor_usage else "",
            "full_instruction": "",
            "transaction_id": ""
        }
        
        if rec:
            # rec: (id, barcode, name, cat, preg, short, full)
            data["category"] = rec[3]
            
            # Use configured source for mapping instruction to label
            if self.radio_doctor.isChecked():
                data["short_instruction"] = doctor_usage if doctor_usage else rec[5]
            elif self.radio_db_short.isChecked():
                data["short_instruction"] = rec[5]
            elif self.radio_db_full.isChecked():
                data["short_instruction"] = rec[6]
                
            data["full_instruction"] = rec[6]
        else:
            data["full_instruction"] = "Veritabanında bulunamadı."
            data["short_instruction"] = doctor_usage
            
        return data

    def update_preview(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            self.lbl_preview.clear()
            return
            
        row = selected_items[0].row()
        data = self._get_row_data(row)
        
        # Render
        img = self.renderer.render_image(data)
        pix = QPixmap.fromImage(img)
        
        # fit width
        w = self.lbl_preview.width() - 10
        if w > 10:
             self.lbl_preview.setPixmap(pix.scaledToWidth(w, Qt.SmoothTransformation))

    def print_all(self):
        count = self.table.rowCount()
        if count == 0: return
        
        pm = PrinterManager()
        printer_name = cfg.get("printer_name")
        success = 0
        
        for row in range(count):
            data = self._get_row_data(row)
            if pm.print_label(data, printer_name):
                success += 1
                
        QMessageBox.information(self, "Yazdır", f"{count} adet etiket yazıcıya gönderildi! ({success} başarılı).")

    def clear_table(self):
        self.table.setRowCount(0)
        self.lbl_preview.clear()

    def delete_selected(self):
        selected_rows = sorted(set(index.row() for index in self.table.selectedIndexes()), reverse=True)
        if not selected_rows:
            return
        
        confirm = QMessageBox.question(self, "Sil", f"{len(selected_rows)} kayıt silinecek. Emin misiniz?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            for row in selected_rows:
                self.table.removeRow(row)
            self.update_preview()
