from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
                               QLineEdit, QTextEdit, QPushButton, QFormLayout, QFrame, QMessageBox, QHeaderView, QLabel)
from PySide6.QtCore import Qt
from database.drug_db import db
from utils.translate_db import force_retranslate_drug
import threading

class DrugManagerPage(QWidget):
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
        self.table.setHorizontalHeaderLabels(["ID", "Barkod", "İlaç Adı", "Kategori"])
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
        
        lbl_head = QLabel("İlaç Detayları")
        lbl_head.setStyleSheet("font-weight: bold; font-size: 16px; color: #333;")
        
        form_layout = QFormLayout()
        self.inp_barcode = QLineEdit()
        self.inp_name = QLineEdit()
        self.inp_category = QLineEdit()
        self.inp_preg = QLineEdit()
        self.inp_short = QLineEdit()
        self.inp_full = QTextEdit()
        
        form_layout.addRow("Barkod:", self.inp_barcode)
        form_layout.addRow("İlaç Adı:", self.inp_name)
        form_layout.addRow("Kategori:", self.inp_category)
        form_layout.addRow("Gebelik Kat.:", self.inp_preg)
        form_layout.addRow("Kısa Talimat:", self.inp_short)
        form_layout.addRow("Detaylı Tarif:", self.inp_full)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_new = QPushButton("Yeni / Temizle")
        btn_new.clicked.connect(self.clear_form)
        
        btn_save = QPushButton("Kaydet")
        btn_save.setStyleSheet("background-color: #28a745; color: white; font-weight: bold;")
        btn_save.clicked.connect(self.save_drug)
        
        btn_del = QPushButton("Sil")
        btn_del.setStyleSheet("background-color: #dc3545; color: white; font-weight: bold;")
        btn_del.clicked.connect(self.delete_drug)
        
        btn_retrans = QPushButton("Tercüme Yenile")
        btn_retrans.setStyleSheet("background-color: #17a2b8; color: white; font-weight: bold;")
        btn_retrans.setToolTip("İlacın İngilizce, Rusça, Arapça çevirilerini Google'dan baştan çeker")
        btn_retrans.clicked.connect(self.retranslate_drug)

        btn_layout.addWidget(btn_new)
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_del)
        btn_layout.addWidget(btn_retrans)
        
        right_layout.addWidget(lbl_head)
        right_layout.addLayout(form_layout)
        right_layout.addLayout(btn_layout)
        right_layout.addStretch()
        
        layout.addWidget(left_panel, 3)
        layout.addWidget(right_panel, 2)

    def load_data(self):
        self.table.setRowCount(0)
        drugs = db.get_all_drugs()
        for row_idx, drug in enumerate(drugs):
            # drug: (id, barcode, name, category, preg_cat, short, full)
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(drug[0])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(drug[1] if drug[1] else ""))
            self.table.setItem(row_idx, 2, QTableWidgetItem(drug[2]))
            self.table.setItem(row_idx, 3, QTableWidgetItem(drug[3]))

    def filter_table(self):
        query = self.inp_filter.text().lower()
        for i in range(self.table.rowCount()):
            # Search in Name (2) or Barcode (1)
            name = self.table.item(i, 2).text().lower()
            barcode = self.table.item(i, 1).text().lower()
            self.table.setRowHidden(i, query not in name and query not in barcode)

    def on_row_clicked(self, item):
        row = item.row()
        id_item = self.table.item(row, 0)
        self.selected_id = int(id_item.text())
        
        drugs = db.get_all_drugs()
        for d in drugs:
            if d[0] == self.selected_id:
                # d: 0:id, 1:barcode, 2:name, 3:cat, 4:preg, 5:short, 6:full
                self.inp_barcode.setText(d[1] if d[1] else "")
                self.inp_name.setText(d[2])
                self.inp_category.setText(d[3] if d[3] else "")
                self.inp_preg.setText(d[4] if d[4] else "")
                self.inp_short.setText(d[5] if d[5] else "")
                self.inp_full.setText(d[6] if d[6] else "")
                break

    def clear_form(self):
        self.selected_id = None
        self.inp_barcode.clear()
        self.inp_name.clear()
        self.inp_category.clear()
        self.inp_preg.clear()
        self.inp_short.clear()
        self.inp_full.clear()

    def save_drug(self):
        barcode = self.inp_barcode.text()
        name = self.inp_name.text()
        cat = self.inp_category.text()
        preg = self.inp_preg.text()
        short = self.inp_short.text()
        full = self.inp_full.toPlainText()
        
        if not name:
            QMessageBox.warning(self, "Hata", "İlaç adı boş olamaz!")
            return

        if self.selected_id:
            # Update
            db.update_drug(self.selected_id, barcode, name, cat, preg, short, full)
            QMessageBox.information(self, "Bilgi", "İlaç güncellendi.")
        else:
            # Add
            success = db.add_drug(barcode, name, cat, preg, short, full)
            if not success:
                QMessageBox.warning(self, "Hata", "Bu isimde veya barkodda bir ilaç zaten var!")
                return
            QMessageBox.information(self, "Bilgi", "Yeni ilaç eklendi.")
        
        self.clear_form()
        self.load_data()

    def delete_drug(self):
        if not self.selected_id:
            return
        
        reply = QMessageBox.question(self, "Onay", "Bu ilacı silmek istediğinize emin misiniz?", 
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            db.delete_drug(self.selected_id)
            self.clear_form()
            self.load_data()

    def retranslate_drug(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Uyarı", "Lütfen listeden bir ilaç seçin.")
            return
        
        reply = QMessageBox.question(
            self, "Emin Misiniz?",
            "Bu ilacın İngilizce, Rusça ve Arapça çevirileri sıfırlanıp Google Translate üzerinden yeniden oluşturulacak. \n\nEğer Türkçe talimatta değişiklik yaptıysanız öncelikle 'Kaydet' butonuna basmanız gerekmektedir. Devam edilsin mi?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # We run it in a thread so UI doesn't freeze waiting for API
            def run_translate():
                try:
                    force_retranslate_drug(self.selected_id)
                    # Use a safe way or just print success, qt cross-thread can be tricky
                    print("Çeviri başarıyla güncellendi.")
                except Exception as e:
                    print("Çeviri hatası:", e)
            
            t = threading.Thread(target=run_translate)
            t.start()
            QMessageBox.information(self, "Bilgi", "Seçili ilacın çeviri/güncelleme işlemi arka planda başlatıldı. Veritabanına anında yansıyacaktır.")
