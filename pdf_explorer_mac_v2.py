#!/usr/bin/env python3
"""
PDF Document Explorer - macOS Version with Semantic Search
Compatible with macOS 10.15+ (Catalina) and Python 3.8+
Includes Flask proxy for semantic search functionality
"""

import os
import sys
import time
import socket
import webbrowser
import threading
import signal
import platform
import subprocess
import json
import requests
from http.server import HTTPServer, SimpleHTTPRequestHandler
from flask import Flask, request, jsonify
from flask_cors import CORS

class SemanticSearchProxy:
    """Flask-based proxy for semantic search"""
    def __init__(self, port=8002):
        self.app = Flask(__name__)
        CORS(self.app)
        self.port = port
        self.server = None
        self.server_thread = None
        
        # Databricks configuration
        self.databricks_url = 'https://dbc-0619d7f5-0bda.cloud.databricks.com/serving-endpoints/icc-intelligence/invocations'
        self.databricks_token = os.getenv('DATABRICKS_TOKEN', 'your-databricks-token-here')
        
        self.setup_routes()
    
    def setup_routes(self):
        """Setup Flask routes"""
        @self.app.route('/semantic-search', methods=['POST'])
        def semantic_search():
            try:
                data = request.get_json()
                if not data or 'query' not in data:
                    return jsonify({'error': 'Query parameter is required'}), 400
                
                query = data['query'].strip()
                if not query:
                    return jsonify({'error': 'Query cannot be empty'}), 400
                
                print(f"Processing semantic search query: {query}")
                
                # Call Databricks API
                result = self.call_databricks_api(query)
                return jsonify(result)
                
            except Exception as e:
                print(f"Semantic search error: {e}")
                return jsonify({'error': f"Semantic search failed: {str(e)}"}), 500

        @self.app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({'status': 'healthy', 'service': 'semantic-search-proxy'})
    
    def call_databricks_api(self, query):
        """Call the Databricks Vector Search API"""
        request_data = {
            "dataframe_split": {
                "columns": ["query", "num_results"],
                "data": [[query, 20]]
            }
        }
        
        headers = {
            'Authorization': f'Bearer {self.databricks_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            self.databricks_url,
            headers=headers,
            json=request_data,
            timeout=30
        )
        
        if not response.ok:
            error_msg = f"Databricks API error: {response.status_code} - {response.text}"
            print(error_msg)
            raise Exception(error_msg)
        
        result = response.json()
        print(f"Databricks API responded successfully with {len(result.get('predictions', [[]])[0])} results")
        return result
    
    def start(self):
        """Start the Flask proxy server"""
        try:
            print(f"Starting semantic search proxy on port {self.port}...")
            
            # Disable Flask logging for cleaner output
            import logging
            log = logging.getLogger('werkzeug')
            log.setLevel(logging.ERROR)
            
            # Start Flask server in thread
            self.server_thread = threading.Thread(
                target=lambda: self.app.run(
                    host='127.0.0.1', 
                    port=self.port, 
                    debug=False, 
                    use_reloader=False,
                    threaded=True
                ),
                daemon=True
            )
            self.server_thread.start()
            
            # Give server time to start
            time.sleep(0.5)
            
            # Verify server is running
            try:
                test_response = requests.get(f'http://127.0.0.1:{self.port}/health', timeout=2)
                if test_response.status_code == 200:
                    print(f"✅ Semantic search proxy ready on port {self.port}")
                    return True
            except:
                pass
            
            print(f"⚠️  Semantic search proxy may not be fully ready")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start semantic search proxy: {e}")
            return False

class PDFExplorerMac:
    def __init__(self):
        self.server = None
        self.server_thread = None
        self.semantic_proxy = None
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
    
    def start_servers(self):
        """Start both the main server and semantic search proxy"""
        try:
            # Start semantic search proxy first
            print("🧠 Starting semantic search functionality...")
            self.semantic_proxy = SemanticSearchProxy(port=8002)
            proxy_started = self.semantic_proxy.start()
            
            if not proxy_started:
                print("⚠️  Semantic search may not be available")
            
            # Start main server
            print("📄 Starting main PDF server...")
            self.port = self.find_available_port()
            if not self.port:
                print("❌ Could not find an available port")
                return False
            
            # Change to the app directory
            os.chdir(self.base_dir)
            
            # Check if required files exist
            if not os.path.exists('web/index.html'):
                print("❌ Required files not found")
                return False
            
            # Create server
            server_address = ('localhost', self.port)
            self.server = HTTPServer(server_address, SimpleHTTPRequestHandler)
            
            # Start server in a separate thread
            self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.server_thread.start()
            
            print(f"✅ Main server ready on port {self.port}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start servers: {str(e)}")
            return False
    
    def open_browser(self):
        """Open the web browser"""
        url = f"http://localhost:{self.port}/web/"
        
        def delayed_open():
            try:
                print(f"🌐 Opening browser: {url}")
                # Use macOS 'open' command
                subprocess.run(['open', url], check=False, timeout=5)
                return True
            except Exception as e:
                print(f"⚠️  Browser auto-open failed: {str(e)}")
                # Fallback to webbrowser module
                try:
                    webbrowser.open(url, new=2)
                    return True
                except:
                    return False
        
        # Use threading timer for delayed browser opening
        timer = threading.Timer(1.0, delayed_open)
        timer.start()
        
        print("🔄 Browser will open automatically in 1 second...")
        return True
    
    def show_success_dialog(self):
        """Show success dialog using AppleScript"""
        url = f"http://localhost:{self.port}/web/"
        
        script = f'''
        display dialog "PDF Document Explorer is now running!

• Main interface: {url}
• Semantic search: Available
• The browser should open automatically

Click OK to continue." with title "PDF Document Explorer" buttons {{"OK"}} default button "OK" with icon note
        '''
        
        try:
            subprocess.run(['osascript', '-e', script], check=False, timeout=10)
        except:
            # Fallback to console
            print(f"""
🎉 PDF Document Explorer is now running!
🌐 URL: {url}
🧠 Semantic search: Available
🚀 Browser should open automatically
            """)
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if self.server:
                self.server.shutdown()
                self.server.server_close()
        except:
            pass
    
    def run(self):
        """Main application entry point"""
        print("🚀 Starting PDF Document Explorer with Semantic Search...")
        print("📍 Application directory:", self.base_dir)
        
        # Check for existing server first
        existing_port = self.check_existing_server()
        
        if existing_port:
            print(f"🔄 Server already running on port {existing_port}")
            self.port = existing_port
            
            # Just open browser to existing server
            print("🌐 Opening browser to existing server...")
            self.open_browser()
            
            # Show success message
            self.show_success_dialog()
            
            # Exit - no need to keep running
            print("🎉 Connected to existing server. Exiting.")
            return 0
        
        # Start new servers
        print("🔧 Starting new servers...")
        
        if not self.start_servers():
            print("❌ Failed to start servers")
            return 1
        
        print(f"✅ All servers started successfully")
        
        # Brief wait for servers to be ready
        time.sleep(1.0)
        
        # Open browser
        self.open_browser()
        
        # Show success dialog
        self.show_success_dialog()
        
        print("🔄 Servers are running... Press Ctrl+C to stop")
        
        try:
            # Keep the application running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down servers...")
            self.cleanup()
            print("✅ Servers stopped. Goodbye!")
            return 0

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🛑 Received shutdown signal...")
    sys.exit(0)

if __name__ == "__main__":
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and run the application
    app = PDFExplorerMac()
    exit_code = app.run()
    sys.exit(exit_code)
