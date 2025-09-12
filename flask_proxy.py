#!/usr/bin/env python3
"""
Simple Flask Proxy for Semantic Search
Handles Databricks API calls to avoid CORS issues
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Databricks configuration
DATABRICKS_URL = 'https://dbc-0619d7f5-0bda.cloud.databricks.com/serving-endpoints/icc-intelligence/invocations'
DATABRICKS_TOKEN = os.getenv('DATABRICKS_TOKEN', 'your-databricks-token-here')

@app.route('/semantic-search', methods=['POST'])
def semantic_search():
    """Handle semantic search requests"""
    try:
        # Get query from request
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        query = data['query'].strip()
        if not query:
            return jsonify({'error': 'Query cannot be empty'}), 400
        
        # Check if "get all references" is requested
        get_all = data.get('get_all', False)
        num_results = 500 if get_all else 20  # Use 500 for "get all", 20 for normal search
        
        print(f"🔍 Processing semantic search query: {query}")
        print(f"   📊 Request data: {data}")
        print(f"   🎯 get_all: {get_all}")
        print(f"   📈 num_results: {num_results}")
        
        # Prepare request to Databricks
        databricks_data = {
            "dataframe_split": {
                "columns": ["query", "num_results"],
                "data": [[query, num_results]]
            }
        }
        
        headers = {
            'Authorization': f'Bearer {DATABRICKS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        # Make request to Databricks
        print("Calling Databricks API...")
        response = requests.post(
            DATABRICKS_URL,
            headers=headers,
            json=databricks_data,
            timeout=30
        )
        
        if not response.ok:
            error_msg = f"Databricks API error: {response.status_code} - {response.text}"
            print(error_msg)
            return jsonify({'error': error_msg}), 500
        
        result = response.json()
        print(f"Databricks API responded successfully with {len(result.get('predictions', [[]])[0])} results")
        
        return jsonify(result)
        
    except requests.exceptions.Timeout:
        error_msg = "Request to Databricks API timed out"
        print(error_msg)
        return jsonify({'error': error_msg}), 504
    
    except requests.exceptions.RequestException as e:
        error_msg = f"Network error: {str(e)}"
        print(error_msg)
        return jsonify({'error': error_msg}), 500
    
    except Exception as e:
        error_msg = f"Internal error: {str(e)}"
        print(error_msg)
        return jsonify({'error': error_msg}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'semantic-search-proxy'})

if __name__ == '__main__':
    print("🚀 Starting Flask Semantic Search Proxy...")
    print("🌐 Proxy URL: http://localhost:8002/semantic-search")
    print("🔄 Ready to handle requests...")
    
    app.run(host='127.0.0.1', port=8002, debug=False)
