#!/usr/bin/env python3
"""
PDF Document Explorer
Flask web application for exploring PDF documents with CAR references
"""

import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder='web', static_url_path='')
CORS(app)

@app.route('/')
def index():
    """Serve the main application"""
    return send_from_directory('web', 'index.html')

@app.route('/web/')
def web_index():
    """Serve the web interface"""
    return send_from_directory('web', 'index.html')

@app.route('/web/<path:filename>')
def web_static(filename):
    """Serve static web files"""
    return send_from_directory('web', filename)

@app.route('/data/<path:filename>')
def serve_data(filename):
    """Serve data files"""
    return send_from_directory('data', filename)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'pdf-document-explorer',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
