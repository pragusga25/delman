import unittest
from unittest.mock import Mock
from app.services.doctor import DoctorService
from app.schemas.doctor import DoctorCreate, DoctorUpdate
from app.models.gender import Gender
from datetime import date, time
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from app.exceptions import UsernameAlreadyExistsError

class TestDoctorService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock()
        self.service = DoctorService(self.mock_repo)

    def test_create_doctor_valid(self):
        doctor_data = DoctorCreate(
            name="Dr. John Doe",
            username="drjohndoe",
            password="Pass1word!",
            gender=Gender.MALE,
            birthdate=date(1980, 1, 1),
            work_start_time=time(9, 0),
            work_end_time=time(17, 0)
        )
        self.mock_repo.create.return_value = Mock(id=1)
        result = self.service.create_doctor(doctor_data)
        self.assertEqual(result.id, 1)
        self.mock_repo.create.assert_called_once()

    def test_create_doctor_username_exists(self):
        doctor_data = DoctorCreate(
            name="Dr. John Doe",
            username="drjohndoe",
            password="Password123!",
            gender=Gender.MALE,
            birthdate=date(1980, 1, 1),
            work_start_time=time(9, 0),
            work_end_time=time(17, 0)
        )
        self.mock_repo.create.side_effect = IntegrityError(
            statement="INSERT INTO doctors ...",
            params={},
            orig=Exception("UNIQUE constraint failed: doctors.username")
        )

        with self.assertRaises(UsernameAlreadyExistsError):
            self.service.create_doctor(doctor_data)

    def test_create_doctor_unknown_error(self):
        doctor_data = DoctorCreate(
            name="Dr. John Doe",
            username="drjohndoe",
            password="Password123!",
            gender=Gender.MALE,
            birthdate=date(1980, 1, 1),
            work_start_time=time(9, 0),
            work_end_time=time(17, 0)
        )
        self.mock_repo.create.side_effect = IntegrityError(
            statement="INSERT INTO doctors ...",
            params={},
            orig=Exception("unknown errors")
        )

        with self.assertRaises(IntegrityError):
            self.service.create_doctor(doctor_data)

    def test_create_doctor_invalid_name(self):
        with self.assertRaises(ValidationError):
            DoctorCreate(
                name="Dr",  # Too short
                username="drjohndoe",
                password="Pass1word!",
                gender=Gender.MALE,
                birthdate=date(1980, 1, 1),
                work_start_time=time(9, 0),
                work_end_time=time(17, 0)
            )

    def test_create_doctor_invalid_username(self):
        with self.assertRaises(ValidationError):
            DoctorCreate(
                name="Dr. John Doe",
                username="dr@johndoe",  # Invalid character
                password="Pass1word!",
                gender=Gender.MALE,
                birthdate=date(1980, 1, 1),
                work_start_time=time(9, 0),
                work_end_time=time(17, 0)
            )

    def test_create_doctor_invalid_password(self):
        with self.assertRaises(ValidationError):
            DoctorCreate(
                name="Dr. John Doe",
                username="drjohndoe",
                password="password",  # Missing uppercase, number, and special character
                gender=Gender.MALE,
                birthdate=date(1980, 1, 1),
                work_start_time=time(9, 0),
                work_end_time=time(17, 0)
            )

    def test_update_doctor_valid(self):
        doctor_data = DoctorUpdate(name="Dr. Jane Doe")
        self.mock_repo.update.return_value = Mock(id=1, doctor_name="Dr. Jane Doe")
        result = self.service.update_doctor(1, doctor_data)
        self.assertEqual(result.doctor_name, "Dr. Jane Doe")
        self.mock_repo.update.assert_called_once()

    def test_update_doctor_username_exists(self):
        doctor_data = DoctorUpdate(
            name="Dr. John Doe Updated",
            username="drjohndoe",
        )
        self.mock_repo.update.side_effect = IntegrityError(
            statement="UPDATE doctors ...",
            params={},
            orig=Exception("UNIQUE constraint failed: doctors.username")
        )

        with self.assertRaises(UsernameAlreadyExistsError):
            self.service.update_doctor(1, doctor_data)

    def test_update_doctor_unknown_error(self):
        doctor_data = DoctorUpdate(
            name="Dr. John Doe Updated",
            username="drjohndoe",
        )
        self.mock_repo.update.side_effect = IntegrityError(
            statement="UPDATE doctors ...",
            params={},
            orig=Exception("unknown errors")
        )

        with self.assertRaises(IntegrityError):
            self.service.update_doctor(1, doctor_data)

    def test_update_doctor_invalid_name(self):
        with self.assertRaises(ValidationError):
            DoctorUpdate(name="Dr")  # Too short

    def test_update_doctor_invalid_birthdate(self):
        with self.assertRaises(ValidationError):
            DoctorUpdate(birthdate="invalid-date")

    def test_get_all_doctors(self):
        self.mock_repo.get_all.return_value = [Mock(id=1), Mock(id=2)]
        result = self.service.get_all_doctors()
        self.assertEqual(len(result), 2)
        self.mock_repo.get_all.assert_called_once()

    def test_get_doctor_by_id(self):
        self.mock_repo.get_by_id.return_value = Mock(id=1)
        result = self.service.get_doctor_by_id(1)
        self.assertEqual(result.id, 1)
        self.mock_repo.get_by_id.assert_called_once_with(1)

    def test_delete_doctor(self):
        self.mock_repo.delete.return_value = True
        result = self.service.delete_doctor(1)
        self.assertTrue(result)
        self.mock_repo.delete.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
