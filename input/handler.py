class InputHandler:
    def __init__(self):
        pass

    def parse_input(self, raw_text):
        """
        Distinguish between a barcode scan and manual typing.
        """
        # Heuristic: Barcodes are often all numeric and specific lengths (EAN-13, etc)
        if raw_text.isdigit() and len(raw_text) > 8:
            return {"type": "barcode", "value": raw_text}
        else:
            return {"type": "manual", "value": raw_text}

    def process_barcode_mock(self, barcode):
        """
        Mock lookup for barcode. In real app, this queries an API or DB.
        """
        # Mock mapping
        barcode_db = {
            "1234567890123": "Paracetamol 500mg",
            "9876543210987": "Amoxicillin 500mg"
        }
        return barcode_db.get(barcode, None)
