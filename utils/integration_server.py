import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from PySide6.QtCore import QObject, Signal

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Send to main thread via the server object
            if self.server.callback:
                self.server.callback(data)
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*') # Allow browser access
            self.end_headers()
            self.wfile.write(b'{"status": "success"}')
            
        except Exception as e:
            print(f"Server Error: {e}")
            self.send_response(500)
            self.end_headers()

    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        return # Silence logs

class IntegrationServer(QObject):
    request_received = Signal(dict)

    def __init__(self, port=5500):
        super().__init__()
        self.port = port
        self.httpd = None
        self.thread = None
        self.running = False

    def start_server(self):
        if self.running: return
        
        try:
            self.httpd = HTTPServer(('localhost', self.port), RequestHandler)
            # Inject callback to access signal
            self.httpd.callback = self.on_request
            self.running = True
            
            self.thread = threading.Thread(target=self.httpd.serve_forever)
            self.thread.daemon = True
            self.thread.start()
            print(f"Integration Server started on port {self.port}")
            return True
        except Exception as e:
            print(f"Failed to start server: {e}")
            return False

    def stop_server(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
            self.running = False

    def on_request(self, data):
        self.request_received.emit(data)
