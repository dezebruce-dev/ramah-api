"""
RAMAH API SERVER
================
Production REST API for Ezekiel/Ramah system.
Allows external AIs (like Claude) to query code patterns and LHT diagnostics.

Deploy to: Railway.app, Render.com, or AWS Lambda
"""

import sys
sys.path.append('/mnt/project')
sys.path.append('/mnt/user-data/outputs')

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from functools import wraps
import time
import json
from typing import Dict, Any

from ezekiel_memory_engine_lht import EzekielMemoryEngine

# ============================================================================
# INITIALIZATION
# ============================================================================

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Initialize Ezekiel engine
print("Initializing Ezekiel Memory Engine...")
engine = EzekielMemoryEngine()
print("Loading Scripture...")
engine.load_scripture()
print("✓ Ramah API Server ready")

# Simple API key system (for production, use proper auth)
VALID_API_KEYS = {
    "demo_key": "Demo Access",
    "claude_key": "Claude AI Access",
    # Add more keys as needed
}

# ============================================================================
# MIDDLEWARE
# ============================================================================

def require_api_key(f):
    """Require valid API key in header or query param"""
    @wraps(f)
    def decorated(*args, **kwargs):
        # Check header first
        api_key = request.headers.get('X-API-Key')
        
        # Fall back to query param
        if not api_key:
            api_key = request.args.get('api_key')
        
        # For demo, allow no key (remove in production)
        if not api_key:
            return jsonify({
                'error': 'API key required',
                'message': 'Include X-API-Key header or ?api_key= parameter'
            }), 401
        
        if api_key not in VALID_API_KEYS:
            return jsonify({'error': 'Invalid API key'}), 403
        
        # Store key info in request for logging
        request.api_key_name = VALID_API_KEYS[api_key]
        
        return f(*args, **kwargs)
    return decorated


def log_request(endpoint: str, params: Dict, response_time: float):
    """Log API usage (in production, send to database)"""
    print(f"[{request.api_key_name}] {endpoint} - {params} - {response_time:.3f}s")


# ============================================================================
# HEALTH & INFO ENDPOINTS
# ============================================================================

@app.route('/')
def index():
    """API documentation"""
    return jsonify({
        'name': 'Ramah API',
        'version': '1.0',
        'description': 'Ezekiel semantic memory system with LHT diagnostics',
        'endpoints': {
            'retrieve': '/retrieve?coordinate=<coord>&lexicon=<lexicon>',
            'search': '/search?query=<text>&lexicon=<lexicon>',
            'analyze': '/analyze?reference=<ref>',
            'echo': '/echo?symbol=<symbol>',
            'query': '/query (POST with Ramah prompt)'
        },
        'authentication': 'Include X-API-Key header or ?api_key= parameter',
        'demo_key': 'demo_key'
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    stats = engine.get_stats()
    return jsonify({
        'status': 'healthy',
        'scripture_verses': stats['layer0_verses'],
        'tech_patterns': stats['tech_patterns'],
        'uptime': 'ok'
    })


# ============================================================================
# CORE RAMAH ENDPOINTS
# ============================================================================

@app.route('/retrieve')
@require_api_key
def retrieve():
    """
    Retrieve specific coordinate.
    
    Query params:
        coordinate: Ezekiel coordinate (e.g., L2.Q2.TECH.WEB.FLASK.API[C3])
        lexicon: KJV or TECH (optional, inferred from coordinate)
    
    Example:
        GET /retrieve?coordinate=L2.Q2.TECH.WEB.FLASK.API[C3]&api_key=demo_key
    """
    start_time = time.time()
    
    coordinate = request.args.get('coordinate')
    lexicon = request.args.get('lexicon', 'TECH')
    
    if not coordinate:
        return jsonify({'error': 'coordinate parameter required'}), 400
    
    # Build Ramah query
    ramah_query = f'RAMAH: RETRIEVE "{coordinate}"\nLEXICON: {lexicon}'
    
    result = engine.query_ramah(ramah_query)
    
    log_request('retrieve', {'coordinate': coordinate}, time.time() - start_time)
    
    return jsonify(result)


@app.route('/search')
@require_api_key
def search():
    """
    Search by keyword.
    
    Query params:
        query: Search text
        lexicon: KJV or TECH (default: both)
        limit: Max results (default: 10)
    
    Example:
        GET /search?query=flask&lexicon=TECH&api_key=demo_key
    """
    start_time = time.time()
    
    query = request.args.get('query')
    lexicon = request.args.get('lexicon')
    
    if not query:
        return jsonify({'error': 'query parameter required'}), 400
    
    # Build Ramah query
    ramah_query = f'RAMAH: SEARCH "{query}"\n'
    if lexicon:
        ramah_query += f'LEXICON: {lexicon}\n'
    ramah_query += 'RETURN: list'
    
    result = engine.query_ramah(ramah_query)
    
    log_request('search', {'query': query, 'lexicon': lexicon}, time.time() - start_time)
    
    return jsonify(result)


@app.route('/analyze')
@require_api_key
def analyze():
    """
    Run LHT TELOS-RUN diagnostic on Scripture passage.
    
    Query params:
        reference: Bible reference (e.g., "John 19:30" or "Ezekiel 37:1-5")
    
    Example:
        GET /analyze?reference=John 19:30&api_key=demo_key
    """
    start_time = time.time()
    
    reference = request.args.get('reference')
    
    if not reference:
        return jsonify({'error': 'reference parameter required'}), 400
    
    # Build Ramah query
    ramah_query = f'RAMAH: ANALYZE "{reference}"\nLEXICON: KJV'
    
    result = engine.query_ramah(ramah_query)
    
    log_request('analyze', {'reference': reference}, time.time() - start_time)
    
    return jsonify(result)


@app.route('/echo')
@require_api_key
def echo():
    """
    Trace symbol across all 7 spirals.
    
    Query params:
        symbol: Symbol name (e.g., WATER, LAMB, SPIRIT)
    
    Example:
        GET /echo?symbol=WATER&api_key=demo_key
    """
    start_time = time.time()
    
    symbol = request.args.get('symbol')
    
    if not symbol:
        return jsonify({'error': 'symbol parameter required'}), 400
    
    # Build Ramah query
    ramah_query = f'RAMAH: ECHO "{symbol}"\nRETURN: summary'
    
    result = engine.query_ramah(ramah_query)
    
    log_request('echo', {'symbol': symbol}, time.time() - start_time)
    
    return jsonify(result)


@app.route('/query', methods=['POST'])
@require_api_key
def query():
    """
    Raw Ramah query (most flexible).
    
    POST body:
        {
            "query": "RAMAH: SEARCH \"flask\"\nLEXICON: TECH\nRETURN: list"
        }
    
    Example:
        POST /query
        Headers: X-API-Key: demo_key
        Body: {"query": "RAMAH: RETRIEVE \"L2.Q2.TECH.WEB.FLASK.API[C3]\"\nLEXICON: TECH"}
    """
    start_time = time.time()
    
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({'error': 'query field required in JSON body'}), 400
    
    ramah_query = data['query']
    
    result = engine.query_ramah(ramah_query)
    
    log_request('query', {'query': ramah_query[:50]}, time.time() - start_time)
    
    return jsonify(result)


# ============================================================================
# BULK OPERATIONS
# ============================================================================

@app.route('/batch', methods=['POST'])
@require_api_key
def batch():
    """
    Batch retrieval for multiple coordinates.
    
    POST body:
        {
            "coordinates": [
                "L2.Q2.TECH.WEB.FLASK.API[C3]",
                "L1.Q1.TECH.PYTHON.FUNCTION.BASIC[C3]"
            ]
        }
    
    Returns all patterns in one response.
    """
    start_time = time.time()
    
    data = request.get_json()
    
    if not data or 'coordinates' not in data:
        return jsonify({'error': 'coordinates array required'}), 400
    
    coordinates = data['coordinates']
    results = []
    
    for coord in coordinates:
        ramah_query = f'RAMAH: RETRIEVE "{coord}"\nLEXICON: TECH'
        result = engine.query_ramah(ramah_query)
        results.append({
            'coordinate': coord,
            'result': result
        })
    
    log_request('batch', {'count': len(coordinates)}, time.time() - start_time)
    
    return jsonify({
        'status': 'success',
        'count': len(results),
        'results': results
    })


# ============================================================================
# STATS & MONITORING
# ============================================================================

@app.route('/stats')
@require_api_key
def stats():
    """Get engine statistics"""
    return jsonify(engine.get_stats())


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': [
            '/', '/health', '/retrieve', '/search', '/analyze', '/echo', '/query', '/batch', '/stats'
        ]
    }), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({
        'error': 'Internal server error',
        'message': str(e)
    }), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    import os
    
    # Get port from environment (for deployment platforms)
    port = int(os.environ.get('PORT', 5000))
    
    # Run server
    print(f"\n🚀 Ramah API Server starting on port {port}...")
    print(f"📖 Documentation: http://localhost:{port}/")
    print(f"💚 Health check: http://localhost:{port}/health")
    print(f"\n🔑 Demo API key: demo_key")
    print(f"\nExample request:")
    print(f'  curl "http://localhost:{port}/retrieve?coordinate=L2.Q2.TECH.WEB.FLASK.API[C3]&api_key=demo_key"')
    print()
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False  # Set to False in production
    )
