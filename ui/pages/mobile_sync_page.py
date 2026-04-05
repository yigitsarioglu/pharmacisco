from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QScrollArea, QFrame, QMessageBox, QGroupBox, QDateEdit
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont

# We import the send_prescription_to_cloud function from our client
from mobile_api_client import send_prescription_to_cloud

class MobileSyncPage(QWidget):
    def __init__(self):
        super().__init__()
        self.medications = []
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        lbl_title = QLabel("Mobil Uygulamaya E-Reçete Gönder")
        lbl_title.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(lbl_title)
        
        # Patient Info
        group_patient = QGroupBox("Hasta Bilgileri")
        layout_patient = QHBoxLayout()
        
        self.input_identifier = QLineEdit()
        self.input_identifier.setPlaceholderText("Hasta TC Kimlik No veya Telefon numarası")
        
        layout_patient.addWidget(QLabel("TC / Tel:"))
        layout_patient.addWidget(self.input_identifier)
        group_patient.setLayout(layout_patient)
        layout.addWidget(group_patient)
        
        # Add Medication Form
        group_med = QGroupBox("İlaç Ekle")
        layout_med = QVBoxLayout()
        
        row1 = QHBoxLayout()
        self.input_med_name = QLineEdit()
        self.input_med_name.setPlaceholderText("İlaç Adı (Örn: Parol 500mg)")
        self.input_dosage = QLineEdit()
        self.input_dosage.setPlaceholderText("Doz (Örn: 1 tablet)")
        row1.addWidget(QLabel("İlaç:"))
        row1.addWidget(self.input_med_name)
        row1.addWidget(QLabel("Doz:"))
        row1.addWidget(self.input_dosage)
        layout_med.addLayout(row1)
        
        row2 = QHBoxLayout()
        self.input_times = QLineEdit()
        self.input_times.setPlaceholderText("Saatler (virgülle ayırın, Örn: 09:00, 21:00)")
        self.input_notes = QLineEdit()
        self.input_notes.setPlaceholderText("Kısa Talimat (Örn: Tok karnına)")
        row2.addWidget(QLabel("Saatler:"))
        row2.addWidget(self.input_times)
        row2.addWidget(QLabel("Not:"))
        row2.addWidget(self.input_notes)
        layout_med.addLayout(row2)
        
        row3 = QHBoxLayout()
        self.date_start = QDateEdit()
        self.date_start.setDate(QDate.currentDate())
        self.date_start.setCalendarPopup(True)
        self.date_start.setDisplayFormat("yyyy-MM-dd")
        self.date_end = QDateEdit()
        self.date_end.setDate(QDate.currentDate().addDays(7))
        self.date_end.setCalendarPopup(True)
        self.date_end.setDisplayFormat("yyyy-MM-dd")
        
        row3.addWidget(QLabel("Başlangıç:"))
        row3.addWidget(self.date_start)
        row3.addWidget(QLabel("Bitiş:"))
        row3.addWidget(self.date_end)
        
        btn_add_med = QPushButton("Listeye Ekle")
        btn_add_med.clicked.connect(self.add_medication)
        row3.addStretch()
        row3.addWidget(btn_add_med)
        layout_med.addLayout(row3)
        
        group_med.setLayout(layout_med)
        layout.addWidget(group_med)
        
        # Current Medications List
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.list_container)
        layout.addWidget(self.scroll_area)
        
        # Send Button
        self.btn_send = QPushButton("E-Reçeteyi Mobil Uygulamaya Gönder")
        self.btn_send.setMinimumHeight(50)
        self.btn_send.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; font-size: 14px;")
        self.btn_send.clicked.connect(self.send_prescription)
        layout.addWidget(self.btn_send)
        
    def add_medication(self):
        name = self.input_med_name.text().strip()
        dosage = self.input_dosage.text().strip()
        times_str = self.input_times.text().strip()
        notes = self.input_notes.text().strip()
        start_date = self.date_start.date().toString("yyyy-MM-dd")
        end_date = self.date_end.date().toString("yyyy-MM-dd")
        
        if not name or not dosage or not times_str:
            QMessageBox.warning(self, "Uyarı", "İlaç Adı, Doz ve Saatler alanları zorunludur.")
            return
            
        times_list = [t.strip() for t in times_str.split(',') if t.strip()]
        
        med_dict = {
            "name": name,
            "dosage": dosage,
            "notes": notes,
            "times": times_list,
            "start_date": start_date,
            "end_date": end_date
        }
        self.medications.append(med_dict)
        self.refresh_med_list()
        
        # Clear inputs
        self.input_med_name.clear()
        self.input_dosage.clear()
        self.input_times.clear()
        self.input_notes.clear()
        
    def refresh_med_list(self):
        # Clear layout
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
                
        for idx, med in enumerate(self.medications):
            frame = QFrame()
            frame.setStyleSheet("background-color: #ecf0f1; border-radius: 5px; padding: 5px; color: black; font-weight: bold;")
            flayout = QHBoxLayout(frame)
            
            lbl = QLabel(f"{med['name']} - {med['dosage']} - Saatler: {', '.join(med['times'])}")
            lbl.setStyleSheet("color: black;")
            btn_del = QPushButton("Sil")
            btn_del.setFixedWidth(50)
            btn_del.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold;")
            
            # Using default argument trick for loop lambda closure
            btn_del.clicked.connect(lambda checked=False, i=idx: self.delete_medication(i))
            
            flayout.addWidget(lbl)
            flayout.addWidget(btn_del)
            self.list_layout.addWidget(frame)
            
    def delete_medication(self, index):
        self.medications.pop(index)
        self.refresh_med_list()
        
    def send_prescription(self):
        user_id = self.input_identifier.text().strip()
        if not user_id:
            QMessageBox.warning(self, "Uyarı", "Lütfen hastanın TC Kimlik numarasını girin.")
            return
            
        if not self.medications:
            QMessageBox.warning(self, "Uyarı", "Lütfen en az bir ilaç ekleyin.")
            return
            
        self.btn_send.setEnabled(False)
        self.btn_send.setText("Gönderiliyor...")
        
        try:
            success = send_prescription_to_cloud(user_id, self.medications)
            if success:
                QMessageBox.information(self, "Başarılı", "Reçete hastanın mobil uygulamasına başarıyla iletildi!")
                self.medications.clear()
                self.refresh_med_list()
                self.input_identifier.clear()
            else:
                QMessageBox.critical(self, "Hata", "Reçete iletilemedi. Hasta Supabase'e kayıt olmamış olabilir mi?")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Beklenmeyen bir hata oluştu: {str(e)}")
        finally:
            self.btn_send.setEnabled(True)
            self.btn_send.setText("E-Reçeteyi Mobil Uygulamaya Gönder")
