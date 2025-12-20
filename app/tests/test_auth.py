import pytest
from unittest.mock import patch, MagicMock

# Test 1: Verify the Login Page loads correctly (Status 200)
def test_login_page_loads(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b"Login" in response.data  # Checks if HTML contains "Login"

# Test 2: Test Successful Login (Mocking the Database)
# We patch 'app.controllers.auth_routes.UserDAO' to avoid real SQL
@patch('app.controllers.auth_routes.UserDAO') 
def test_login_success(mock_user_dao, client):
    # Setup the mock to return a fake user when get_user_by_email is called
    mock_user = MagicMock()
    mock_user.UserID = 1
    mock_user.PasswordHash = "hashed_password_123" # In real app, you'd hash this
    mock_user.Role = "Student"
    
    # Mock the DAO method
    mock_user_dao.get_user_by_email.return_value = mock_user
    
    # Mock the password check (assuming you use a helper function or check hash directly)
    # If you use check_password_hash in route, we rely on the input matching or mocking that too.
    # For simplicity, assuming your route verifies hash. 
    # NOTE: You might need to patch the hashing function if it's complex.
    
    with patch('app.controllers.auth_routes.check_password_hash', return_value=True):
        response = client.post('/auth/login', data={
            'email': 'student@test.com',
            'password': 'password123'
        }, follow_redirects=True)

        # Assert we are redirected to dashboard or see dashboard content
        assert response.status_code == 200
        # Check for a string that only appears on the dashboard
        # assert b"Welcome" in response.data 

# Test 3: Test Login Failure (Wrong Password)
@patch('app.controllers.auth_routes.UserDAO')
def test_login_failure(mock_user_dao, client):
    # Setup mock to return a user
    mock_user = MagicMock()
    mock_user.PasswordHash = "real_hash"
    
    mock_user_dao.get_user_by_email.return_value = mock_user
    
    # Force password check to return False
    with patch('app.controllers.auth_routes.check_password_hash', return_value=False):
        response = client.post('/auth/login', data={
            'email': 'student@test.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)

        # Should reload login page with error
        assert b"Invalid credentials" in response.data