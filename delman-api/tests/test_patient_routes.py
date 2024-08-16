import unittest
from unittest.mock import Mock, patch
from flask import Flask
from app.routes.patient import create_patient_blueprint
from app.services.patient import PatientService
from app.exts import jwt
from app.models.gender import Gender
from datetime import date
from app.models.patient import Patient
from app.exceptions import DuplicateResourceError
from app.utils import CustomJSONProvider

class TestPatientRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        jwt.init_app(self.app)
        
        self.mock_service = Mock(spec=PatientService)
        self.bp = create_patient_blueprint(self.mock_service)
        self.app.register_blueprint(self.bp)
        self.app.json_provider_class = CustomJSONProvider
        self.app.json = CustomJSONProvider(self.app)
        self.client = self.app.test_client()

        self.jwt_patcher = patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
        self.jwt_patcher.start()

    def tearDown(self):
        self.jwt_patcher.stop()

    def test_create_patient_success(self):
        mock_patient = Mock(spec=Patient)
        mock_patient.id = 1
        mock_patient.name = "John Doe"
        mock_patient.gender = Gender.MALE
        mock_patient.birthdate = date(1990, 1, 1)
        mock_patient.no_ktp = "1234567890123456"
        mock_patient.address = "123 Main St, City"
        mock_patient.vaccine_type = None
        mock_patient.vaccine_count = None

        self.mock_service.create_patient.return_value = mock_patient

        response = self.client.post('/patients', json={
            'name': 'John Doe',
            'gender': 'male',
            'birthdate': '1990-01-01',
            'no_ktp': '1234567890123456',
            'address': '123 Main St, City'
        })

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['result']['name'], 'John Doe')
        self.mock_service.create_patient.assert_called_once()

    def test_create_patient_invalid_data(self):
        response = self.client.post('/patients', json={
            'name': 'J',  # Too short
            'gender': 'invalid',  # Invalid gender
            'birthdate': '1990-13-01',  # Invalid date
            'no_ktp': '123',  # Too short
            'address': 'A'  # Too short
        })

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_patient_duplicate_ktp(self):
        self.mock_service.create_patient.side_effect = DuplicateResourceError("A patient with this KTP number already exists.")

        response = self.client.post('/patients', json={
            'name': 'John Doe',
            'gender': 'male',
            'birthdate': '1990-01-01',
            'no_ktp': '1234567890123456',
            'address': '123 Main St, City'
        })

        self.assertEqual(response.status_code, 409)
        data = response.get_json()
        self.assertEqual(data['error']['code'], 'patient/duplicate')

    def test_create_patient_unknown_error(self):
        self.mock_service.create_patient.side_effect = Exception()

        response = self.client.post('/patients', json={
            'name': 'John Doe',
            'gender': 'male',
            'birthdate': '1990-01-01',
            'no_ktp': '1234567890123456',
            'address': '123 Main St, City'
        })

        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertEqual(data['error']['code'], 'patient/creation-failed')

    def test_get_all_patients(self):
        mock_patient1 = Mock(spec=Patient)
        mock_patient1.id = 1
        mock_patient1.name = "John Doe"
        mock_patient1.gender = Gender.MALE
        mock_patient1.birthdate = date(1990, 1, 1)
        mock_patient1.no_ktp = "1234567890123456"
        mock_patient1.address = "123 Main St, City"
        mock_patient1.vaccine_type = None
        mock_patient1.vaccine_count = None

        mock_patient2 = Mock(spec=Patient)
        mock_patient2.id = 2
        mock_patient2.name = "Jane Doe"
        mock_patient2.gender = Gender.FEMALE
        mock_patient2.birthdate = date(1992, 2, 2)
        mock_patient2.no_ktp = "6543210987654321"
        mock_patient2.address = "456 Elm St, Town"
        mock_patient2.vaccine_type = "Pfizer"  
        mock_patient2.vaccine_count = 2  

        mock_patients = [mock_patient1, mock_patient2]
        self.mock_service.get_all_patients.return_value = mock_patients

        response = self.client.get('/patients')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['result']), 2)

    def test_get_patient_by_id_success(self):
        mock_patient = Mock(spec=Patient)
        mock_patient.id = 1
        mock_patient.name = "John Doe"
        mock_patient.gender = Gender.MALE
        mock_patient.birthdate = date(1990, 1, 1)
        mock_patient.no_ktp = "1234567890123456"
        mock_patient.address = "123 Main St, City"
        mock_patient.vaccine_type = "Pfizer" 
        mock_patient.vaccine_count = 2 

        self.mock_service.get_patient_by_id.return_value = mock_patient

        response = self.client.get('/patients/1')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['result']['name'], 'John Doe')

    def test_get_patient_by_id_not_found(self):
        self.mock_service.get_patient_by_id.return_value = None

        response = self.client.get('/patients/999')

        self.assertEqual(response.status_code, 404)

    def test_update_patient_success(self):
        mock_patient = Mock(spec=Patient)
        mock_patient.id = 1
        mock_patient.name = "John Updated"
        mock_patient.gender = Gender.MALE
        mock_patient.birthdate = date(1990, 1, 1)
        mock_patient.no_ktp = "1234567890123456"
        mock_patient.address = "123 Main St, City"
        mock_patient.vaccine_type = "Pfizer" 
        mock_patient.vaccine_count = 2 

        self.mock_service.update_patient.return_value = mock_patient

        response = self.client.put('/patients/1', json={
            'name': 'John Updated',
        })

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['result']['name'], 'John Updated')

    def test_update_patient_not_found(self):
        self.mock_service.update_patient.return_value = None

        response = self.client.put('/patients/999', json={
            'name': 'John Updated',
        })

        self.assertEqual(response.status_code, 404)

    def test_update_patient_validation_error(self):
        response = self.client.put('/patients/1', json={
            'no_ktp': '987'
        })

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['error']['code'], 'patient/validation-error')

    def test_update_patient_duplicate_ktp(self):
        self.mock_service.update_patient.side_effect = DuplicateResourceError("A patient with this KTP number already exists.")

        response = self.client.put('/patients/1', json={
            'no_ktp': '9876543210987654'
        })

        self.assertEqual(response.status_code, 409)
        data = response.get_json()
        self.assertEqual(data['error']['code'], 'patient/duplicate-error')

    def test_update_patient_unknown_error(self):
        self.mock_service.update_patient.side_effect = Exception()

        response = self.client.put('/patients/1', json={
            'no_ktp': '9876543210987654'
        })

        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertEqual(data['error']['code'], 'patient/update-failed')

    def test_delete_patient_success(self):
        self.mock_service.delete_patient.return_value = True

        response = self.client.delete('/patients/1')

        self.assertEqual(response.status_code, 200)

    def test_delete_patient_not_found(self):
        self.mock_service.delete_patient.return_value = False

        response = self.client.delete('/patients/999')

        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
