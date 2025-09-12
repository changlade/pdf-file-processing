#!/usr/bin/env python
"""
PDF Document Explorer - Legacy macOS Version
Compatible with macOS 10.9+ (Mavericks) and very old Python versions
"""

import os
import sys
import time
import socket
import webbrowser
import threading
import signal
import platform

# Ultra-compatible imports - work with Python 2.6+
try:
    # Python 3
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    import urllib.request as urllib_request
    import urllib.error as urllib_error
    PYTHON3 = True
except ImportError:
    # Python 2
    from BaseHTTPServer import HTTPServer, SimpleHTTPRequestHandler
    import urllib2 as urllib_request
    urllib_error = urllib_request
    PYTHON3 = False

# Subprocess with maximum compatibility
try:
    import subprocess
    HAS_SUBPROCESS = True
except ImportError:
    HAS_SUBPROCESS = False

class PDFExplorerLegacy:
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
                # Ultra-compatible socket handling
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                try:
                    s.bind(('localhost', port))
                    s.close()
                    return port
                except:
                    try:
                        s.close()
                    except:
                        pass
                    continue
            except:
                continue
        return None
    
    def check_existing_server(self, start_port=8000, max_attempts=5):
        """Check if server is already running and return the port - simplified for old systems"""
        for i in range(max_attempts):
            port = start_port + i
            try:
                # Simple socket check only - more reliable on old systems
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)  # Short timeout
                try:
                    result = s.connect_ex(('localhost', port))
                    s.close()
                    if result == 0:
                        return port
                except:
                    try:
                        s.close()
                    except:
                        pass
            except:
                pass
        return None
    
    def start_server(self):
        """Start the HTTP server with maximum compatibility"""
        try:
            # Find available port
            self.port = self.find_available_port()
            if not self.port:
                return False
            
            # Set working directory
            try:
                os.chdir(self.base_dir)
            except:
                pass
            
            # Very simple file check
            web_dir = os.path.join(self.base_dir, 'web')
            if not os.path.exists(web_dir):
                # Try parent directory
                web_dir = os.path.join(self.base_dir, '..', 'web')
                if not os.path.exists(web_dir):
                    return False
            
            # Create server with maximum compatibility
            server_address = ('localhost', self.port)
            self.server = HTTPServer(server_address, SimpleHTTPRequestHandler)
            
            # Start server thread - compatible with old Python
            self.server_thread = threading.Thread(target=self._run_server)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            # Give server time to start
            time.sleep(0.5)
            
            return True
        except:
            return False
    
    def _run_server(self):
        """Run the server with error handling"""
        try:
            self.server.serve_forever()
        except:
            pass
    
    def open_browser(self):
        """Open the web browser with maximum compatibility"""
        url = "http://localhost:{0}/web/".format(self.port)
        
        def delayed_open():
            try:
                # Try multiple methods for opening browser
                success = False
                
                # Method 1: Try 'open' command (macOS)
                if not success and HAS_SUBPROCESS:
                    try:
                        if hasattr(subprocess, 'check_call'):
                            subprocess.check_call(['open', url])
                            success = True
                    except:
                        pass
                
                # Method 2: Try older os.system (very compatible)
                if not success:
                    try:
                        os.system('open "{0}"'.format(url))
                        success = True
                    except:
                        pass
                
                # Method 3: Python webbrowser module
                if not success:
                    try:
                        webbrowser.open(url, new=2)
                        success = True
                    except:
                        pass
                
                return success
            except:
                return False
        
        # Use timer with longer delay for old systems
        timer = threading.Timer(1.0, delayed_open)
        timer.start()
        
        return True
    
    def show_error_dialog(self, message):
        """Show error dialog with maximum compatibility"""
        try:
            # Try osascript first
            if HAS_SUBPROCESS:
                try:
                    script = 'display dialog "{0}" with title "PDF Document Explorer" buttons {{"OK"}} default button "OK" with icon stop'.format(message)
                    if hasattr(subprocess, 'check_call'):
                        subprocess.check_call(['osascript', '-e', script])
                        return
                except:
                    pass
            
            # Fallback to os.system
            try:
                script = 'display dialog "{0}" with title "PDF Document Explorer" buttons {{"OK"}} default button "OK" with icon stop'.format(message)
                os.system('osascript -e \'{0}\''.format(script))
                return
            except:
                pass
            
            # Last resort: print to console
            print("ERROR: {0}".format(message))
        except:
            pass
    
    def cleanup(self):
        """Clean up server resources"""
        try:
            if self.server:
                self.server.shutdown()
                self.server.server_close()
        except:
            pass
    
    def run(self):
        """Main application entry point - maximum compatibility"""
        try:
            # Check for existing server
            existing_port = self.check_existing_server()
            
            if existing_port:
                self.port = existing_port
                self.open_browser()
                # Exit quickly to avoid background processes
                time.sleep(2)
                return 0
            
            # Start new server
            if not self.start_server():
                self.show_error_dialog("Failed to start the application.")
                return 1
            
            # Open browser
            self.open_browser()
            
            # Keep server running with simple loop
            try:
                # Use a simple counter instead of infinite loop
                for i in range(3600):  # Run for 1 hour max
                    time.sleep(1)
                    if not self.server_thread.is_alive():
                        break
            except KeyboardInterrupt:
                pass
            except:
                pass
            
            self.cleanup()
            return 0
            
        except Exception as e:
            try:
                self.show_error_dialog("Application error: {0}".format(str(e)))
            except:
                pass
            return 1

if __name__ == "__main__":
    app = PDFExplorerLegacy()
    try:
        sys.exit(app.run())
    except:
        sys.exit(1)
