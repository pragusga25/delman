import unittest
from unittest.mock import Mock, patch
from flask import Flask
from app.routes.appointment import create_appointment_blueprint
from app.services.appointment import AppointmentService
from app.exts import jwt
from datetime import datetime
from app.models.appointment import Appointment, AppointmentStatus
from app.exceptions import ResourceNotFoundError, ValidationError
from app.utils import CustomJSONProvider

class TestAppointmentRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        jwt.init_app(self.app)
        
        self.mock_service = Mock(spec=AppointmentService)
        self.bp = create_appointment_blueprint(self.mock_service)
        self.app.register_blueprint(self.bp)
        self.app.json_provider_class = CustomJSONProvider
        self.app.json = CustomJSONProvider(self.app)
        self.client = self.app.test_client()

        self.jwt_patcher = patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
        self.jwt_patcher.start()

    def tearDown(self):
        self.jwt_patcher.stop()

    def test_create_appointment_success(self):
        mock_appointment = Mock(spec=Appointment)
        mock_appointment.id = 1
        mock_appointment.patient_id = 1
        mock_appointment.doctor_id = 1
        mock_appointment.datetime = datetime(2023, 6, 1, 10, 0)
        mock_appointment.status = AppointmentStatus.IN_QUEUE
        mock_appointment.diagnose = None
        mock_appointment.notes = None

        self.mock_service.create_appointment.return_value = mock_appointment

        response = self.client.post('/appointments', json={
            'patient_id': 1,
            'doctor_id': 1,
            'datetime': '2023-06-01T10:00:00'
        })

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['result']['patient_id'], 1)
        self.mock_service.create_appointment.assert_called_once()

    def test_create_appointment_invalid_data(self):
        response = self.client.post('/appointments', json={
            'patient_id': 'invalid',
            'doctor_id': None,
            'datetime': '2023-06-01'
        })

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_appointment_resource_not_found(self):
        self.mock_service.create_appointment.side_effect = ResourceNotFoundError('Patient not found', 'appointment/patient-not-found')

        response = self.client.post('/appointments', json={
            'patient_id': 999,
            'doctor_id': 1,
            'datetime': '2023-06-01T10:00:00'
        })

        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data['error']['code'], 'appointment/patient-not-found')

    def test_create_appointment_validation_error(self):
        self.mock_service.create_appointment.side_effect = ValidationError('Appointment time is outside of doctor\'s working hours')

        response = self.client.post('/appointments', json={
            'patient_id': 1,
            'doctor_id': 1,
            'datetime': '2023-06-01T08:00:00'
        })

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['error']['code'], 'appointment/validation-error')

    def test_create_appointment_unknown_error(self):
        self.mock_service.create_appointment.side_effect = Exception()

        response = self.client.post('/appointments', json={
            'patient_id': 1,
            'doctor_id': 1,
            'datetime': '2023-06-01T10:00:00'
        })

        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertEqual(data['error']['code'], 'appointment/creation-failed')

    def test_get_all_appointments(self):
        mock_appointment1 = Mock(spec=Appointment)
        mock_appointment1.id = 1
        mock_appointment1.patient_id = 1
        mock_appointment1.doctor_id = 1
        mock_appointment1.datetime = datetime(2023, 6, 1, 10, 0)
        mock_appointment1.status = AppointmentStatus.IN_QUEUE
        mock_appointment1.diagnose = None
        mock_appointment1.notes = None

        mock_appointment2 = Mock(spec=Appointment)
        mock_appointment2.id = 2
        mock_appointment2.patient_id = 2
        mock_appointment2.doctor_id = 2
        mock_appointment2.datetime = datetime(2023, 6, 2, 11, 0)
        mock_appointment2.status = AppointmentStatus.DONE
        mock_appointment2.diagnose = "Diagnosis"
        mock_appointment2.notes = "Notes"

        mock_appointments = [mock_appointment1, mock_appointment2]
        self.mock_service.filter_appointments.return_value = mock_appointments

        response = self.client.get('/appointments')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['result']), 2)

    def test_get_appointment_by_id_success(self):
        mock_patient = Mock()
        mock_patient.id = 1
        mock_patient.name = 'John Doe'
        mock_patient.birthdate = datetime(1980, 1, 1)
        mock_patient.gender = "male"

        mock_doctor = Mock()
        mock_doctor.id = 1
        mock_doctor.name = 'Dr. Jane Doe'
        mock_doctor.birthdate = datetime(1980, 1, 1)
        mock_doctor.gender = "male"
    
        mock_appointment = Mock(spec=Appointment)
        mock_appointment.id = 1
        mock_appointment.datetime = datetime(2023, 6, 1, 10, 0)
        mock_appointment.status = AppointmentStatus.IN_QUEUE
        mock_appointment.diagnose = None
        mock_appointment.notes = None
        mock_appointment.patient = mock_patient
        mock_appointment.doctor = mock_doctor

        self.mock_service.get_appointment_by_id.return_value = mock_appointment

        response = self.client.get('/appointments/1')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['result']['patient']['id'], 1)

    def test_get_appointment_by_id_not_found(self):
        self.mock_service.get_appointment_by_id.return_value = None

        response = self.client.get('/appointments/999')

        self.assertEqual(response.status_code, 404)

    def test_update_appointment_success(self):
        mock_appointment = Mock(spec=Appointment)
        mock_appointment.id = 1
        mock_appointment.patient_id = 1
        mock_appointment.doctor_id = 1
        mock_appointment.datetime = datetime(2023, 6, 1, 10, 0)
        mock_appointment.status = AppointmentStatus.DONE
        mock_appointment.diagnose = "Updated Diagnosis"
        mock_appointment.notes = "Updated Notes"

        self.mock_service.update_appointment.return_value = mock_appointment

        response = self.client.put('/appointments/1', json={
            'status': 'DONE',
            'diagnose': 'Updated Diagnosis',
            'notes': 'Updated Notes'
        })

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['result']['diagnose'], 'Updated Diagnosis')

    def test_update_appointment_pydantic_validation_error(self):
        response = self.client.put('/appointments/1', json={
            'status': 'INVALID_STATUS'
        })

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['error']['code'], 'appointment/validation-error')

    def test_update_appointment_resource_not_found(self):
        self.mock_service.update_appointment.side_effect = ResourceNotFoundError('Doctor not found', 'appointment/doctor-not-found')

        response = self.client.put('/appointments/1', json={
            'doctor_id': 999
        })

        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data['error']['code'], 'appointment/doctor-not-found')

    def test_update_appointment_validation_error(self):
        self.mock_service.update_appointment.side_effect = ValidationError('Appointment time is outside of doctor\'s working hours')

        response = self.client.put('/appointments/1', json={
            'datetime': '2023-06-01T08:00:00'
        })

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['error']['code'], 'appointment/validation-error')

    def test_update_appointment_unknown_error(self):
        self.mock_service.update_appointment.side_effect = Exception()

        response = self.client.put('/appointments/1', json={
            'status': 'DONE'
        })

        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertEqual(data['error']['code'], 'appointment/update-failed')

    def test_update_appointment_not_found(self):
        self.mock_service.update_appointment.return_value = None

        response = self.client.put('/appointments/999', json={
            'status': 'DONE'
        })

        self.assertEqual(response.status_code, 404)

    def test_delete_appointment_success(self):
        self.mock_service.delete_appointment.return_value = True

        response = self.client.delete('/appointments/1')

        self.assertEqual(response.status_code, 200)

    def test_delete_appointment_not_found(self):
        self.mock_service.delete_appointment.return_value = False

        response = self.client.delete('/appointments/999')

        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
