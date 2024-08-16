import unittest
from unittest.mock import Mock, patch
from app.services.auth import AuthService
from app.models.employee import Employee, Gender
from werkzeug.security import generate_password_hash
from datetime import date

class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock()
        self.auth_service = AuthService(self.mock_repo)

    @patch('app.services.auth.create_access_token')
    @patch('app.services.auth.create_refresh_token')
    def test_login_success(self, mock_refresh_token, mock_access_token):
        # Arrange
        mock_access_token.return_value = "fake_access_token"
        mock_refresh_token.return_value = "fake_refresh_token"
        
        mock_employee = Employee(
            id=1,
            name="Test User",
            username="testuser",
            password=generate_password_hash("correctpassword"),
            gender=Gender.MALE,
            birthdate=date(1990, 1, 1)
        )
        self.mock_repo.get_by_username.return_value = mock_employee

        # Act
        result = self.auth_service.login("testuser", "correctpassword")

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result['access_token'], "fake_access_token")
        self.assertEqual(result['refresh_token'], "fake_refresh_token")
        mock_access_token.assert_called_once_with(identity=1)
        mock_refresh_token.assert_called_once_with(identity=1)
        self.mock_repo.get_by_username.assert_called_once_with("testuser")

    def test_login_invalid_username(self):
        # Arrange
        self.mock_repo.get_by_username.return_value = None

        # Act
        result = self.auth_service.login("nonexistentuser", "anypassword")

        # Assert
        self.assertIsNone(result)
        self.mock_repo.get_by_username.assert_called_once_with("nonexistentuser")

    def test_login_invalid_password(self):
        # Arrange
        mock_employee = Employee(
            id=1,
            name="Test User",
            username="testuser",
            password=generate_password_hash("correctpassword"),
            gender=Gender.MALE,
            birthdate=date(1990, 1, 1)
        )
        self.mock_repo.get_by_username.return_value = mock_employee

        # Act
        result = self.auth_service.login("testuser", "wrongpassword")

        # Assert
        self.assertIsNone(result)
        self.mock_repo.get_by_username.assert_called_once_with("testuser")

    @patch('app.services.auth.create_access_token')
    @patch('app.services.auth.create_refresh_token')
    def test_login_token_generation_error(self, mock_refresh_token, mock_access_token):
        # Arrange
        mock_access_token.side_effect = Exception("Token generation failed")
        
        mock_employee = Employee(
            id=1,
            name="Test User",
            username="testuser",
            password=generate_password_hash("correctpassword"),
            gender=Gender.MALE,
            birthdate=date(1990, 1, 1)
        )
        self.mock_repo.get_by_username.return_value = mock_employee

        # Act
        with self.assertRaises(Exception):
            self.auth_service.login("testuser", "correctpassword")

        # Assert
        mock_access_token.assert_called_once_with(identity=1)
        self.mock_repo.get_by_username.assert_called_once_with("testuser")

if __name__ == '__main__':
    unittest.main()
