#!/usr/bin/env python3
"""
PDF Document Explorer - Standalone Application
Creates a local web server and opens the PDF explorer in the browser
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

class PDFExplorerApp:
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
                urllib.request.urlopen(url, timeout=2)
                print(f"✅ Found existing server running on port {port}")
                return port
            except (urllib.error.URLError, ConnectionRefusedError, OSError):
                continue
        return None
    
    def start_server(self):
        """Start the HTTP server in a separate thread"""
        # Find available port
        self.port = self.find_available_port()
        if not self.port:
            self.show_error("Could not find an available port to start the server.")
            return False
        
        # Change to the app directory
        os.chdir(self.base_dir)
        
        # Check if required files exist
        if not os.path.exists('web/index.html'):
            self.show_error("Required files not found. Please ensure the application is properly installed.")
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
        except Exception as e:
            self.show_error(f"Failed to start server: {str(e)}")
            return False
    
    def open_browser(self):
        """Open the web browser using threading timer (recommended for packaged apps)"""
        url = f"http://localhost:{self.port}/web/"
        
        def delayed_open():
            try:
                print(f"🌐 Opening browser: {url}")
                webbrowser.open(url, new=2)  # new=2 opens in new tab
                return True
            except Exception as e:
                print(f"⚠️  Browser auto-open failed: {str(e)}")
                return False
        
        # Use threading timer for delayed browser opening (best practice for packaged apps)
        import threading
        timer = threading.Timer(0.5, delayed_open)  # Reduced to 0.5 second delay
        timer.start()
        
        print("🔄 Browser will open automatically in 0.5 seconds...")
        return True  # Assume success since we're using timer
    
    def show_error(self, message):
        """Show error message to user"""
        print(f"❌ ERROR: {message}")
        input("Press Enter to exit...")
    
    def show_success(self, browser_opened=True):
        """Show success message to user - console version"""
        url = f"http://localhost:{self.port}/web/"
        
        print("\n" + "="*60)
        print("🎉 PDF Document Explorer is now running!")
        print("="*60)
        print(f"🌐 URL: {url}")
        
        if browser_opened:
            print("🚀 Your browser should open automatically")
        else:
            print("⚠️  Browser didn't open automatically")
        
        print("")
        print("💡 If browser doesn't open:")
        print(f"   1. Copy this URL: {url}")
        print("   2. Open your web browser")
        print("   3. Paste the URL and press Enter")
        print("")
        print("🛑 To stop the server: Close this window or press Ctrl+C")
        print("="*60)
        print("")
    
    def run(self):
        """Main application entry point"""
        print("🚀 Starting PDF Document Explorer...")
        print("📍 Application directory:", self.base_dir)
        
        # First check if a server is already running
        existing_port = self.check_existing_server()
        
        if existing_port:
            print(f"🔄 Server already running on port {existing_port}")
            self.port = existing_port
            self.server = None  # We're not managing this server
            
            # Just open browser to existing server
            print("🌐 Opening browser to existing server...")
            browser_opened = self.open_browser()
            
            if browser_opened:
                print("✅ Browser opened successfully")
            else:
                print("⚠️  Browser failed to open automatically")
            
            # Show success message for existing server
            self.show_success(browser_opened)
            
            # Don't start a new server loop, just open browser and exit
            print("🎉 Connected to existing server. You can close this window.")
            input("Press Enter to close this window...")
            return 0
        
        # No existing server found, start a new one
        print("🔧 No existing server found, starting new server...")
        
        # Start the server
        if not self.start_server():
            return 1
        
        print(f"✅ Server started successfully on port {self.port}")
        
        # Brief wait for server to be ready (reduced from 2 seconds)
        time.sleep(0.3)
        
        # Open browser
        print("🌐 Opening browser...")
        browser_opened = self.open_browser()
        
        if browser_opened:
            print("✅ Browser opened successfully")
        else:
            print("⚠️  Browser failed to open automatically")
        
        # Show success dialog
        self.show_success(browser_opened)
        
        print("🔄 Server is running... Press Ctrl+C to stop")
        
        try:
            # Keep the application running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down server...")
            if self.server:
                self.server.shutdown()
            print("✅ Server stopped. Goodbye!")
            return 0

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🛑 Received shutdown signal...")
    sys.exit(0)

if __name__ == "__main__":
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    if platform.system() != "Windows":
        signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and run the application
    app = PDFExplorerApp()
    exit_code = app.run()
    sys.exit(exit_code)
