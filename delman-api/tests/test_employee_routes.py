import unittest
from unittest.mock import Mock, patch
from flask import Flask
from app.routes.employee import create_employee_blueprint
from app.services.employee import EmployeeService
from app.exts import jwt
from app.models.gender import Gender
from datetime import date
from app.models.employee import Employee
from app.exceptions import UsernameAlreadyExistsError

class TestEmployeeRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        jwt.init_app(self.app)
        
        self.mock_service = Mock(spec=EmployeeService)
        self.bp = create_employee_blueprint(self.mock_service)
        self.app.register_blueprint(self.bp)
        self.client = self.app.test_client()

        self.jwt_patcher = patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
        self.jwt_patcher.start()

    def tearDown(self):
        self.jwt_patcher.stop()

    def test_create_employee_success(self):
        mock_employee = Mock(spec=Employee)
        mock_employee.id = 1
        mock_employee.name = "John Doe"
        mock_employee.username = "johndoe"
        mock_employee.gender = Gender.MALE
        mock_employee.birthdate = date(1990, 1, 1)

        self.mock_service.create_employee.return_value = mock_employee

        response = self.client.post('/employees', json={
            'name': 'John Doe',
            'username': 'johndoe',
            'password': 'Password!23',
            'gender': 'male',
            'birthdate': '1990-01-01'
        })

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['result']['name'], 'John Doe')
        self.mock_service.create_employee.assert_called_once()

    def test_create_employee_invalid_data(self):
        response = self.client.post('/employees', json={
            'name': 'J',  # Too short
            'username': 'john@doe',  # Invalid characters
            'password': 'short',  # Too short
            'gender': 'invalid',  # Invalid gender
            'birthdate': '1990-13-01'  # Invalid date
        })

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_employee_username_exists(self):
        self.mock_service.create_employee.side_effect = UsernameAlreadyExistsError('employee', 'johndoe')

        response = self.client.post('/employees', json={
            'name': 'John Doe',
            'username': 'johndoe',
            'password': 'Password!23',
            'gender': 'male',
            'birthdate': '1990-01-01'
        })

        self.assertEqual(response.status_code, 409)
        data = response.get_json()
        self.assertEqual(data['error']['code'], 'employee/username-exists')
        self.assertIn('johndoe', data['error']['message'])

    def test_create_employee_unknown_error(self):
        self.mock_service.create_employee.side_effect = Exception()

        response = self.client.post('/employees', json={
            'name': 'John Doe',
            'username': 'johndoe',
            'password': 'Password!23',
            'gender': 'male',
            'birthdate': '1990-01-01'
        })

        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertEqual(data['error']['code'], 'employee/creation-failed')

    def test_get_all_employees(self):
        mock_employee1 = Mock(spec=Employee)
        mock_employee1.id = 1
        mock_employee1.name = "John Doe"
        mock_employee1.username = "johndoe1"
        mock_employee1.gender = Gender.MALE
        mock_employee1.birthdate = date(1990, 1, 1)

        mock_employee2 = Mock(spec=Employee)
        mock_employee2.id = 2
        mock_employee2.name = "John Doe"
        mock_employee2.username = "johndoe2"
        mock_employee2.gender = Gender.MALE
        mock_employee2.birthdate = date(1990, 1, 1)

        mock_employees = [mock_employee1, mock_employee2]
        self.mock_service.get_all_employees.return_value = mock_employees

        response = self.client.get('/employees')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['result']), 2)

    def test_get_employee_by_id_success(self):
        mock_employee = Mock(spec=Employee)
        mock_employee.id = 1
        mock_employee.name = "John Doe"
        mock_employee.username = "johndoe"
        mock_employee.gender = Gender.MALE
        mock_employee.birthdate = date(1990, 1, 1)

        self.mock_service.get_employee_by_id.return_value = mock_employee

        response = self.client.get('/employees/1')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['result']['name'], 'John Doe')

    def test_get_employee_by_id_not_found(self):
        self.mock_service.get_employee_by_id.return_value = None

        response = self.client.get('/employees/999')

        self.assertEqual(response.status_code, 404)

    def test_update_employee_success(self):
        mock_employee = Mock()
        mock_employee.id = 1
        mock_employee.name = "John Updated"
        mock_employee.username = "johndoe"
        mock_employee.gender = Gender.MALE
        mock_employee.birthdate = date(1990, 1, 1)

        self.mock_service.update_employee.return_value = mock_employee

        response = self.client.put('/employees/1', json={
            'name': 'John Updated',
        })

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['result']['name'], 'John Updated')

    def test_update_employee_username_exists(self):
        self.mock_service.update_employee.side_effect = UsernameAlreadyExistsError('employee', 'johndoe')

        response = self.client.put('/employees/1', json={
            'name': 'John Doe',
            'username': 'johndoe',
            'password': 'Password!23',
            'gender': 'male',
            'birthdate': '1990-01-01'
        })

        self.assertEqual(response.status_code, 409)
        data = response.get_json()
        self.assertEqual(data['error']['code'], 'employee/username-exists')
        self.assertIn('johndoe', data['error']['message'])
    
    def test_update_employee_validation_error(self):
        response = self.client.put('/employees/1', json={
            'name': 'J',
            'username': 'j'
        })

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['error']['code'], 'employee/validation-error')

    def test_update_employee_unknown_error(self):
        self.mock_service.update_employee.side_effect = Exception()

        response = self.client.put('/employees/1', json={
            'name': 'John Doe',
            'username': 'johndoe',
            'password': 'Password!23',
            'gender': 'male',
            'birthdate': '1990-01-01'
        })

        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertEqual(data['error']['code'], 'employee/update-failed')

    def test_update_employee_not_found(self):
        self.mock_service.update_employee.return_value = None

        response = self.client.put('/employees/999', json={
            'name': 'John Updated',
        })

        self.assertEqual(response.status_code, 404)

    def test_delete_employee_success(self):
        self.mock_service.delete_employee.return_value = True

        response = self.client.delete('/employees/1')

        self.assertEqual(response.status_code, 200)

    def test_delete_employee_not_found(self):
        self.mock_service.delete_employee.return_value = False

        response = self.client.delete('/employees/999')

        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
