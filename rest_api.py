"""
REST API SERVER
===============
Complete REST API with CRUD operations for users.
Built using Flask patterns from Ramah API server.

Features:
- Health check endpoint
- Full CRUD operations for users (Create, Read, Update, Delete)
- API key authentication
- Error handling
- Request logging
- CORS support
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import time
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime

# ============================================================================
# INITIALIZATION
# ============================================================================

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# In-memory database (replace with real database in production)
users_db: Dict[str, Dict[str, Any]] = {}

# Simple API key system (for production, use proper auth)
VALID_API_KEYS = {
    "demo_key": "Demo Access",
    "claude_key": "Claude AI Access",
    "test_key": "Test Access",
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


def log_request(endpoint: str, method: str, params: Dict, response_time: float, status: int):
    """Log API usage"""
    key_name = getattr(request, 'api_key_name', 'Anonymous')
    print(f"[{key_name}] {method} {endpoint} - {params} - {status} - {response_time:.3f}s")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def validate_user_data(data: Dict[str, Any], required_fields: List[str] = None) -> Optional[str]:
    """
    Validate user data structure.

    Returns:
        Error message if validation fails, None if valid
    """
    if not data:
        return "Request body required"

    if required_fields:
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return f"Missing required fields: {', '.join(missing_fields)}"

    # Validate email format if provided
    if 'email' in data:
        email = data['email']
        if not email or '@' not in email:
            return "Invalid email format"

    # Validate age if provided
    if 'age' in data:
        try:
            age = int(data['age'])
            if age < 0 or age > 150:
                return "Age must be between 0 and 150"
        except (ValueError, TypeError):
            return "Age must be a valid integer"

    return None


def create_user(name: str, email: str, age: int = None) -> Dict[str, Any]:
    """Create a new user and add to database"""
    user_id = str(uuid.uuid4())
    user = {
        'id': user_id,
        'name': name,
        'email': email,
        'age': age,
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }
    users_db[user_id] = user
    return user


def get_user(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user by ID"""
    return users_db.get(user_id)


def update_user(user_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update existing user"""
    user = users_db.get(user_id)
    if not user:
        return None

    # Update allowed fields
    allowed_fields = ['name', 'email', 'age']
    for field in allowed_fields:
        if field in data:
            user[field] = data[field]

    user['updated_at'] = datetime.utcnow().isoformat()
    users_db[user_id] = user
    return user


def delete_user(user_id: str) -> bool:
    """Delete user by ID"""
    if user_id in users_db:
        del users_db[user_id]
        return True
    return False


def list_users(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    """List all users with pagination"""
    all_users = list(users_db.values())
    return all_users[offset:offset + limit]


# ============================================================================
# HEALTH & INFO ENDPOINTS
# ============================================================================

@app.route('/')
def index():
    """API documentation"""
    return jsonify({
        'name': 'REST API Server',
        'version': '1.0',
        'description': 'Complete REST API with CRUD operations for users',
        'endpoints': {
            'health': 'GET /health',
            'list_users': 'GET /users',
            'create_user': 'POST /users',
            'get_user': 'GET /users/<id>',
            'update_user': 'PUT /users/<id>',
            'delete_user': 'DELETE /users/<id>'
        },
        'authentication': 'Include X-API-Key header or ?api_key= parameter',
        'demo_keys': ['demo_key', 'claude_key', 'test_key']
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'users_count': len(users_db),
        'service': 'REST API',
        'version': '1.0'
    })


# ============================================================================
# USER CRUD ENDPOINTS
# ============================================================================

@app.route('/users', methods=['GET'])
@require_api_key
def get_users():
    """
    List all users with pagination.

    Query params:
        limit: Maximum number of users to return (default: 100)
        offset: Number of users to skip (default: 0)

    Example:
        GET /users?limit=10&offset=0&api_key=demo_key
    """
    start_time = time.time()

    try:
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))

        # Validate pagination params
        if limit < 1 or limit > 1000:
            return jsonify({'error': 'Limit must be between 1 and 1000'}), 400
        if offset < 0:
            return jsonify({'error': 'Offset must be non-negative'}), 400

        users = list_users(limit, offset)

        response = {
            'status': 'success',
            'count': len(users),
            'total': len(users_db),
            'limit': limit,
            'offset': offset,
            'users': users
        }

        log_request('/users', 'GET', {'limit': limit, 'offset': offset},
                   time.time() - start_time, 200)

        return jsonify(response), 200

    except ValueError as e:
        return jsonify({'error': f'Invalid parameter: {str(e)}'}), 400


@app.route('/users', methods=['POST'])
@require_api_key
def create_user_endpoint():
    """
    Create a new user.

    POST body:
        {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30  // optional
        }

    Example:
        POST /users
        Headers: X-API-Key: demo_key
        Body: {"name": "John Doe", "email": "john@example.com", "age": 30}
    """
    start_time = time.time()

    try:
        data = request.get_json()

        # Validate request data
        error = validate_user_data(data, required_fields=['name', 'email'])
        if error:
            log_request('/users', 'POST', {}, time.time() - start_time, 400)
            return jsonify({'error': error}), 400

        # Create user
        user = create_user(
            name=data['name'],
            email=data['email'],
            age=data.get('age')
        )

        log_request('/users', 'POST', {'email': data['email']},
                   time.time() - start_time, 201)

        return jsonify({
            'status': 'success',
            'message': 'User created successfully',
            'user': user
        }), 201

    except Exception as e:
        log_request('/users', 'POST', {}, time.time() - start_time, 500)
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/users/<user_id>', methods=['GET'])
@require_api_key
def get_user_endpoint(user_id: str):
    """
    Get a specific user by ID.

    Example:
        GET /users/123e4567-e89b-12d3-a456-426614174000?api_key=demo_key
    """
    start_time = time.time()

    user = get_user(user_id)

    if not user:
        log_request(f'/users/{user_id}', 'GET', {}, time.time() - start_time, 404)
        return jsonify({
            'error': 'User not found',
            'user_id': user_id
        }), 404

    log_request(f'/users/{user_id}', 'GET', {}, time.time() - start_time, 200)

    return jsonify({
        'status': 'success',
        'user': user
    }), 200


@app.route('/users/<user_id>', methods=['PUT'])
@require_api_key
def update_user_endpoint(user_id: str):
    """
    Update an existing user.

    PUT body:
        {
            "name": "Jane Doe",      // optional
            "email": "jane@example.com",  // optional
            "age": 31                // optional
        }

    Example:
        PUT /users/123e4567-e89b-12d3-a456-426614174000
        Headers: X-API-Key: demo_key
        Body: {"name": "Jane Doe", "age": 31}
    """
    start_time = time.time()

    try:
        data = request.get_json()

        # Validate request data
        error = validate_user_data(data)
        if error:
            log_request(f'/users/{user_id}', 'PUT', {}, time.time() - start_time, 400)
            return jsonify({'error': error}), 400

        # Check if user exists and update
        user = update_user(user_id, data)

        if not user:
            log_request(f'/users/{user_id}', 'PUT', {}, time.time() - start_time, 404)
            return jsonify({
                'error': 'User not found',
                'user_id': user_id
            }), 404

        log_request(f'/users/{user_id}', 'PUT', data, time.time() - start_time, 200)

        return jsonify({
            'status': 'success',
            'message': 'User updated successfully',
            'user': user
        }), 200

    except Exception as e:
        log_request(f'/users/{user_id}', 'PUT', {}, time.time() - start_time, 500)
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/users/<user_id>', methods=['DELETE'])
@require_api_key
def delete_user_endpoint(user_id: str):
    """
    Delete a user by ID.

    Example:
        DELETE /users/123e4567-e89b-12d3-a456-426614174000?api_key=demo_key
    """
    start_time = time.time()

    success = delete_user(user_id)

    if not success:
        log_request(f'/users/{user_id}', 'DELETE', {}, time.time() - start_time, 404)
        return jsonify({
            'error': 'User not found',
            'user_id': user_id
        }), 404

    log_request(f'/users/{user_id}', 'DELETE', {}, time.time() - start_time, 200)

    return jsonify({
        'status': 'success',
        'message': 'User deleted successfully',
        'user_id': user_id
    }), 200


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'error': 'Endpoint not found',
        'message': str(e),
        'available_endpoints': [
            '/', '/health', '/users', '/users/<id>'
        ]
    }), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({
        'error': 'Internal server error',
        'message': str(e)
    }), 500


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({
        'error': 'Method not allowed',
        'message': str(e)
    }), 405


@app.errorhandler(400)
def bad_request(e):
    return jsonify({
        'error': 'Bad request',
        'message': str(e)
    }), 400


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    import os

    # Get port from environment (for deployment platforms)
    port = int(os.environ.get('PORT', 5000))

    # Add some sample users for testing
    create_user("Alice Johnson", "alice@example.com", 28)
    create_user("Bob Smith", "bob@example.com", 35)
    create_user("Charlie Brown", "charlie@example.com", 42)

    # Run server
    print(f"\n🚀 REST API Server starting on port {port}...")
    print(f"📖 Documentation: http://localhost:{port}/")
    print(f"💚 Health check: http://localhost:{port}/health")
    print(f"👥 Users endpoint: http://localhost:{port}/users")
    print(f"\n🔑 Demo API keys: demo_key, claude_key, test_key")
    print(f"\nExample requests:")
    print(f'  # List users')
    print(f'  curl "http://localhost:{port}/users?api_key=demo_key"')
    print(f'\n  # Create user')
    print(f'  curl -X POST "http://localhost:{port}/users?api_key=demo_key" \\')
    print(f'       -H "Content-Type: application/json" \\')
    print(f'       -d \'{{"name":"John Doe","email":"john@example.com","age":30}}\'')
    print()

    app.run(
        host='0.0.0.0',
        port=port,
        debug=False  # Set to False in production
    )
