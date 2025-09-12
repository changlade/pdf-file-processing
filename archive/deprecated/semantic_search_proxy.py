#!/usr/bin/env python3
"""
Semantic Search Proxy Server
Handles Databricks API calls to avoid CORS issues in the browser
"""

import json
import os
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import sys

class SemanticSearchHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle preflight CORS requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        """Handle POST requests for semantic search"""
        # Add CORS headers
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        
        try:
            # Parse the request path
            parsed_path = urlparse(self.path)
            
            if parsed_path.path == '/semantic-search':
                result = self.handle_semantic_search()
                self.end_headers()
                
                response_data = json.dumps(result, ensure_ascii=False)
                self.wfile.write(response_data.encode('utf-8'))
            else:
                self.end_headers()
                error_response = {"error": "Endpoint not found"}
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
                
        except Exception as e:
            print(f"Error handling request: {e}")
            self.end_headers()
            error_response = {"error": f"Internal server error: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))

    def handle_semantic_search(self):
        """Handle semantic search requests"""
        try:
            # Read the request body
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                return {"error": "No request body"}
                
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            query = request_data.get('query', '').strip()
            if not query:
                return {"error": "Query parameter is required"}
            
            print(f"Processing semantic search query: {query}")
            
            # Call Databricks API
            result = self.call_databricks_api(query)
            
            print(f"Successfully processed query, returned {len(result.get('predictions', [[]])[0])} results")
            return result
            
        except Exception as e:
            print(f"Error in semantic search: {e}")
            return {"error": f"Semantic search failed: {str(e)}"}

    def call_databricks_api(self, query):
        """Call the Databricks Vector Search API"""
        url = 'https://dbc-0619d7f5-0bda.cloud.databricks.com/serving-endpoints/icc-intelligence/invocations'
        token = os.getenv('DATABRICKS_TOKEN', 'your-databricks-token-here')
        
        # Prepare the data in the format expected by Databricks
        request_data = {
            "dataframe_split": {
                "columns": ["query"],
                "data": [[query]]
            }
        }
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        print(f"Calling Databricks API with query: {query}")
        
        response = requests.post(
            url, 
            headers=headers, 
            json=request_data,
            timeout=30
        )
        
        if not response.ok:
            error_text = response.text
            print(f"Databricks API error: {response.status_code} - {error_text}")
            raise Exception(f"API request failed: {response.status_code} - {error_text}")
        
        result = response.json()
        print(f"Databricks API response received successfully")
        return result

    def log_message(self, format, *args):
        """Custom logging"""
        print(f"[PROXY] {format % args}")

def run_proxy_server(port=8001):
    """Run the proxy server"""
    try:
        server_address = ('localhost', port)
        httpd = HTTPServer(server_address, SemanticSearchHandler)
        
        print(f"🚀 Starting Semantic Search Proxy Server on port {port}")
        print(f"🌐 Proxy URL: http://localhost:{port}/semantic-search")
        print("🔄 Ready to handle semantic search requests...")
        
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down proxy server...")
        httpd.shutdown()
        httpd.server_close()
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_proxy_server()
