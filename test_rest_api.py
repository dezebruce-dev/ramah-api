"""
REST API TEST SUITE
===================
Comprehensive tests for the REST API server.

Tests:
- Health check endpoint
- User CRUD operations
- Error handling
- Authentication
- Validation
- Edge cases

Run with: pytest test_rest_api.py -v
"""

import pytest
import json
from rest_api import app, users_db, create_user, get_user, update_user, delete_user, validate_user_data


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_database():
    """Reset database before each test"""
    users_db.clear()
    yield
    users_db.clear()


@pytest.fixture
def sample_user():
    """Create a sample user for testing"""
    return create_user("Test User", "test@example.com", 25)


@pytest.fixture
def auth_headers():
    """Valid authentication headers"""
    return {'X-API-Key': 'test_key'}


@pytest.fixture
def auth_params():
    """Valid authentication query params"""
    return {'api_key': 'test_key'}


# ============================================================================
# HEALTH & INFO ENDPOINT TESTS
# ============================================================================

class TestHealthEndpoints:
    """Test health and info endpoints"""

    def test_index_endpoint(self, client):
        """Test index endpoint returns API documentation"""
        response = client.get('/')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'name' in data
        assert 'version' in data
        assert 'endpoints' in data
        assert data['name'] == 'REST API Server'

    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
        assert 'users_count' in data
        assert data['service'] == 'REST API'

    def test_health_endpoint_shows_user_count(self, client, sample_user):
        """Test health endpoint shows correct user count"""
        response = client.get('/health')
        data = json.loads(response.data)
        assert data['users_count'] == 1


# ============================================================================
# AUTHENTICATION TESTS
# ============================================================================

class TestAuthentication:
    """Test API key authentication"""

    def test_missing_api_key(self, client):
        """Test request without API key is rejected"""
        response = client.get('/users')
        assert response.status_code == 401

        data = json.loads(response.data)
        assert 'error' in data
        assert 'API key required' in data['error']

    def test_invalid_api_key(self, client):
        """Test request with invalid API key is rejected"""
        response = client.get('/users', headers={'X-API-Key': 'invalid_key'})
        assert response.status_code == 403

        data = json.loads(response.data)
        assert 'error' in data
        assert 'Invalid API key' in data['error']

    def test_valid_api_key_header(self, client, auth_headers):
        """Test request with valid API key in header"""
        response = client.get('/users', headers=auth_headers)
        assert response.status_code == 200

    def test_valid_api_key_query_param(self, client, auth_params):
        """Test request with valid API key in query param"""
        response = client.get('/users', query_string=auth_params)
        assert response.status_code == 200

    def test_multiple_api_keys_work(self, client):
        """Test that multiple API keys are valid"""
        for key in ['demo_key', 'claude_key', 'test_key']:
            response = client.get('/users', headers={'X-API-Key': key})
            assert response.status_code == 200


# ============================================================================
# USER CRUD TESTS
# ============================================================================

class TestCreateUser:
    """Test user creation"""

    def test_create_user_success(self, client, auth_headers):
        """Test successful user creation"""
        user_data = {
            'name': 'New User',
            'email': 'new@example.com',
            'age': 30
        }

        response = client.post('/users',
                              headers=auth_headers,
                              data=json.dumps(user_data),
                              content_type='application/json')

        assert response.status_code == 201

        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'user' in data
        assert data['user']['name'] == 'New User'
        assert data['user']['email'] == 'new@example.com'
        assert data['user']['age'] == 30
        assert 'id' in data['user']
        assert 'created_at' in data['user']

    def test_create_user_without_age(self, client, auth_headers):
        """Test user creation without optional age field"""
        user_data = {
            'name': 'Young User',
            'email': 'young@example.com'
        }

        response = client.post('/users',
                              headers=auth_headers,
                              data=json.dumps(user_data),
                              content_type='application/json')

        assert response.status_code == 201

        data = json.loads(response.data)
        assert data['user']['age'] is None

    def test_create_user_missing_name(self, client, auth_headers):
        """Test user creation fails without name"""
        user_data = {
            'email': 'noname@example.com'
        }

        response = client.post('/users',
                              headers=auth_headers,
                              data=json.dumps(user_data),
                              content_type='application/json')

        assert response.status_code == 400

        data = json.loads(response.data)
        assert 'error' in data
        assert 'name' in data['error'].lower()

    def test_create_user_missing_email(self, client, auth_headers):
        """Test user creation fails without email"""
        user_data = {
            'name': 'No Email'
        }

        response = client.post('/users',
                              headers=auth_headers,
                              data=json.dumps(user_data),
                              content_type='application/json')

        assert response.status_code == 400

        data = json.loads(response.data)
        assert 'error' in data
        assert 'email' in data['error'].lower()

    def test_create_user_invalid_email(self, client, auth_headers):
        """Test user creation fails with invalid email"""
        user_data = {
            'name': 'Bad Email',
            'email': 'not-an-email'
        }

        response = client.post('/users',
                              headers=auth_headers,
                              data=json.dumps(user_data),
                              content_type='application/json')

        assert response.status_code == 400

        data = json.loads(response.data)
        assert 'error' in data
        assert 'email' in data['error'].lower()

    def test_create_user_invalid_age(self, client, auth_headers):
        """Test user creation fails with invalid age"""
        user_data = {
            'name': 'Bad Age',
            'email': 'bad@example.com',
            'age': 'not-a-number'
        }

        response = client.post('/users',
                              headers=auth_headers,
                              data=json.dumps(user_data),
                              content_type='application/json')

        assert response.status_code == 400

        data = json.loads(response.data)
        assert 'error' in data
        assert 'age' in data['error'].lower()

    def test_create_user_age_out_of_range(self, client, auth_headers):
        """Test user creation fails with age out of range"""
        user_data = {
            'name': 'Old Person',
            'email': 'old@example.com',
            'age': 200
        }

        response = client.post('/users',
                              headers=auth_headers,
                              data=json.dumps(user_data),
                              content_type='application/json')

        assert response.status_code == 400

    def test_create_user_empty_body(self, client, auth_headers):
        """Test user creation fails with empty body"""
        response = client.post('/users',
                              headers=auth_headers,
                              data=json.dumps({}),
                              content_type='application/json')

        assert response.status_code == 400


class TestGetUsers:
    """Test listing users"""

    def test_get_users_empty(self, client, auth_headers):
        """Test getting users from empty database"""
        response = client.get('/users', headers=auth_headers)
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['count'] == 0
        assert data['total'] == 0
        assert len(data['users']) == 0

    def test_get_users_with_data(self, client, auth_headers, sample_user):
        """Test getting users with data"""
        response = client.get('/users', headers=auth_headers)
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['count'] == 1
        assert data['total'] == 1
        assert len(data['users']) == 1
        assert data['users'][0]['id'] == sample_user['id']

    def test_get_users_pagination(self, client, auth_headers):
        """Test user pagination"""
        # Create multiple users
        for i in range(5):
            create_user(f"User {i}", f"user{i}@example.com", 20 + i)

        # Test limit
        response = client.get('/users?limit=2', headers=auth_headers)
        data = json.loads(response.data)
        assert data['count'] == 2
        assert data['total'] == 5

        # Test offset
        response = client.get('/users?limit=2&offset=2', headers=auth_headers)
        data = json.loads(response.data)
        assert data['count'] == 2
        assert data['offset'] == 2

    def test_get_users_invalid_limit(self, client, auth_headers):
        """Test get users with invalid limit"""
        response = client.get('/users?limit=0', headers=auth_headers)
        assert response.status_code == 400

        response = client.get('/users?limit=2000', headers=auth_headers)
        assert response.status_code == 400

    def test_get_users_invalid_offset(self, client, auth_headers):
        """Test get users with invalid offset"""
        response = client.get('/users?offset=-1', headers=auth_headers)
        assert response.status_code == 400


class TestGetUser:
    """Test getting individual user"""

    def test_get_user_success(self, client, auth_headers, sample_user):
        """Test getting user by ID"""
        user_id = sample_user['id']
        response = client.get(f'/users/{user_id}', headers=auth_headers)

        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['user']['id'] == user_id
        assert data['user']['name'] == 'Test User'

    def test_get_user_not_found(self, client, auth_headers):
        """Test getting non-existent user"""
        response = client.get('/users/nonexistent-id', headers=auth_headers)

        assert response.status_code == 404

        data = json.loads(response.data)
        assert 'error' in data
        assert 'not found' in data['error'].lower()


class TestUpdateUser:
    """Test updating users"""

    def test_update_user_success(self, client, auth_headers, sample_user):
        """Test successful user update"""
        user_id = sample_user['id']
        update_data = {
            'name': 'Updated Name',
            'age': 30
        }

        response = client.put(f'/users/{user_id}',
                             headers=auth_headers,
                             data=json.dumps(update_data),
                             content_type='application/json')

        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['user']['name'] == 'Updated Name'
        assert data['user']['age'] == 30
        assert 'updated_at' in data['user']

    def test_update_user_partial(self, client, auth_headers, sample_user):
        """Test partial user update"""
        user_id = sample_user['id']
        update_data = {
            'age': 35
        }

        response = client.put(f'/users/{user_id}',
                             headers=auth_headers,
                             data=json.dumps(update_data),
                             content_type='application/json')

        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['user']['name'] == 'Test User'  # Original name
        assert data['user']['age'] == 35  # Updated age

    def test_update_user_not_found(self, client, auth_headers):
        """Test updating non-existent user"""
        update_data = {'name': 'New Name'}

        response = client.put('/users/nonexistent-id',
                             headers=auth_headers,
                             data=json.dumps(update_data),
                             content_type='application/json')

        assert response.status_code == 404

    def test_update_user_invalid_email(self, client, auth_headers, sample_user):
        """Test update with invalid email"""
        user_id = sample_user['id']
        update_data = {'email': 'invalid-email'}

        response = client.put(f'/users/{user_id}',
                             headers=auth_headers,
                             data=json.dumps(update_data),
                             content_type='application/json')

        assert response.status_code == 400

    def test_update_user_invalid_age(self, client, auth_headers, sample_user):
        """Test update with invalid age"""
        user_id = sample_user['id']
        update_data = {'age': -5}

        response = client.put(f'/users/{user_id}',
                             headers=auth_headers,
                             data=json.dumps(update_data),
                             content_type='application/json')

        assert response.status_code == 400


class TestDeleteUser:
    """Test deleting users"""

    def test_delete_user_success(self, client, auth_headers, sample_user):
        """Test successful user deletion"""
        user_id = sample_user['id']
        response = client.delete(f'/users/{user_id}', headers=auth_headers)

        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'deleted' in data['message'].lower()

        # Verify user is gone
        assert get_user(user_id) is None

    def test_delete_user_not_found(self, client, auth_headers):
        """Test deleting non-existent user"""
        response = client.delete('/users/nonexistent-id', headers=auth_headers)

        assert response.status_code == 404

        data = json.loads(response.data)
        assert 'error' in data
        assert 'not found' in data['error'].lower()


# ============================================================================
# ERROR HANDLER TESTS
# ============================================================================

class TestErrorHandlers:
    """Test error handling"""

    def test_404_not_found(self, client):
        """Test 404 error handler"""
        response = client.get('/nonexistent-endpoint')
        assert response.status_code == 404

        data = json.loads(response.data)
        assert 'error' in data
        assert 'available_endpoints' in data

    def test_405_method_not_allowed(self, client, auth_headers):
        """Test 405 error handler"""
        # Try POST on health endpoint (which only accepts GET)
        response = client.post('/health', headers=auth_headers)
        assert response.status_code == 405

        data = json.loads(response.data)
        assert 'error' in data

    def test_400_bad_request(self, client, auth_headers):
        """Test 400 error on malformed JSON"""
        response = client.post('/users',
                              headers=auth_headers,
                              data='invalid json',
                              content_type='application/json')

        # Should get 400 or 500 depending on Flask version
        assert response.status_code in [400, 500]


# ============================================================================
# HELPER FUNCTION TESTS
# ============================================================================

class TestHelperFunctions:
    """Test helper functions"""

    def test_validate_user_data_valid(self):
        """Test validation with valid data"""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'age': 30
        }
        error = validate_user_data(data, ['name', 'email'])
        assert error is None

    def test_validate_user_data_missing_fields(self):
        """Test validation with missing required fields"""
        data = {'name': 'John Doe'}
        error = validate_user_data(data, ['name', 'email'])
        assert error is not None
        assert 'email' in error.lower()

    def test_validate_user_data_invalid_email(self):
        """Test validation with invalid email"""
        data = {
            'name': 'John Doe',
            'email': 'invalid'
        }
        error = validate_user_data(data)
        assert error is not None
        assert 'email' in error.lower()

    def test_validate_user_data_invalid_age(self):
        """Test validation with invalid age"""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'age': 'not-a-number'
        }
        error = validate_user_data(data)
        assert error is not None
        assert 'age' in error.lower()

    def test_create_user_function(self):
        """Test create_user helper function"""
        user = create_user('Test', 'test@test.com', 25)
        assert user['name'] == 'Test'
        assert user['email'] == 'test@test.com'
        assert user['age'] == 25
        assert 'id' in user
        assert user['id'] in users_db

    def test_update_user_function(self):
        """Test update_user helper function"""
        user = create_user('Test', 'test@test.com', 25)
        user_id = user['id']

        updated = update_user(user_id, {'name': 'Updated'})
        assert updated['name'] == 'Updated'
        assert updated['email'] == 'test@test.com'

    def test_delete_user_function(self):
        """Test delete_user helper function"""
        user = create_user('Test', 'test@test.com', 25)
        user_id = user['id']

        success = delete_user(user_id)
        assert success is True
        assert user_id not in users_db

        # Try deleting again
        success = delete_user(user_id)
        assert success is False


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Test full workflows"""

    def test_full_crud_workflow(self, client, auth_headers):
        """Test complete CRUD workflow"""
        # Create user
        user_data = {
            'name': 'Integration Test',
            'email': 'integration@test.com',
            'age': 25
        }
        response = client.post('/users',
                              headers=auth_headers,
                              data=json.dumps(user_data),
                              content_type='application/json')
        assert response.status_code == 201
        user_id = json.loads(response.data)['user']['id']

        # Read user
        response = client.get(f'/users/{user_id}', headers=auth_headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['user']['name'] == 'Integration Test'

        # Update user
        update_data = {'name': 'Updated Integration Test'}
        response = client.put(f'/users/{user_id}',
                             headers=auth_headers,
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['user']['name'] == 'Updated Integration Test'

        # Delete user
        response = client.delete(f'/users/{user_id}', headers=auth_headers)
        assert response.status_code == 200

        # Verify deletion
        response = client.get(f'/users/{user_id}', headers=auth_headers)
        assert response.status_code == 404

    def test_multiple_users_workflow(self, client, auth_headers):
        """Test working with multiple users"""
        # Create multiple users
        for i in range(3):
            user_data = {
                'name': f'User {i}',
                'email': f'user{i}@test.com',
                'age': 20 + i
            }
            response = client.post('/users',
                                  headers=auth_headers,
                                  data=json.dumps(user_data),
                                  content_type='application/json')
            assert response.status_code == 201

        # List all users
        response = client.get('/users', headers=auth_headers)
        data = json.loads(response.data)
        assert data['total'] == 3
        assert len(data['users']) == 3

        # Test pagination
        response = client.get('/users?limit=2', headers=auth_headers)
        data = json.loads(response.data)
        assert data['count'] == 2
        assert data['total'] == 3


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
