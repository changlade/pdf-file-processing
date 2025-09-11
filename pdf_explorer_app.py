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
import tkinter as tk
from tkinter import messagebox
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
            # Running as compiled executable
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
        timer = threading.Timer(1.5, delayed_open)  # 1.5 second delay
        timer.start()
        
        print("🔄 Browser will open automatically in 1.5 seconds...")
        return True  # Assume success since we're using timer
    
    def show_error(self, message):
        """Show error message to user"""
        try:
            # Try to show GUI error dialog
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showerror("PDF Document Explorer - Error", message)
            root.destroy()
        except:
            # Fall back to console output
            print(f"ERROR: {message}")
    
    def show_success(self, browser_opened=True):
        """Show success message to user with manual browser open option"""
        try:
            import tkinter.ttk as ttk
            
            root = tk.Tk()
            root.title("PDF Document Explorer - Running")
            root.geometry("500x400")
            root.resizable(False, False)
            
            # Center the window
            root.update_idletasks()
            x = (root.winfo_screenwidth() // 2) - (500 // 2)
            y = (root.winfo_screenheight() // 2) - (400 // 2)
            root.geometry(f"500x400+{x}+{y}")
            
            # Main frame
            main_frame = ttk.Frame(root, padding="20")
            main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Title
            title_label = ttk.Label(main_frame, text="🚀 PDF Document Explorer", 
                                  font=("Arial", 16, "bold"))
            title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
            
            # Status
            status_text = "✅ Server is running!" if browser_opened else "⚠️ Server running, but browser didn't open automatically"
            status_label = ttk.Label(main_frame, text=status_text, font=("Arial", 12))
            status_label.grid(row=1, column=0, columnspan=2, pady=(0, 15))
            
            # URL section
            url_label = ttk.Label(main_frame, text="🌐 Application URL:", font=("Arial", 11, "bold"))
            url_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
            
            url_text = f"http://localhost:{self.port}/web/"
            url_entry = ttk.Entry(main_frame, width=50, font=("Courier", 10))
            url_entry.insert(0, url_text)
            url_entry.configure(state="readonly")
            url_entry.grid(row=3, column=0, columnspan=2, pady=(0, 15), sticky=(tk.W, tk.E))
            
            # Buttons frame
            button_frame = ttk.Frame(main_frame)
            button_frame.grid(row=4, column=0, columnspan=2, pady=(0, 15))
            
            # Copy URL button
            def copy_url():
                root.clipboard_clear()
                root.clipboard_append(url_text)
                copy_btn.configure(text="✅ Copied!")
                root.after(2000, lambda: copy_btn.configure(text="📋 Copy URL"))
            
            copy_btn = ttk.Button(button_frame, text="📋 Copy URL", command=copy_url)
            copy_btn.grid(row=0, column=0, padx=(0, 10))
            
            # Open browser button
            def manual_open():
                try:
                    # Try multiple methods for manual browser opening
                    success = False
                    
                    # Method 1: Standard webbrowser
                    try:
                        webbrowser.open(url_text, new=2)
                        success = True
                    except:
                        pass
                    
                    # Method 2: macOS open command (if on Mac)
                    if not success and platform.system() == "Darwin":
                        try:
                            import subprocess
                            result = subprocess.run(['open', url_text], capture_output=True, timeout=5)
                            success = result.returncode == 0
                        except:
                            pass
                    
                    if success:
                        open_btn.configure(text="✅ Opened!")
                        root.after(2000, lambda: open_btn.configure(text="🌐 Open Browser"))
                    else:
                        open_btn.configure(text="❌ Failed")
                        root.after(2000, lambda: open_btn.configure(text="🌐 Open Browser"))
                except:
                    open_btn.configure(text="❌ Error")
                    root.after(2000, lambda: open_btn.configure(text="🌐 Open Browser"))
            
            open_btn = ttk.Button(button_frame, text="🌐 Open Browser", command=manual_open)
            open_btn.grid(row=0, column=1)
            
            # Instructions
            instructions_text = """💡 Manual Instructions:
1. Copy the URL above (click Copy URL button)
2. Open your web browser (Safari, Chrome, Firefox, etc.)
3. Paste the URL into the address bar
4. Press Enter to load the PDF Explorer

🛑 To stop the server: Close this window"""
            
            instructions_label = ttk.Label(main_frame, text=instructions_text, 
                                         font=("Arial", 10), justify=tk.LEFT)
            instructions_label.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
            
            # Close button
            def close_app():
                if self.server:
                    self.server.shutdown()
                root.destroy()
                import sys
                sys.exit(0)
            
            close_btn = ttk.Button(main_frame, text="🛑 Stop Server & Close", command=close_app)
            close_btn.grid(row=6, column=0, columnspan=2)
            
            # Configure grid weights
            root.columnconfigure(0, weight=1)
            root.rowconfigure(0, weight=1)
            main_frame.columnconfigure(0, weight=1)
            main_frame.columnconfigure(1, weight=1)
            
            # Handle window close
            root.protocol("WM_DELETE_WINDOW", close_app)
            
            root.mainloop()
            
        except Exception as e:
            # Fallback to simple dialog
            try:
                root = tk.Tk()
                root.withdraw()
                message = f"""PDF Document Explorer is running!
                
🌐 URL: http://localhost:{self.port}/web/

Please copy this URL and open it in your browser.
                
To stop: Close this dialog or press Ctrl+C"""
                messagebox.showinfo("PDF Document Explorer", message)
                root.destroy()
            except:
                # Final fallback to console
                print(f"PDF Document Explorer is running at: http://localhost:{self.port}/web/")
                print("Please open this URL in your browser")
                print("Press Ctrl+C to stop the server")
    
    def run(self):
        """Main application entry point"""
        print("🚀 Starting PDF Document Explorer...")
        print("📍 Application directory:", self.base_dir)
        
        # Start the server
        if not self.start_server():
            return 1
        
        print(f"✅ Server started successfully on port {self.port}")
        
        # Wait a moment for server to be ready
        time.sleep(2)
        
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
