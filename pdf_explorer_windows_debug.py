#!/usr/bin/env python3
"""
PDF Document Explorer - Windows Debug Version
With console output for troubleshooting
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
                print(f"🔧 PyInstaller temp dir: {sys._MEIPASS}")
                return sys._MEIPASS
            else:
                # Fallback
                print(f"🔧 Executable dir: {os.path.dirname(sys.executable)}")
                return os.path.dirname(sys.executable)
        else:
            # Running as Python script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            print(f"🔧 Script dir: {script_dir}")
            return script_dir
    
    def find_available_port(self, start_port=8000, max_attempts=10):
        """Find an available port starting from start_port"""
        for i in range(max_attempts):
            port = start_port + i
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    print(f"✅ Found available port: {port}")
                    return port
            except OSError as e:
                print(f"❌ Port {port} not available: {e}")
                continue
        print("❌ No available ports found")
        return None
    
    def check_existing_server(self, start_port=8000, max_attempts=10):
        """Check if server is already running and return the port"""
        import urllib.request
        import urllib.error
        
        print("🔍 Checking for existing servers...")
        for i in range(max_attempts):
            port = start_port + i
            try:
                # Try to connect to potential existing server
                url = f"http://localhost:{port}/web/"
                urllib.request.urlopen(url, timeout=1)
                print(f"✅ Found existing server on port {port}")
                return port
            except (urllib.error.URLError, ConnectionRefusedError, OSError):
                continue
        print("🔍 No existing servers found")
        return None
    
    def start_server(self):
        """Start the HTTP server in a separate thread"""
        try:
            print("🚀 Starting server...")
            print(f"📍 Base directory: {self.base_dir}")
            print(f"📁 Directory contents: {os.listdir(self.base_dir)}")
            
            # Find available port
            self.port = self.find_available_port()
            if not self.port:
                print("❌ No available port found")
                return False
            
            # Change to the app directory
            os.chdir(self.base_dir)
            print(f"🔧 Changed to directory: {os.getcwd()}")
            
            # Check if required files exist with more specific paths
            web_path = os.path.join(self.base_dir, 'web', 'index.html')
            data_path = os.path.join(self.base_dir, 'data', 'car_references.json')
            
            print(f"🔍 Looking for web files at: {web_path}")
            print(f"🔍 Looking for data files at: {data_path}")
            
            if not os.path.exists(web_path):
                print(f"❌ Web files not found at: {web_path}")
                # List directory contents for debugging
                if os.path.exists(os.path.dirname(web_path)):
                    print(f"📁 Contents of {os.path.dirname(web_path)}: {os.listdir(os.path.dirname(web_path))}")
                return False
            
            if not os.path.exists(data_path):
                print(f"❌ Data files not found at: {data_path}")
                # List directory contents for debugging
                if os.path.exists(os.path.dirname(data_path)):
                    print(f"📁 Contents of {os.path.dirname(data_path)}: {os.listdir(os.path.dirname(data_path))}")
                return False
            
            print("✅ All required files found")
            
            # Create server with error handling
            server_address = ('localhost', self.port)
            httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
            self.server = httpd
            
            print(f"🌐 Server created on {server_address}")
            
            # Start server in a separate thread
            self.server_thread = threading.Thread(target=self._run_server, daemon=True)
            self.server_thread.start()
            
            print("🔄 Server thread started")
            
            # Brief wait to ensure server started
            time.sleep(0.2)
            
            print("✅ Server startup complete")
            return True
        except Exception as e:
            print(f"❌ Server startup failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _run_server(self):
        """Run the server with error handling"""
        try:
            print("🔄 Server thread running...")
            self.server.serve_forever()
        except Exception as e:
            print(f"❌ Server error: {e}")
            import traceback
            traceback.print_exc()
    
    def open_browser(self):
        """Open the web browser using threading timer (optimized for Windows)"""
        url = f"http://localhost:{self.port}/web/"
        print(f"🌐 Preparing to open browser: {url}")
        
        def delayed_open():
            try:
                print(f"🚀 Opening browser: {url}")
                webbrowser.open(url, new=2)  # new=2 opens in new tab
                print("✅ Browser opened successfully")
                return True
            except Exception as e:
                print(f"❌ Browser opening failed: {e}")
                return False
        
        # Fast browser opening for Windows
        import threading
        timer = threading.Timer(0.5, delayed_open)  # Slightly longer for debugging
        timer.start()
        
        print("🔄 Browser timer started")
        return True
    
    def run(self):
        """Main application entry point - optimized for Windows"""
        print("🚀 PDF Document Explorer - Windows Debug Version")
        print(f"🖥️  Platform: {platform.system()} {platform.release()}")
        print(f"🐍 Python: {sys.version}")
        
        # Fast existing server check
        existing_port = self.check_existing_server()
        
        if existing_port:
            # Found existing server - just open browser
            print(f"🔄 Using existing server on port {existing_port}")
            self.port = existing_port
            self.server = None
            self.open_browser()
            
            print("⏱️  Waiting 5 seconds before exit...")
            time.sleep(5)
            return 0
        
        # No existing server - start new one
        if not self.start_server():
            print("❌ Failed to start server")
            input("Press Enter to exit...")
            return 1
        
        print("✅ Server started successfully")
        
        # Very brief wait for server
        time.sleep(0.2)
        
        # Open browser immediately
        self.open_browser()
        
        print("🔄 Server running... Press Ctrl+C to stop")
        
        try:
            # Keep the application running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            if self.server:
                self.server.shutdown()
            return 0

if __name__ == "__main__":
    app = PDFExplorerWindows()
    sys.exit(app.run())
