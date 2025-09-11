#!/usr/bin/env python3
"""
PDF Document Explorer - Windows Official Version
Fast startup, reliable server detection, proper cleanup
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
import atexit
import concurrent.futures

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
        self.cleanup_registered = False
        
        # Register cleanup function
        atexit.register(self.cleanup)
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
    def _signal_handler(self, signum, frame):
        """Handle termination signals"""
        self.cleanup()
        sys.exit(0)
        
    def cleanup(self):
        """Clean up resources to prevent background tasks"""
        if not self.cleanup_registered:
            self.cleanup_registered = True
            if self.server:
                try:
                    self.server.shutdown()
                    self.server.server_close()
                except:
                    pass
            if self.server_thread and self.server_thread.is_alive():
                try:
                    # Force thread termination if needed
                    pass
                except:
                    pass
        
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
        """Fast check if server is already running and return the port"""
        import urllib.request
        import urllib.error
        
        def check_port(port):
            try:
                # Quick socket check first (faster than HTTP)
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(0.1)  # Very fast timeout
                    result = s.connect_ex(('localhost', port))
                    if result != 0:
                        return None
                
                # If socket connects, verify it's our server with HTTP
                url = f"http://localhost:{port}/web/"
                request = urllib.request.Request(url)
                request.add_header('User-Agent', 'PDF-Explorer-Check')
                with urllib.request.urlopen(request, timeout=0.3) as response:
                    # Quick check - if we get a response, it's likely our server
                    return port
            except:
                return None
        
        # Check ports concurrently for speed
        ports_to_check = [start_port + i for i in range(max_attempts)]
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_port = {executor.submit(check_port, port): port for port in ports_to_check}
            
            for future in concurrent.futures.as_completed(future_to_port, timeout=1.0):
                try:
                    result = future.result()
                    if result:
                        return result
                except:
                    continue
        
        return None
    
    def start_server(self):
        """Start the HTTP server with fast startup"""
        try:
            # Find available port quickly
            self.port = self.find_available_port()
            if not self.port:
                return False
            
            # Set working directory
            os.chdir(self.base_dir)
            
            # Quick file existence check (no deep validation for speed)
            web_exists = (os.path.exists(os.path.join(self.base_dir, 'web')) or 
                         os.path.exists(os.path.join(self.base_dir, '..', 'web')))
            if not web_exists:
                return False
            
            # Create and start server immediately
            server_address = ('localhost', self.port)
            self.server = HTTPServer(server_address, SimpleHTTPRequestHandler)
            
            # Start server thread with faster startup
            self.server_thread = threading.Thread(target=self._run_server, daemon=False)
            self.server_thread.start()
            
            # Minimal wait - just ensure thread started
            time.sleep(0.1)
            
            return self.server_thread.is_alive()
        except Exception:
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
        """Main application entry point - fast and reliable"""
        print("🚀 PDF Document Explorer - Fast Startup")
        
        # Fast existing server check (max 1 second)
        print("🔍 Checking for existing server...")
        existing_port = self.check_existing_server()
        
        if existing_port:
            print(f"✅ Using existing server on port {existing_port}")
            self.port = existing_port
            self.open_browser()
            
            # Quick hide and exit (no background tasks)
            time.sleep(0.5)
            self.hide_console()
            
            # Exit immediately - browser is open, no need to keep process running
            time.sleep(1)
            return 0
        
        # Start new server quickly
        print("🔧 Starting server...")
        if not self.start_server():
            print("❌ Server startup failed")
            time.sleep(2)
            return 1
        
        print(f"✅ Server ready on port {self.port}")
        
        # Quick browser opening
        print("🌐 Opening browser...")
        self.open_browser()
        
        # Hide console after browser starts
        time.sleep(1.5)
        self.hide_console()
        
        # Keep server running but allow clean exit
        try:
            # Use event to allow quick shutdown
            import threading
            shutdown_event = threading.Event()
            
            def wait_for_shutdown():
                try:
                    while not shutdown_event.is_set():
                        shutdown_event.wait(1)
                except KeyboardInterrupt:
                    shutdown_event.set()
            
            wait_for_shutdown()
            
        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()
            return 0

if __name__ == "__main__":
    app = PDFExplorerWindows()
    sys.exit(app.run())