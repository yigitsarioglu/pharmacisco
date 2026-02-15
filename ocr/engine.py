import cv2
import pytesseract
import re
import os
import sys

# Set Tesseract Path (Windows default)
# The user might need to change this or add to PATH
possible_paths = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    r"C:\Users\yigit\AppData\Local\Tesseract-OCR\tesseract.exe"
]
for p in possible_paths:
    if os.path.exists(p):
        pytesseract.pytesseract.tesseract_cmd = p
        break

class OCREngine:
    def __init__(self):
        pass

    def detect_text(self, image_path):
        if not os.path.exists(image_path):
            return "Error: Image file not found."
            
        try:
            # Load image
            img = cv2.imread(image_path)
            # Convert to RGB for Tesseract
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Simple wrapper to get string
            # --psm 6 is good for uniform blocks of text
            text = pytesseract.image_to_string(rgb, lang='tur+eng', config='--psm 6')
            return text
        except Exception as e:
            return f"Error during OCR: {e}. (Is Tesseract installed?)"

    def parse_prescription(self, text):
        """
        Parses the specific format from the screenshot.
        Example line: 
        Adı : FAMODIN 40 MG.30 TB. (8699516094171) Adet : 1 Kullanım : Günde 2x1...
        """
        results = []
        
        # Regex to find: Adı : {NAME} ({BARCODE}) ... Kullanım : {USAGE} ...
        # Note: OCR often messes up structure, so we look for patterns line by line or globally.
        # User image shows clearly defined lines.
        
        # Pattern Breakdown:
        # Adı\s*: matches "Adı :"
        # \s*(?P<name>.*?)\s* matches drug name until...
        # \( matches opening paren
        # (?P<barcode>\d{13}) matches 13 digit barcode
        # \) matches closing paren
        # .*? matches stuff in between (Adet : 1 etc)
        # Kullanım\s*:\s*(?P<usage>.*?) matches usage
        # We stop at some reasonable delimiter or end of line.
        
        pattern = re.compile(
            r"Adı\s*[:;]\s*(?P<name>.*?)\s*\((?P<barcode>\d{13})\).*?Kullanım\s*[:;]\s*(?P<usage>.*?)(?=\s+Ağızdan|$|\n\s*Adı)", 
            re.IGNORECASE | re.DOTALL
        )
        
        # Since the text might be line-wrapped, 'findall' on the whole block is better if structure is consistent.
        # But image shows one drug per section.
        
        matches = pattern.finditer(text)
        for m in matches:
            drug = {
                "name": m.group("name").strip().replace("\n", " "),
                "barcode": m.group("barcode"),
                "usage": m.group("usage").strip().replace("\n", " ")
            }
            results.append(drug)
            
        return results

ocr_engine = OCREngine()
