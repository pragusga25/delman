import unittest
from unittest.mock import Mock, patch
from flask import Flask
from app.routes.doctor import create_doctor_blueprint
from app.services.doctor import DoctorService
from app.exts import jwt
from app.models.gender import Gender
from datetime import date, time
from app.models.doctor import Doctor
from app.exceptions import UsernameAlreadyExistsError
from app.utils import CustomJSONProvider

class TestDoctorRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        jwt.init_app(self.app)
        
        self.mock_service = Mock(spec=DoctorService)
        self.bp = create_doctor_blueprint(self.mock_service)
        self.app.register_blueprint(self.bp)
        self.app.json_provider_class = CustomJSONProvider
        self.app.json = CustomJSONProvider(self.app)
        self.client = self.app.test_client()

        self.jwt_patcher = patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
        self.jwt_patcher.start()

    def tearDown(self):
        self.jwt_patcher.stop()

    def test_create_doctor_success(self):
        mock_doctor = Mock(spec=Doctor)
        mock_doctor.id = 1
        mock_doctor.name = "Dr. John Doe"
        mock_doctor.username = "drjohndoe"
        mock_doctor.gender = Gender.MALE
        mock_doctor.birthdate = date(1980, 1, 1)
        mock_doctor.work_start_time = time(9, 0)
        mock_doctor.work_end_time = time(17, 0)

        self.mock_service.create_doctor.return_value = mock_doctor

        response = self.client.post('/doctors', json={
            'name': 'Dr. John Doe',
            'username': 'drjohndoe',
            'password': 'Password!23',
            'gender': 'male',
            'birthdate': '1980-01-01',
            'work_start_time': '09:00:00',
            'work_end_time': '17:00:00'
        })

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['result']['name'], 'Dr. John Doe')
        self.mock_service.create_doctor.assert_called_once()

    def test_create_doctor_invalid_data(self):
        response = self.client.post('/doctors', json={
            'name': 'Dr',  # Too short
            'username': 'dr@johndoe',  # Invalid characters
            'password': 'short',  # Too short
            'gender': 'invalid',  # Invalid gender
            'birthdate': '1980-13-01',  # Invalid date
            'work_start_time': '25:00:00',  # Invalid time
            'work_end_time': '17:00:00'
        })

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_doctor_username_exists(self):
        self.mock_service.create_doctor.side_effect = UsernameAlreadyExistsError('doctor', 'drjohndoe')

        response = self.client.post('/doctors', json={
            'name': 'Dr. John Doe',
            'username': 'drjohndoe',
            'password': 'Password!23',
            'gender': 'male',
            'birthdate': '1980-01-01',
            'work_start_time': '09:00:00',
            'work_end_time': '17:00:00'
        })

        self.assertEqual(response.status_code, 409)
        data = response.get_json()
        self.assertEqual(data['error']['code'], 'doctor/username-exists')
        self.assertIn('drjohndoe', data['error']['message'])

    def test_create_doctor_unknown_error(self):
        self.mock_service.create_doctor.side_effect = Exception()

        response = self.client.post('/doctors', json={
            'name': 'Dr. John Doe',
            'username': 'drjohndoe',
            'password': 'Password!23',
            'gender': 'male',
            'birthdate': '1980-01-01',
            'work_start_time': '09:00:00',
            'work_end_time': '17:00:00'
        })

        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertEqual(data['error']['code'], 'doctor/creation-failed')

    def test_get_all_doctors(self):
        mock_doctor1 = Mock(spec=Doctor)
        mock_doctor1.id = 1
        mock_doctor1.name = "Dr. John Doe"
        mock_doctor1.username = "drjohndoe1"
        mock_doctor1.gender = Gender.MALE
        mock_doctor1.birthdate = date(1980, 1, 1)
        mock_doctor1.work_start_time = time(9, 0)
        mock_doctor1.work_end_time = time(17, 0)

        mock_doctor2 = Mock(spec=Doctor)
        mock_doctor2.id = 2
        mock_doctor2.name = "Dr. Jane Doe"
        mock_doctor2.username = "drjanedoe2"
        mock_doctor2.gender = Gender.FEMALE
        mock_doctor2.birthdate = date(1985, 1, 1)
        mock_doctor2.work_start_time = time(10, 0)
        mock_doctor2.work_end_time = time(18, 0)

        mock_doctors = [mock_doctor1, mock_doctor2]
        self.mock_service.get_all_doctors.return_value = mock_doctors

        response = self.client.get('/doctors')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['result']), 2)

    def test_get_doctor_by_id_success(self):
        mock_doctor = Mock(spec=Doctor)
        mock_doctor.id = 1
        mock_doctor.name = "Dr. John Doe"
        mock_doctor.username = "drjohndoe"
        mock_doctor.gender = Gender.MALE
        mock_doctor.birthdate = date(1980, 1, 1)
        mock_doctor.work_start_time = time(9, 0)
        mock_doctor.work_end_time = time(17, 0)

        self.mock_service.get_doctor_by_id.return_value = mock_doctor

        response = self.client.get('/doctors/1')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['result']['name'], 'Dr. John Doe')

    def test_get_doctor_by_id_not_found(self):
        self.mock_service.get_doctor_by_id.return_value = None

        response = self.client.get('/doctors/999')

        self.assertEqual(response.status_code, 404)

    def test_update_doctor_success(self):
        mock_doctor = Mock(spec=Doctor)
        mock_doctor.id = 1
        mock_doctor.name = "Dr. John Updated"
        mock_doctor.username = "drjohndoe"
        mock_doctor.gender = Gender.MALE
        mock_doctor.birthdate = date(1980, 1, 1)
        mock_doctor.work_start_time = time(9, 0)
        mock_doctor.work_end_time = time(17, 0)

        self.mock_service.update_doctor.return_value = mock_doctor

        response = self.client.put('/doctors/1', json={
            'name': 'Dr. John Updated',
        })

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['result']['name'], 'Dr. John Updated')

    def test_update_doctor_validation_error(self):
        response = self.client.put('/doctors/1', json={
            'name': 'D',
            'username': 'dr'
        })

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['error']['code'], 'doctor/validation-error')

    def test_update_doctor_username_exists(self):
        self.mock_service.update_doctor.side_effect = UsernameAlreadyExistsError('doctor', 'drjohndoe')

        response = self.client.put('/doctors/1', json={
            'name': 'Dr. John Doe',
            'username': 'drjohndoe',
            'gender': 'male',
            'birthdate': '1980-01-01',
            'work_start_time': '09:00:00',
            'work_end_time': '17:00:00'
        })

        self.assertEqual(response.status_code, 409)
        data = response.get_json()
        self.assertEqual(data['error']['code'], 'doctor/username-exists')
        self.assertIn('drjohndoe', data['error']['message'])

    def test_update_doctor_unknown_error(self):
        self.mock_service.update_doctor.side_effect = Exception()

        response = self.client.put('/doctors/1', json={
            'name': 'Dr. John Doe',
            'username': 'drjohndoe',
            'gender': 'male',
            'birthdate': '1980-01-01',
            'work_start_time': '09:00:00',
            'work_end_time': '17:00:00'
        })

        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertEqual(data['error']['code'], 'doctor/update-failed')

    def test_update_doctor_not_found(self):
        self.mock_service.update_doctor.return_value = None

        response = self.client.put('/doctors/999', json={
            'name': 'Dr. John Updated',
        })

        self.assertEqual(response.status_code, 404)

    def test_delete_doctor_success(self):
        self.mock_service.delete_doctor.return_value = True

        response = self.client.delete('/doctors/1')

        self.assertEqual(response.status_code, 200)

    def test_delete_doctor_not_found(self):
        self.mock_service.delete_doctor.return_value = False

        response = self.client.delete('/doctors/999')

        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
