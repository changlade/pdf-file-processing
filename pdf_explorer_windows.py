#!/usr/bin/env python3
"""
PDF Document Explorer - Windows Optimized Version
Fast startup, no console window, optimized for Windows .exe
"""

import os
import sys
import time
import socket
import webbrowser
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import signal
import platform

class PDFExplorerWindows:
    def __init__(self):
        self.server = None
        self.server_thread = None
        self.port = 8000
        self.base_dir = self.get_app_directory()
        
    def get_app_directory(self):
        """Get the directory where the app resources are located"""
        if getattr(sys, 'frozen', False):
            # Running as compiled executable - PyInstaller bundle
            if hasattr(sys, '_MEIPASS'):
                # PyInstaller temp directory
                return sys._MEIPASS
            else:
                # Fallback
                return os.path.dirname(sys.executable)
        else:
            # Running as Python script
            return os.path.dirname(os.path.abspath(__file__))
    
    def find_available_port(self, start_port=8000, max_attempts=10):
        """Find an available port starting from start_port"""
        for i in range(max_attempts):
            port = start_port + i
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    return port
            except OSError:
                continue
        return None
    
    def check_existing_server(self, start_port=8000, max_attempts=10):
        """Check if server is already running and return the port"""
        import urllib.request
        import urllib.error
        
        for i in range(max_attempts):
            port = start_port + i
            try:
                # Try to connect to potential existing server
                url = f"http://localhost:{port}/web/"
                urllib.request.urlopen(url, timeout=1)  # Faster timeout
                return port
            except (urllib.error.URLError, ConnectionRefusedError, OSError):
                continue
        return None
    
    def start_server(self):
        """Start the HTTP server in a separate thread"""
        try:
            # Find available port
            self.port = self.find_available_port()
            if not self.port:
                return False
            
            # Change to the app directory
            os.chdir(self.base_dir)
            
            # Check if required files exist with more specific paths
            web_path = os.path.join(self.base_dir, 'web', 'index.html')
            data_path = os.path.join(self.base_dir, 'data', 'car_references.json')
            
            if not os.path.exists(web_path):
                # Try alternative path for PyInstaller
                web_path = os.path.join(self.base_dir, '..', 'web', 'index.html')
                if not os.path.exists(web_path):
                    return False
            
            # Create server with error handling
            server_address = ('localhost', self.port)
            httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
            self.server = httpd
            
            # Start server in a separate thread
            self.server_thread = threading.Thread(target=self._run_server, daemon=True)
            self.server_thread.start()
            
            # Brief wait to ensure server started
            time.sleep(0.2)
            
            return True
        except Exception as e:
            return False
    
    def _run_server(self):
        """Run the server with error handling"""
        try:
            self.server.serve_forever()
        except Exception:
            pass
    
    def open_browser(self):
        """Open the web browser using threading timer (optimized for Windows)"""
        url = f"http://localhost:{self.port}/web/"
        
        def delayed_open():
            try:
                webbrowser.open(url, new=2)  # new=2 opens in new tab
                return True
            except Exception:
                return False
        
        # Fast browser opening for Windows
        import threading
        timer = threading.Timer(0.2, delayed_open)  # Very fast for Windows
        timer.start()
        
        return True
    
    def run(self):
        """Main application entry point - optimized for Windows"""
        # Fast existing server check
        existing_port = self.check_existing_server()
        
        if existing_port:
            # Found existing server - just open browser
            self.port = existing_port
            self.server = None
            self.open_browser()
            return 0
        
        # No existing server - start new one
        if not self.start_server():
            # Silent fail for Windows - just exit
            return 1
        
        # Very brief wait for server
        time.sleep(0.1)
        
        # Open browser immediately
        self.open_browser()
        
        try:
            # Keep the application running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            if self.server:
                self.server.shutdown()
            return 0

if __name__ == "__main__":
    app = PDFExplorerWindows()
    sys.exit(app.run())
