# REST API Server

Complete REST API with CRUD operations for user management, built using Flask patterns from the Ramah API server.

## Features

✅ **Health Check Endpoint** - Monitor API status
✅ **Full CRUD Operations** - Create, Read, Update, Delete users
✅ **API Key Authentication** - Secure access control
✅ **Error Handling** - Comprehensive error responses
✅ **Request Logging** - Performance tracking
✅ **CORS Support** - Cross-origin requests enabled
✅ **Validation** - Input validation for all endpoints
✅ **Comprehensive Tests** - Full test coverage with pytest

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python rest_api.py
```

The server will start on `http://localhost:5000` (or the port specified in `PORT` environment variable).

### Running Tests

```bash
# Run all tests
pytest test_rest_api.py -v

# Run with coverage report
pytest test_rest_api.py -v --cov=rest_api --cov-report=html

# Run specific test class
pytest test_rest_api.py::TestCreateUser -v
```

## API Documentation

### Authentication

All endpoints (except `/` and `/health`) require authentication via API key.

**Methods:**
- **Header**: `X-API-Key: your_api_key`
- **Query Parameter**: `?api_key=your_api_key`

**Available API Keys:**
- `demo_key` - Demo Access
- `claude_key` - Claude AI Access
- `test_key` - Test Access

### Endpoints

#### 1. API Information
**GET /**

Returns API documentation and available endpoints.

**Response:**
```json
{
  "name": "REST API Server",
  "version": "1.0",
  "description": "Complete REST API with CRUD operations for users",
  "endpoints": {
    "health": "GET /health",
    "list_users": "GET /users",
    "create_user": "POST /users",
    "get_user": "GET /users/<id>",
    "update_user": "PUT /users/<id>",
    "delete_user": "DELETE /users/<id>"
  },
  "authentication": "Include X-API-Key header or ?api_key= parameter",
  "demo_keys": ["demo_key", "claude_key", "test_key"]
}
```

---

#### 2. Health Check
**GET /health**

Check API health status and get basic statistics.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-22T10:30:00.000000",
  "users_count": 3,
  "service": "REST API",
  "version": "1.0"
}
```

---

#### 3. List Users
**GET /users**

Get a list of all users with pagination support.

**Authentication Required:** Yes

**Query Parameters:**
- `limit` (optional) - Maximum users to return (1-1000, default: 100)
- `offset` (optional) - Number of users to skip (default: 0)

**Example Request:**
```bash
curl "http://localhost:5000/users?limit=10&offset=0&api_key=demo_key"
```

**Response:**
```json
{
  "status": "success",
  "count": 3,
  "total": 3,
  "limit": 10,
  "offset": 0,
  "users": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "Alice Johnson",
      "email": "alice@example.com",
      "age": 28,
      "created_at": "2025-11-22T10:00:00.000000",
      "updated_at": "2025-11-22T10:00:00.000000"
    }
  ]
}
```

---

#### 4. Create User
**POST /users**

Create a new user.

**Authentication Required:** Yes

**Request Body:**
```json
{
  "name": "John Doe",      // required
  "email": "john@example.com",  // required
  "age": 30                // optional
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:5000/users?api_key=demo_key" \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","age":30}'
```

**Response (201 Created):**
```json
{
  "status": "success",
  "message": "User created successfully",
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "created_at": "2025-11-22T10:30:00.000000",
    "updated_at": "2025-11-22T10:30:00.000000"
  }
}
```

**Validation Rules:**
- `name` - Required, non-empty string
- `email` - Required, must contain '@' symbol
- `age` - Optional, must be integer between 0-150

---

#### 5. Get User
**GET /users/{user_id}**

Get a specific user by ID.

**Authentication Required:** Yes

**Example Request:**
```bash
curl "http://localhost:5000/users/123e4567-e89b-12d3-a456-426614174000?api_key=demo_key"
```

**Response (200 OK):**
```json
{
  "status": "success",
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "created_at": "2025-11-22T10:30:00.000000",
    "updated_at": "2025-11-22T10:30:00.000000"
  }
}
```

**Error Response (404 Not Found):**
```json
{
  "error": "User not found",
  "user_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

---

#### 6. Update User
**PUT /users/{user_id}**

Update an existing user. All fields are optional.

**Authentication Required:** Yes

**Request Body:**
```json
{
  "name": "Jane Doe",      // optional
  "email": "jane@example.com",  // optional
  "age": 31                // optional
}
```

**Example Request:**
```bash
curl -X PUT "http://localhost:5000/users/123e4567-e89b-12d3-a456-426614174000?api_key=demo_key" \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe","age":31}'
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "User updated successfully",
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Jane Doe",
    "email": "john@example.com",
    "age": 31,
    "created_at": "2025-11-22T10:30:00.000000",
    "updated_at": "2025-11-22T11:00:00.000000"
  }
}
```

---

#### 7. Delete User
**DELETE /users/{user_id}**

Delete a user by ID.

**Authentication Required:** Yes

**Example Request:**
```bash
curl -X DELETE "http://localhost:5000/users/123e4567-e89b-12d3-a456-426614174000?api_key=demo_key"
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "User deleted successfully",
  "user_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

**Error Response (404 Not Found):**
```json
{
  "error": "User not found",
  "user_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

---

## Error Handling

The API uses standard HTTP status codes and returns JSON error responses.

### Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (missing API key) |
| 403 | Forbidden (invalid API key) |
| 404 | Not Found |
| 405 | Method Not Allowed |
| 500 | Internal Server Error |

### Error Response Format

```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

### Common Errors

**Missing API Key (401):**
```json
{
  "error": "API key required",
  "message": "Include X-API-Key header or ?api_key= parameter"
}
```

**Invalid API Key (403):**
```json
{
  "error": "Invalid API key"
}
```

**Validation Error (400):**
```json
{
  "error": "Missing required fields: name, email"
}
```

**User Not Found (404):**
```json
{
  "error": "User not found",
  "user_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

---

## Flask Patterns Used

This API follows established Flask patterns from the Ramah API server:

### 1. Authentication Middleware
```python
@require_api_key
def protected_endpoint():
    # Only accessible with valid API key
    pass
```

### 2. Error Handlers
```python
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404
```

### 3. Request Logging
```python
def log_request(endpoint, method, params, response_time, status):
    print(f"[{method}] {endpoint} - {status} - {response_time:.3f}s")
```

### 4. Validation
```python
def validate_user_data(data, required_fields):
    # Validate input data
    return error_message or None
```

### 5. JSON Responses
```python
return jsonify({'status': 'success', 'data': data}), 200
```

---

## Testing

The API includes comprehensive tests covering:

- ✅ Health check endpoints
- ✅ Authentication (valid/invalid API keys)
- ✅ User creation (success/validation errors)
- ✅ User listing (pagination, empty database)
- ✅ User retrieval (success/not found)
- ✅ User updates (partial/full updates)
- ✅ User deletion
- ✅ Error handlers (404, 405, 400, 500)
- ✅ Helper functions
- ✅ Integration workflows

**Test Coverage:**
```bash
pytest test_rest_api.py -v --cov=rest_api
```

**Example Test Output:**
```
test_rest_api.py::TestHealthEndpoints::test_index_endpoint PASSED
test_rest_api.py::TestHealthEndpoints::test_health_endpoint PASSED
test_rest_api.py::TestAuthentication::test_missing_api_key PASSED
test_rest_api.py::TestCreateUser::test_create_user_success PASSED
...
==================== 50 passed in 0.85s ====================
```

---

## Database

Currently uses an **in-memory dictionary** for storage (data is lost on restart).

**For production**, replace with a real database:

### Option 1: SQLite
```python
import sqlite3

# Connection
conn = sqlite3.connect('users.db')
```

### Option 2: PostgreSQL
```python
import psycopg2

# Connection
conn = psycopg2.connect(
    host="localhost",
    database="rest_api",
    user="postgres",
    password="password"
)
```

### Option 3: MongoDB
```python
from pymongo import MongoClient

# Connection
client = MongoClient('mongodb://localhost:27017/')
db = client['rest_api']
users = db['users']
```

---

## Deployment

### Railway.app

1. Create new project
2. Connect GitHub repository
3. Add environment variables:
   - `PORT` (auto-set by Railway)
4. Deploy!

### Render.com

1. Create new Web Service
2. Connect repository
3. Build command: `pip install -r requirements.txt`
4. Start command: `python rest_api.py`
5. Deploy!

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY rest_api.py .

EXPOSE 5000
CMD ["python", "rest_api.py"]
```

Build and run:
```bash
docker build -t rest-api .
docker run -p 5000:5000 rest-api
```

---

## Development

### Project Structure

```
ramah-api/
├── rest_api.py           # Main API server
├── test_rest_api.py      # Comprehensive test suite
├── requirements.txt      # Dependencies
└── REST_API_README.md    # This file
```

### Adding New Endpoints

1. Define route with `@app.route()`
2. Add `@require_api_key` decorator
3. Validate input data
4. Perform operation
5. Log request
6. Return JSON response
7. Add tests in `test_rest_api.py`

**Example:**
```python
@app.route('/users/<user_id>/activate', methods=['POST'])
@require_api_key
def activate_user(user_id: str):
    start_time = time.time()

    user = get_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user['active'] = True
    log_request(f'/users/{user_id}/activate', 'POST', {},
                time.time() - start_time, 200)

    return jsonify({'status': 'success', 'user': user}), 200
```

---

## License

MIT License - See repository for details

## Support

For issues and questions:
- GitHub Issues: https://github.com/your-repo/issues
- Email: support@example.com

---

Built with ❤️ using Flask patterns from Ramah API
