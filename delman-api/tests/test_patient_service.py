import unittest
from unittest.mock import Mock
from app.services.patient import PatientService
from app.repositories.patient import PatientRepository
from app.schemas.patient import PatientCreate, PatientUpdate
from app.models.gender import Gender
from app.exceptions import DuplicateResourceError
from sqlalchemy.exc import IntegrityError
from datetime import date
from app.models.patient import Patient

class TestPatientService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock(spec=PatientRepository)
        self.service = PatientService(self.mock_repo)

    def test_create_patient_success(self):
        patient_data = PatientCreate(
            name="John Doe",
            gender=Gender.MALE,
            birthdate=date(1990, 1, 1),
            no_ktp="1234567890123456",
            address="123 Main St, City"
        )
        mock_patient = Mock(spec=Patient)
        mock_patient.id = 1
        mock_patient.name = patient_data.name
        mock_patient.no_ktp = patient_data.no_ktp
        self.mock_repo.create.return_value = mock_patient

        result = self.service.create_patient(patient_data)

        self.assertEqual(result.id, mock_patient.id)
        self.assertEqual(result.name, mock_patient.name)
        self.assertEqual(result.no_ktp, mock_patient.no_ktp)
        self.mock_repo.create.assert_called_once_with(patient_data.model_dump())

    def test_create_patient_duplicate_ktp(self):
        patient_data = PatientCreate(
            name="John Doe",
            gender=Gender.MALE,
            birthdate=date(1990, 1, 1),
            no_ktp="1234567890123456",
            address="123 Main St, City"
        )
        mock_integrity_error = IntegrityError(None, None, None)
        mock_integrity_error.orig = Exception("unique constraint violated ktp")
        self.mock_repo.create.side_effect = mock_integrity_error

        with self.assertRaises(DuplicateResourceError) as context:
            self.service.create_patient(patient_data)
        
        self.assertIn("1234567890123456", str(context.exception))

    def test_create_patient_unknown_error(self):
        patient_data = PatientCreate(
            name="John Doe",
            gender=Gender.MALE,
            birthdate=date(1990, 1, 1),
            no_ktp="1234567890123456",
            address="123 Main St, City"
        )
        mock_integrity_error = IntegrityError(None, None, None)
        mock_integrity_error.orig = Exception("unknown erros")
        self.mock_repo.create.side_effect = mock_integrity_error

        with self.assertRaises(IntegrityError):
            self.service.create_patient(patient_data)

    def test_get_all_patients(self):
        mock_patients = [Mock(id=1), Mock(id=2)]
        self.mock_repo.get_all.return_value = mock_patients

        result = self.service.get_all_patients()

        self.assertEqual(len(result), 2)
        self.mock_repo.get_all.assert_called_once()

    def test_get_patient_by_id(self):
        mock_patient = Mock(spec=Patient)
        mock_patient.id = 1
        mock_patient.name = "John Doe"
        self.mock_repo.get_by_id.return_value = mock_patient

        result = self.service.get_patient_by_id(1)

        self.assertEqual(result.id, mock_patient.id)
        self.assertEqual(result.name, mock_patient.name)
        self.mock_repo.get_by_id.assert_called_once_with(1)

    def test_update_patient_success(self):
        update_data = PatientUpdate(name="Jane Doe")
        mock_patient = Mock(spec=Patient)
        mock_patient.id = 1
        mock_patient.name = "John Doe"
        self.mock_repo.update.return_value = mock_patient

        result = self.service.update_patient(1, update_data)

        self.assertEqual(result.id, mock_patient.id)
        self.assertEqual(result.name, mock_patient.name)
        self.mock_repo.update.assert_called_once_with(1, update_data.model_dump(exclude_unset=True))

    def test_update_patient_duplicate_ktp(self):
        update_data = PatientUpdate(no_ktp="9876543210987654")
        mock_integrity_error = IntegrityError(None, None, None)
        mock_integrity_error.orig = Exception("unique constraint violated ktp")
        self.mock_repo.update.side_effect = mock_integrity_error

        with self.assertRaises(DuplicateResourceError) as context:
            self.service.update_patient(1, update_data)
        
        self.assertIn("9876543210987654", str(context.exception))
    
    def test_update_patient_unknown_error(self):
        update_data = PatientUpdate(no_ktp="9876543210987654")
        mock_integrity_error = IntegrityError(None, None, None)
        mock_integrity_error.orig = Exception("unknown errors")
        self.mock_repo.update.side_effect = mock_integrity_error

        with self.assertRaises(IntegrityError):
            self.service.update_patient(1, update_data)

    def test_delete_patient(self):
        self.mock_repo.delete.return_value = True

        result = self.service.delete_patient(1)

        self.assertTrue(result)
        self.mock_repo.delete.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
