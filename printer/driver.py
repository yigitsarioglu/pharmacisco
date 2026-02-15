from PySide6.QtPrintSupport import QPrinter, QPrintDialog, QPrinterInfo
from PySide6.QtGui import QPainter, QPageSize
from label.renderer import LabelRenderer

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
        
        # Setup page size (Custom 60x40mm)
        # Note: Qt handling of custom page sizes can be tricky on Windows without correct driver settings.
        # We try to set it, but user driver preferences often override.
        page_size = QPageSize(QSize(60, 40), QPageSize.Millimeter)
        printer.setPageSize(page_size)
        
        # Setup margins to 0, we handle margins in renderer
        printer.setPageMargins(0, 0, 0, 0, QPrinter.Millimeter)
        
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
