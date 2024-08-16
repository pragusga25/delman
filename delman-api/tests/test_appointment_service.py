import unittest
from unittest.mock import Mock, patch
from datetime import datetime, time, timedelta
from app.services.appointment import AppointmentService
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentFilter
from app.exceptions import ResourceNotFoundError, ValidationError
from sqlalchemy.exc import IntegrityError
from app.models.appointment import AppointmentStatus

class TestAppointmentService(unittest.TestCase):
    def setUp(self):
        self.appointment_repo = Mock()
        self.doctor_repo = Mock()
        self.patient_repo = Mock()
        self.service = AppointmentService(self.appointment_repo, self.doctor_repo, self.patient_repo)

    def test_create_appointment_success(self):
        appointment_data = AppointmentCreate(
            doctor_id=1,
            patient_id=1,
            datetime=datetime(2023, 1, 1, 10, 0)
        )
        mock_doctor = Mock(work_start_time=time(9, 0), work_end_time=time(17, 0))
        self.doctor_repo.get_by_id.return_value = mock_doctor
        self.patient_repo.get_by_id.return_value = Mock()
        self.appointment_repo.get_doctor_appointments.return_value = []
        self.appointment_repo.create.return_value = Mock(id=1)

        result = self.service.create_appointment(appointment_data)

        self.assertEqual(result.id, 1)
        self.appointment_repo.create.assert_called_once()

    def test_create_appointment_doctor_not_found(self):
        appointment_data = AppointmentCreate(
            doctor_id=1,
            patient_id=1,
            datetime=datetime(2023, 1, 1, 10, 0)
        )
        self.doctor_repo.get_by_id.return_value = None

        with self.assertRaises(ResourceNotFoundError):
            self.service.create_appointment(appointment_data)

    def test_create_appointment_patient_not_found(self):
        appointment_data = AppointmentCreate(
            doctor_id=1,
            patient_id=1,
            datetime=datetime(2023, 1, 1, 10, 0)
        )
        self.doctor_repo.get_by_id.return_value = Mock()
        self.patient_repo.get_by_id.return_value = None

        with self.assertRaises(ResourceNotFoundError):
            self.service.create_appointment(appointment_data)

    def test_create_appointment_outside_working_hours(self):
        appointment_data = AppointmentCreate(
            doctor_id=1,
            patient_id=1,
            datetime=datetime(2023, 1, 1, 8, 0)
        )
        mock_doctor = Mock(work_start_time=time(9, 0), work_end_time=time(17, 0))
        self.doctor_repo.get_by_id.return_value = mock_doctor
        self.patient_repo.get_by_id.return_value = Mock()

        with self.assertRaises(ValidationError):
            self.service.create_appointment(appointment_data)

    def test_create_appointment_doctor_already_booked(self):
        appointment_data = AppointmentCreate(
            doctor_id=1,
            patient_id=1,
            datetime=datetime(2023, 1, 1, 10, 0),
            status=AppointmentStatus.IN_QUEUE
        )
        mock_doctor = Mock(work_start_time=time(9, 0), work_end_time=time(17, 0))
        self.doctor_repo.get_by_id.return_value = mock_doctor
        self.patient_repo.get_by_id.return_value = Mock()
        self.appointment_repo.get_doctor_appointments.return_value = [
            Mock(datetime=datetime(2023, 1, 1, 10, 15))
        ]

        with self.assertRaises(ValidationError):
            self.service.create_appointment(appointment_data)

    def test_get_all_appointments(self):
        self.appointment_repo.get_all.return_value = [Mock(), Mock()]
        result = self.service.get_all_appointments()
        self.assertEqual(len(result), 2)
        self.appointment_repo.get_all.assert_called_once()

    def test_get_appointment_by_id_success(self):
        mock_appointment = Mock(id=1)
        self.appointment_repo.get_by_id.return_value = mock_appointment
        result = self.service.get_appointment_by_id(1)
        self.assertEqual(result.id, 1)
        self.appointment_repo.get_by_id.assert_called_once_with(1)

    def test_update_appointment_success(self):
        appointment_data = AppointmentUpdate(status="DONE")
        mock_appointment = Mock(id=1, doctor_id=1, patient_id=1, datetime=datetime(2023, 1, 1, 10, 0))
        self.appointment_repo.get_by_id.return_value = mock_appointment
        self.appointment_repo.update.return_value = mock_appointment

        result = self.service.update_appointment(1, appointment_data)

        self.assertEqual(result.id, 1)
        self.appointment_repo.update.assert_called_once()

    def test_update_appointment_not_found(self):
        appointment_data = AppointmentUpdate(status="DONE")
        self.appointment_repo.get_by_id.return_value = None

        with self.assertRaises(ResourceNotFoundError):
            self.service.update_appointment(1, appointment_data)

    def test_update_appointment_with_datetime_change(self):
        appointment_data = AppointmentUpdate(datetime=datetime(2023, 1, 1, 11, 0))
        mock_appointment = Mock(id=1, doctor_id=1, patient_id=1, datetime=datetime(2023, 1, 1, 10, 0))
        self.appointment_repo.get_by_id.return_value = mock_appointment
        mock_doctor = Mock(work_start_time=time(9, 0), work_end_time=time(17, 0))
        self.doctor_repo.get_by_id.return_value = mock_doctor
        self.patient_repo.get_by_id.return_value = Mock()
        self.appointment_repo.get_doctor_appointments.return_value = []
        self.appointment_repo.update.return_value = mock_appointment

        # Convert the mock_appointment to a dictionary
        updated_appointment_data = {
            'id': mock_appointment.id,
            'doctor_id': mock_appointment.doctor_id,
            'patient_id': mock_appointment.patient_id,
            'datetime': appointment_data.datetime
        }

        # Mock the behavior of appointment_data.model_dump(exclude_unset=True)
        with patch.object(AppointmentUpdate, 'model_dump', return_value={'datetime': appointment_data.datetime}):
            result = self.service.update_appointment(1, appointment_data)

        self.assertEqual(result.id, 1)
        self.appointment_repo.update.assert_called_once()
        self.doctor_repo.get_by_id.assert_called_once_with(updated_appointment_data['doctor_id'])
        self.patient_repo.get_by_id.assert_called_once_with(updated_appointment_data['patient_id'])

    def test_delete_appointment_success(self):
        self.appointment_repo.delete.return_value = True
        result = self.service.delete_appointment(1)
        self.assertTrue(result)
        self.appointment_repo.delete.assert_called_once_with(1)

    def test_filter_appointments(self):
        filters = AppointmentFilter(doctor_id=1, start_date=datetime(2023, 1, 1))
        self.appointment_repo.filter_appointments.return_value = [Mock(), Mock()]
        result = self.service.filter_appointments(filters)
        self.assertEqual(len(result), 2)
        self.appointment_repo.filter_appointments.assert_called_once_with(filters)

    @patch('app.services.appointment.AppointmentService._validate_appointment')
    def test_create_appointment_integrity_error(self, mock_validate):
        appointment_data = AppointmentCreate(
            doctor_id=1,
            patient_id=1,
            datetime=datetime(2023, 1, 1, 10, 0)
        )
        mock_validate.return_value = None
        self.appointment_repo.create.side_effect = IntegrityError(None, None, None)

        with self.assertRaises(IntegrityError):
            self.service.create_appointment(appointment_data)

    @patch('app.services.appointment.AppointmentService._validate_appointment')
    def test_update_appointment_integrity_error(self, mock_validate):
        appointment_data = AppointmentUpdate(doctor_id=2)
        mock_appointment = Mock(id=1, doctor_id=1, patient_id=1, datetime=datetime(2023, 1, 1, 10, 0))
        self.appointment_repo.get_by_id.return_value = mock_appointment
        mock_validate.return_value = None
        self.appointment_repo.update.side_effect = IntegrityError(None, None, None)

        with self.assertRaises(IntegrityError):
            self.service.update_appointment(1, appointment_data)

if __name__ == '__main__':
    unittest.main()
