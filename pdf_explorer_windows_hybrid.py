#!/usr/bin/env python3
"""
PDF Document Explorer - Windows Hybrid Version
Shows console briefly during startup, then hides it
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

# Windows-specific imports for console manipulation
if platform.system() == 'Windows':
    try:
        import ctypes
        from ctypes import wintypes
        kernel32 = ctypes.windll.kernel32
        user32 = ctypes.windll.user32
        HWND = ctypes.c_void_p
    except:
        kernel32 = None
        user32 = None

class PDFExplorerWindows:
    def __init__(self):
        self.server = None
        self.server_thread = None
        self.port = 8000
        self.base_dir = self.get_app_directory()
        
    def hide_console(self):
        """Hide the console window on Windows"""
        if platform.system() == 'Windows' and kernel32 and user32:
            try:
                # Get console window handle
                console_window = kernel32.GetConsoleWindow()
                if console_window:
                    # Hide the console window
                    user32.ShowWindow(console_window, 0)  # SW_HIDE = 0
            except:
                pass
        
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
                urllib.request.urlopen(url, timeout=1)
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
            
            # Wait for server to be ready on Windows
            time.sleep(0.5)
            
            # Verify the server thread is actually running
            if not self.server_thread.is_alive():
                return False
            
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
        """Open the web browser using threading timer"""
        url = f"http://localhost:{self.port}/web/"
        
        def delayed_open():
            try:
                webbrowser.open(url, new=2)  # new=2 opens in new tab
                return True
            except Exception:
                return False
        
        # Browser opening with appropriate delay
        import threading
        timer = threading.Timer(0.5, delayed_open)
        timer.start()
        
        return True
    
    def run(self):
        """Main application entry point - Windows hybrid approach"""
        print("🚀 Starting PDF Document Explorer...")
        
        # Check for existing server first
        existing_port = self.check_existing_server()
        
        if existing_port:
            print(f"✅ Found existing server on port {existing_port}")
            self.port = existing_port
            self.server = None
            self.open_browser()
            
            # Hide console after successful connection
            time.sleep(1)
            self.hide_console()
            
            # Keep running to maintain the browser connection reference
            try:
                while True:
                    time.sleep(10)
            except KeyboardInterrupt:
                return 0
        
        # No existing server - start new one
        print("🔧 Starting new server...")
        if not self.start_server():
            print("❌ Failed to start server")
            input("Press Enter to exit...")
            return 1
        
        print(f"✅ Server started on port {self.port}")
        
        # Wait for server to be fully ready
        print("🔄 Waiting for server to be ready...")
        time.sleep(1.0)
        
        # Verify server is actually running
        import urllib.request
        import urllib.error
        server_ready = False
        for attempt in range(10):  # Try for 5 seconds
            try:
                url = f"http://localhost:{self.port}/web/"
                urllib.request.urlopen(url, timeout=1)
                server_ready = True
                break
            except:
                time.sleep(0.5)
        
        if not server_ready:
            print("❌ Server not responding")
            input("Press Enter to exit...")
            return 1
        
        print("🌐 Opening browser...")
        self.open_browser()
        
        # Wait a moment for browser to start opening
        time.sleep(2)
        
        # Hide console window after successful startup
        print("✅ Startup complete - hiding console...")
        time.sleep(1)
        self.hide_console()
        
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
