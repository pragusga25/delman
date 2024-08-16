import unittest
from unittest.mock import Mock
from flask import Flask
from app.routes.auth import create_auth_blueprint
from app.services.auth import AuthService

class TestAuthRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.mock_service = Mock(spec=AuthService)
        self.bp = create_auth_blueprint(self.mock_service)
        self.app.register_blueprint(self.bp)
        self.client = self.app.test_client()

    def test_login_success(self):
        # Setup mock
        mock_tokens = {
            'access_token': 'fake_access_token',
            'refresh_token': 'fake_refresh_token'
        }
        self.mock_service.login.return_value = mock_tokens

        # Make request
        response = self.client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })

        # Assert
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['result'], mock_tokens)
        self.mock_service.login.assert_called_once_with('testuser', 'testpassword')

    def test_login_invalid_credentials(self):
        # Setup mock
        self.mock_service.login.return_value = None

        # Make request
        response = self.client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'wrongpassword'
        })

        # Assert
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertEqual(data['error']['code'], 'auth/invalid-credentials')

    def test_login_validation_error(self):
        # Make request with missing password
        response = self.client.post('/auth/login', json={
            'username': 'testuser'
        })

        # Assert
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['error']['code'], 'auth/validation-error')

    def test_login_internal_server_error(self):
        self.mock_service.login.side_effect = Exception()
        response = self.client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })

        # Assert
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertEqual(data['error']['code'], 'auth/login-failed')

if __name__ == '__main__':
    unittest.main()
