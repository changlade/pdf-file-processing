#!/usr/bin/env python3
"""
PDF Document Explorer - Cloud Run Version
Flask web application with semantic search functionality
"""

import os
import json
import requests
from requests.exceptions import ReadTimeout, ConnectTimeout, Timeout
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS

app = Flask(__name__, static_folder='web', static_url_path='')
CORS(app)

# Databricks configuration - using environment variables for security
DATABRICKS_URL = os.getenv('DATABRICKS_URL', 'https://dbc-0619d7f5-0bda.cloud.databricks.com/serving-endpoints/icc-intelligence/invocations')
RAG_URL = os.getenv('RAG_URL', 'https://dbc-0619d7f5-0bda.cloud.databricks.com/serving-endpoints/icc-rag-chatbot/invocations')
DATABRICKS_TOKEN = os.getenv('DATABRICKS_TOKEN')

# Validate required environment variables
if not DATABRICKS_TOKEN:
    print("⚠️  WARNING: DATABRICKS_TOKEN environment variable not set!")
    print("   Semantic search and RAG chat will not work without a valid token.")
    DATABRICKS_TOKEN = 'missing-token'

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

@app.route('/semantic-search', methods=['POST'])
def semantic_search():
    """Handle semantic search requests"""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        query = data['query'].strip()
        if not query:
            return jsonify({'error': 'Query cannot be empty'}), 400
        
        # Check if "get all references" is requested
        get_all = data.get('get_all', False)
        num_results = 500 if get_all else 20
        
        print(f"Processing semantic search query: {query} (num_results: {num_results})")
        
        # Call Databricks API
        result = call_databricks_api(query, num_results)
        return jsonify(result)
        
    except (ReadTimeout, ConnectTimeout, Timeout) as e:
        print(f"Semantic search timeout error: {e}")
        return jsonify({
            'error': 'ENDPOINT_STARTING',
            'message': 'The search endpoint is currently starting up. This usually takes about 30 seconds. Please try again in a moment.',
            'retry_suggested': True
        }), 503
    except Exception as e:
        print(f"Semantic search error: {e}")
        return jsonify({'error': f"Semantic search failed: {str(e)}"}), 500

@app.route('/rag-chat', methods=['POST'])
def rag_chat():
    """Handle RAG chat requests"""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        query = data['query']
        num_results = data.get('num_results', [10])
        conversation_id = data.get('conversation_id', ['session_001'])
        
        print(f"Processing RAG chat query: {query}")
        
        # Call Databricks RAG API
        result = call_rag_api(query, num_results, conversation_id)
        return jsonify(result)
        
    except (ReadTimeout, ConnectTimeout, Timeout) as e:
        print(f"RAG chat timeout error: {e}")
        return jsonify({
            'error': 'ENDPOINT_STARTING',
            'message': 'The AI endpoint is currently starting up. This usually takes about 30 seconds. Please try again in a moment.',
            'retry_suggested': True
        }), 503
    except Exception as e:
        print(f"RAG chat error: {e}")
        return jsonify({'error': f"RAG chat failed: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Cloud Run"""
    return jsonify({
        'status': 'healthy',
        'service': 'pdf-document-explorer',
        'version': '1.0.0'
    })

@app.route('/ping-endpoints', methods=['POST'])
def ping_endpoints():
    """Ping both Databricks endpoints to warm them up"""
    results = {}

    # Ping semantic search endpoint
    try:
        semantic_result = ping_semantic_endpoint()
        results['semantic_search'] = {
            'status': 'success' if semantic_result else 'failed',
            'endpoint': DATABRICKS_URL
        }
    except Exception as e:
        results['semantic_search'] = {
            'status': 'failed',
            'endpoint': DATABRICKS_URL,
            'error': str(e)
        }

    # Ping RAG endpoint
    try:
        rag_result = ping_rag_endpoint()
        results['rag_chat'] = {
            'status': 'success' if rag_result else 'failed',
            'endpoint': RAG_URL
        }
    except Exception as e:
        results['rag_chat'] = {
            'status': 'failed',
            'endpoint': RAG_URL,
            'error': str(e)
        }

    return jsonify(results)

def call_databricks_api(query, num_results=20):
    """Call the Databricks Vector Search API"""
    request_data = {
        "dataframe_split": {
            "columns": ["query", "num_results"],
            "data": [[query, num_results]]
        }
    }
    
    headers = {
        'Authorization': f'Bearer {DATABRICKS_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(
            DATABRICKS_URL,
            headers=headers,
            json=request_data,
            timeout=30
        )
    except (ReadTimeout, ConnectTimeout, Timeout) as e:
        # Re-raise timeout exceptions to be caught by the route handler
        raise e
    
    if not response.ok:
        error_msg = f"Databricks API error: {response.status_code} - {response.text}"
        print(error_msg)
        raise Exception(error_msg)
    
    result = response.json()
    print(f"Databricks API responded successfully with {len(result.get('predictions', [[]])[0])} results")
    return result

def call_rag_api(query, num_results=[10], conversation_id=['session_001']):
    """Call the Databricks RAG Chatbot API"""
    # Ensure query is a list and extract first element if it's nested
    if isinstance(query, list) and len(query) > 0:
        query_text = query[0]
    else:
        query_text = str(query)
    
    # Ensure num_results and conversation_id are single values
    num_results_val = num_results[0] if isinstance(num_results, list) else num_results
    conversation_id_val = conversation_id[0] if isinstance(conversation_id, list) else conversation_id
    
    request_data = {
        "dataframe_split": {
            "columns": ["query", "num_results", "conversation_id"],
            "data": [[query_text, num_results_val, conversation_id_val]]
        }
    }
    
    headers = {
        'Authorization': f'Bearer {DATABRICKS_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(
            RAG_URL,
            headers=headers,
            json=request_data,
            timeout=30
        )
    except (ReadTimeout, ConnectTimeout, Timeout) as e:
        # Re-raise timeout exceptions to be caught by the route handler
        raise e
    
    if not response.ok:
        error_msg = f"Databricks RAG API error: {response.status_code} - {response.text}"
        print(error_msg)
        raise Exception(error_msg)
    
    result = response.json()
    print(f"Databricks RAG API responded successfully")
    return result

def ping_semantic_endpoint():
    """Send a simple ping request to the semantic search endpoint"""
    try:
        print("Pinging semantic search endpoint to warm it up...")

        # Use a simple test query to ping the endpoint
        request_data = {
            "dataframe_split": {
                "columns": ["query", "num_results"],
                "data": [["ping", 1]]
            }
        }

        headers = {
            'Authorization': f'Bearer {DATABRICKS_TOKEN}',
            'Content-Type': 'application/json'
        }

        response = requests.post(
            DATABRICKS_URL,
            headers=headers,
            json=request_data,
            timeout=60  # Longer timeout for warming up
        )

        success = response.ok
        print(f"Semantic search endpoint ping: {'SUCCESS' if success else 'FAILED'}")
        return success

    except Exception as e:
        print(f"Error pinging semantic search endpoint: {e}")
        return False

def ping_rag_endpoint():
    """Send a simple ping request to the RAG endpoint"""
    try:
        print("Pinging RAG endpoint to warm it up...")

        # Use a simple test query to ping the endpoint
        request_data = {
            "dataframe_split": {
                "columns": ["query", "num_results", "conversation_id"],
                "data": [["ping", 1, "ping_session"]]
            }
        }

        headers = {
            'Authorization': f'Bearer {DATABRICKS_TOKEN}',
            'Content-Type': 'application/json'
        }

        response = requests.post(
            RAG_URL,
            headers=headers,
            json=request_data,
            timeout=60  # Longer timeout for warming up
        )

        success = response.ok
        print(f"RAG endpoint ping: {'SUCCESS' if success else 'FAILED'}")
        return success

    except Exception as e:
        print(f"Error pinging RAG endpoint: {e}")
        return False

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
