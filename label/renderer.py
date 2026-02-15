from PySide6.QtGui import QPainter, QColor, QFont, QImage, QPen, QBrush
from PySide6.QtCore import QRectF, Qt
from config.settings import cfg

class LabelRenderer:
    def __init__(self):
        self.width_mm = cfg.get("label_width_mm")
        self.height_mm = cfg.get("label_height_mm")
        self.dpi = 203
        self.dpmm = self.dpi / 25.4
        self.w_px = int(self.width_mm * self.dpmm)
        self.h_px = int(self.height_mm * self.dpmm)

    def render_image(self, data):
        image = QImage(self.w_px, self.h_px, QImage.Format_ARGB32)
        image.fill(QColor("#FFFF00")) # Vibrant Yellow
        
        painter = QPainter(image)
        self.paint(painter, data, self.w_px, self.h_px)
        painter.end()
        return image

    def paint(self, p: QPainter, data: dict, w: int, h: int):
        # Colors
        c_yellow = QColor("#FFFF00") # Main bg
        c_black = QColor("#000000")
        c_white = QColor("#FFFFFF")
        
        # Ensure bg is yellow (if printing directly)
        p.fillRect(0, 0, w, h, c_yellow)
        
        # Margins / Constants
        m_side = w * 0.02
        line_h = h * 0.05
        
        # Fonts
        # Adjust sizes relative to height 40mm (approx 320px at 203dpi)
        f_small = QFont("Arial", 7)
        f_std = QFont("Arial", 9)
        f_bold = QFont("Arial", 9, QFont.Bold)
        f_large_bold = QFont("Arial", 10, QFont.Bold)
        f_category = QFont("Arial", 9, QFont.Bold)
        
        # --- 1. Top Row: Drug Name | Date ---
        # Height approx 12%
        y_cursor = 0
        h_row1 = h * 0.12
        r_row1 = QRectF(m_side, y_cursor, w - 2*m_side, h_row1)
        
        p.setPen(c_black)
        p.setFont(f_std)
        # Drug Name (Left)
        p.drawText(r_row1, Qt.AlignLeft | Qt.AlignVCenter, data.get("drug_name", ""))
        # Date (Right)
        p.drawText(r_row1, Qt.AlignRight | Qt.AlignVCenter, data.get("date", ""))
        
        y_cursor += h_row1
        
        # --- 2. Category Bar (Black) ---
        # Height approx 12%
        h_cat = h * 0.12
        r_cat = QRectF(0, y_cursor, w, h_cat)
        p.fillRect(r_cat, c_black)
        
        p.setPen(c_white)
        p.setFont(f_category)
        category_text = data.get("category", "GENEL KULLANIM")
        p.drawText(r_cat, Qt.AlignCenter, category_text)
        
        y_cursor += h_cat
        
        # --- 3. Short Instruction (Bold) ---
        # Height approx 20%, Yellow bg
        h_short = h * 0.22
        r_short = QRectF(m_side, y_cursor, w - 2*m_side, h_short)
        
        p.setPen(c_black)
        p.setFont(f_large_bold)
        short_inst = data.get("short_instruction", "")
        # TextOption for wrapping
        p.drawText(r_short, Qt.AlignLeft | Qt.AlignVCenter | Qt.TextWordWrap, short_inst)
        
        y_cursor += h_short
        
        # Divider Line (Thin)
        p.drawLine(0, y_cursor, w, y_cursor)
        
        # --- 4. Full Instruction (Body) ---
        # Remainder until footer bars
        # Reserve bottom ~20% for footers
        h_footer_total = h * 0.22
        h_body = h - y_cursor - h_footer_total
        
        r_body = QRectF(m_side, y_cursor + 2, w - 2*m_side, h_body)
        p.setFont(f_small)
        full_inst = data.get("full_instruction", "")
        p.drawText(r_body, Qt.AlignLeft | Qt.AlignTop | Qt.TextWordWrap, full_inst)
        
        y_cursor += h_body
        
        # --- 5. Info Bar (Black) ---
        h_info = h * 0.10
        r_info = QRectF(0, y_cursor, w, h_info)
        p.fillRect(r_info, c_black)
        
        p.setPen(c_white)
        p.setFont(QFont("Arial", 8, QFont.Bold))
        
        # Transaction ID / Left -> replaced by Patient Name
        pat_name = data.get("patient_name", "").upper()
        if not pat_name:
            pat_name = "HASTA ADI GIRILMEDI"
            
        p.drawText(QRectF(m_side, y_cursor, w/2, h_info), Qt.AlignLeft | Qt.AlignVCenter, pat_name)
        
        # Label Right
        # In image: "BİTİŞ TARİHİ" text
        p.setPen(QColor("#AAAAAA")) # Slightly dimmed
        p.setFont(QFont("Arial", 6))
        p.drawText(QRectF(w/2, y_cursor, w/2 - m_side, h_info), Qt.AlignRight | Qt.AlignVCenter, "BİTİŞ TARİHİ")
        
        y_cursor += h_info
        
        # --- 6. Pharmacy Footer ---
        h_pharm = h - y_cursor
        r_pharm = QRectF(m_side, y_cursor, w - 2*m_side, h_pharm)
        
        p.setPen(c_black)
        p.setFont(QFont("Arial", 7, QFont.Bold))
        pharm_info = f"{cfg.get('pharmacy_name')} / {cfg.get('pharmacy_phone')}"
        p.drawText(r_pharm, Qt.AlignCenter, pharm_info)

