from PySide6.QtPrintSupport import QPrinter, QPrintDialog, QPrinterInfo
from PySide6.QtGui import QPainter, QPageSize, QPageLayout
from PySide6.QtCore import QSizeF, QMarginsF
from label.renderer import LabelRenderer
from config.settings import cfg

class PrinterManager:
    def __init__(self):
        self.renderer = LabelRenderer()

    def get_available_printers(self):
        return QPrinterInfo.availablePrinterNames()

    def print_label(self, data, printer_name=None):
        """
        Prints the label using the system printer.
        """
        printer = QPrinter(QPrinter.HighResolution)
        
        if printer_name:
            printer.setPrinterName(printer_name)
        
        # Setup page size from Config (default 60x40mm)
        w = float(cfg.get("label_width_mm") or 60.0)
        h = float(cfg.get("label_height_mm") or 40.0)
        
        page_size = QPageSize(QSizeF(w, h), QPageSize.Unit.Millimeter)
        printer.setPageSize(page_size)
        
        
        margin = QMarginsF(0, 0, 0, 0)
        printer.setPageMargins(margin, QPageLayout.Unit.Millimeter)
        
        painter = QPainter()
        if not painter.begin(printer):
            print("Failed to open printer.")
            return False
            
        # Delegating painting to the renderer
        self.renderer.paint_on_printer(painter, data)
        
        painter.end()
        return True

    def print_zpl_stub(self, data):
        """
        Example of how a ZPL implementation would look.
        """
        zpl = f"""
        ^XA
        ^FO50,50^ADN,36,20^FD{data.get('pharmacy_name')}^FS
        ^FO50,100^ADN,36,20^FD{data.get('drug_name')}^FS
        ^XZ
        """
        print("Sending ZPL to printer (Stub):")
        print(zpl)
        # raw_socket.send(zpl) ...
