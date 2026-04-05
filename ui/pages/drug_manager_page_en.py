from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
                               QLineEdit, QTextEdit, QPushButton, QFormLayout, QFrame, QMessageBox, QHeaderView, QLabel)
from PySide6.QtCore import Qt
from database.drug_db import db

class DrugManagerPageEN(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_id = None
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QHBoxLayout(self)
        
        # --- LEFT: List & Filter ---
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0,0,0,0)
        
        self.inp_filter = QLineEdit()
        self.inp_filter.setPlaceholderText("Barkod veya İsimle Ara...")
        self.inp_filter.textChanged.connect(self.filter_table)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4) # ID, Barcode, Name, Category
        self.table.setHorizontalHeaderLabels(["ID", "Barkod", "İlaç Adı (EN)", "Kategori (EN)"])
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.itemClicked.connect(self.on_row_clicked)
        self.table.hideColumn(0) # Hide ID
        
        left_layout.addWidget(self.inp_filter)
        left_layout.addWidget(self.table)
        
        # --- RIGHT: Form ---
        right_panel = QFrame()
        right_panel.setStyleSheet("""
            QFrame { background-color: #EEE; border-radius: 5px; }
            QLineEdit, QTextEdit { background-color: white; border: 1px solid #CCC; padding: 4px; border-radius: 4px; }
        """)
        right_layout = QVBoxLayout(right_panel)
        
        lbl_head = QLabel("İlaç Detayları (İngilizce - EN)")
        lbl_head.setStyleSheet("font-weight: bold; font-size: 16px; color: #333;")
        
        form_layout = QFormLayout()
        
        # Display Only
        self.lbl_barcode = QLabel("-")
        self.lbl_barcode.setStyleSheet("font-weight: bold;")
        
        self.inp_name_en = QLineEdit()
        self.inp_category_en = QLineEdit()
        self.inp_preg = QLineEdit()
        self.inp_short_en = QLineEdit()
        self.inp_full_en = QTextEdit()
        
        form_layout.addRow("Barkod (Sabit):", self.lbl_barcode)
        form_layout.addRow("İlaç Adı (EN):", self.inp_name_en)
        form_layout.addRow("Kategori (EN):", self.inp_category_en)
        form_layout.addRow("Gebelik Kat.:", self.inp_preg)
        form_layout.addRow("Kısa Talimat (EN):", self.inp_short_en)
        form_layout.addRow("Detaylı Tarif (EN):", self.inp_full_en)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_new = QPushButton("Temizle Seçimi")
        btn_new.clicked.connect(self.clear_form)
        
        btn_save = QPushButton("İngilizce Veriyi Kaydet")
        btn_save.setStyleSheet("background-color: #28a745; color: white; font-weight: bold;")
        btn_save.clicked.connect(self.save_drug)
        
        btn_layout.addWidget(btn_new)
        btn_layout.addWidget(btn_save)
        
        right_layout.addWidget(lbl_head)
        right_layout.addLayout(form_layout)
        right_layout.addLayout(btn_layout)
        right_layout.addStretch()
        
        layout.addWidget(left_panel, 3)
        layout.addWidget(right_panel, 2)

    def load_data(self):
        self.table.setRowCount(0)
        # We need the full columns to get name_en, category_en etc.
        conn = db._get_conn() if hasattr(db, '_get_conn') else __import__('sqlite3').connect(db.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, barcode, name, category, pregnancy_category, name_en, category_en, short_instruction_en, full_instruction_en FROM drugs ORDER BY name ASC")
        drugs = cursor.fetchall()
        
        for row_idx, drug in enumerate(drugs):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(drug[0])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(drug[1] if drug[1] else ""))
            self.table.setItem(row_idx, 2, QTableWidgetItem(drug[5] if drug[5] else drug[2])) # Show EN name, fallback to TR if empty
            self.table.setItem(row_idx, 3, QTableWidgetItem(drug[6] if drug[6] else drug[3])) # Show EN category, fallback to TR if empty
            
        conn.close()

    def filter_table(self):
        query = self.inp_filter.text().lower()
        for i in range(self.table.rowCount()):
            name = self.table.item(i, 2).text().lower()
            barcode = self.table.item(i, 1).text().lower()
            self.table.setRowHidden(i, query not in name and query not in barcode)

    def on_row_clicked(self, item):
        row = item.row()
        id_item = self.table.item(row, 0)
        self.selected_id = int(id_item.text())
        
        conn = __import__('sqlite3').connect(db.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT barcode, pregnancy_category, name_en, category_en, short_instruction_en, full_instruction_en FROM drugs WHERE id=?", (self.selected_id,))
        d = cursor.fetchone()
        conn.close()
        
        if d:
            self.lbl_barcode.setText(d[0] if d[0] else "")
            self.inp_preg.setText(d[1] if d[1] else "")
            self.inp_name_en.setText(d[2] if d[2] else "")
            self.inp_category_en.setText(d[3] if d[3] else "")
            self.inp_short_en.setText(d[4] if d[4] else "")
            self.inp_full_en.setText(d[5] if d[5] else "")

    def clear_form(self):
        self.selected_id = None
        self.lbl_barcode.setText("-")
        self.inp_name_en.clear()
        self.inp_category_en.clear()
        self.inp_preg.clear()
        self.inp_short_en.clear()
        self.inp_full_en.clear()

    def save_drug(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Hata", "Lütfen listeden düzenlemek istediğiniz ilacı seçin.")
            return

        name_en = self.inp_name_en.text()
        cat_en = self.inp_category_en.text()
        preg = self.inp_preg.text()
        short_en = self.inp_short_en.text()
        full_en = self.inp_full_en.toPlainText()

        success = db.update_drug_en(self.selected_id, name_en, cat_en, preg, short_en, full_en)
        if success:
            QMessageBox.information(self, "Bilgi", "İlacın İngilizce verileri başarıyla güncellendi.")
        else:
            QMessageBox.warning(self, "Hata", "Veritabanı güncellenirken bir hata oluştu.")
        
        self.load_data()
