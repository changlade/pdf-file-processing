#!/usr/bin/env python3
"""
PDF Document Explorer - macOS Optimized Version
Fast startup, no console window, optimized for macOS .app
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

class PDFExplorerMac:
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
        # Find available port
        self.port = self.find_available_port()
        if not self.port:
            return False
        
        # Change to the app directory
        os.chdir(self.base_dir)
        
        # Check if required files exist
        if not os.path.exists('web/index.html'):
            return False
        
        try:
            # Create server
            server_address = ('localhost', self.port)
            httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
            self.server = httpd
            
            # Start server in a separate thread
            self.server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
            self.server_thread.start()
            
            return True
        except Exception:
            return False
    
    def open_browser(self):
        """Open the web browser using threading timer (optimized for macOS)"""
        url = f"http://localhost:{self.port}/web/"
        
        def delayed_open():
            try:
                # For macOS, try multiple methods
                import subprocess
                try:
                    # Try using 'open' command first (macOS native)
                    subprocess.run(['open', url], check=True, timeout=5)
                    return True
                except:
                    # Fallback to webbrowser
                    webbrowser.open(url, new=2)
                    return True
            except Exception:
                return False
        
        # Fast browser opening for macOS
        import threading
        timer = threading.Timer(0.3, delayed_open)  # Optimized for macOS
        timer.start()
        
        return True
    
    def show_error_dialog(self, message):
        """Show error dialog on macOS without console"""
        try:
            # Try using osascript for native macOS dialog
            import subprocess
            script = f'''display dialog "{message}" with title "PDF Document Explorer" buttons {{"OK"}} default button "OK" with icon stop'''
            subprocess.run(['osascript', '-e', script], timeout=10)
        except:
            # Fallback to tkinter if osascript fails
            try:
                import tkinter as tk
                from tkinter import messagebox
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror("PDF Document Explorer", message)
                root.destroy()
            except:
                pass
    
    def run(self):
        """Main application entry point - optimized for macOS"""
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
            self.show_error_dialog("Failed to start the application. Please ensure all files are present.")
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
    app = PDFExplorerMac()
    sys.exit(app.run())
