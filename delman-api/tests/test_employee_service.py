import unittest
from unittest.mock import Mock
from app.services.employee import EmployeeService
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.models.gender import Gender
from datetime import date
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from app.exceptions import UsernameAlreadyExistsError

class TestEmployeeService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock()
        self.service = EmployeeService(self.mock_repo)

    def test_create_employee_valid(self):
        employee_data = EmployeeCreate(
            name="John Doe",
            username="johndoe",
            password="Pass1word!",
            gender=Gender.MALE,
            birthdate=date(1990, 1, 1)
        )
        self.mock_repo.create.return_value = Mock(id=1)
        result = self.service.create_employee(employee_data)
        self.assertEqual(result.id, 1)
        self.mock_repo.create.assert_called_once()

    def test_create_employee_username_exists(self):
        employee_data = EmployeeCreate(
            name="John Doe",
            username="johndoe",
            password="Password123!",
            gender=Gender.MALE,
            birthdate=date(1990, 1, 1)
        )
        self.mock_repo.create.side_effect = IntegrityError(
            statement="INSERT INTO employees ...",
            params={},
            orig=Exception("UNIQUE constraint failed: employees.username")
        )

        with self.assertRaises(UsernameAlreadyExistsError):
            self.service.create_employee(employee_data)

    def test_create_employee_unknown_error(self):
        employee_data = EmployeeCreate(
            name="John Doe",
            username="johndoe",
            password="Password123!",
            gender=Gender.MALE,
            birthdate=date(1990, 1, 1)
        )
        self.mock_repo.create.side_effect = IntegrityError(
            statement="INSERT INTO employees ...",
            params={},
            orig=Exception("unknown errors")
        )

        with self.assertRaises(IntegrityError):
            self.service.create_employee(employee_data)

    def test_create_employee_invalid_name(self):
        with self.assertRaises(ValidationError):
            EmployeeCreate(
                name="Jo",  # Too short
                username="johndoe",
                password="Pass1word!",
                gender=Gender.MALE,
                birthdate=date(1990, 1, 1)
            )

    def test_create_employee_invalid_username(self):
        with self.assertRaises(ValidationError):
            EmployeeCreate(
                name="John Doe",
                username="john@doe",  # Invalid character
                password="Pass1word!",
                gender=Gender.MALE,
                birthdate=date(1990, 1, 1)
            )

    def test_create_employee_invalid_password(self):
        with self.assertRaises(ValidationError):
            EmployeeCreate(
                name="John Doe",
                username="johndoe",
                password="password",  # Missing uppercase, number, and special character
                gender=Gender.MALE,
                birthdate=date(1990, 1, 1)
            )

    def test_update_employee_valid(self):
        employee_data = EmployeeUpdate(name="Jane Doe")
        self.mock_repo.update.return_value = Mock(id=1, employee_name="Jane Doe")
        result = self.service.update_employee(1, employee_data)
        self.assertEqual(result.employee_name, "Jane Doe")
        self.mock_repo.update.assert_called_once()

    def test_update_employee_username_exists(self):
        employee_data = EmployeeUpdate(
            name="John Doe Updated",
            username="johndoe",
        )
        self.mock_repo.update.side_effect = IntegrityError(
            statement="UPDATE employees ...",
            params={},
            orig=Exception("UNIQUE constraint failed: employees.username")
        )

        with self.assertRaises(UsernameAlreadyExistsError):
            self.service.update_employee(1, employee_data)

    def test_update_employee_unknown_error(self):
        employee_data = EmployeeUpdate(
            name="John Doe Updated",
            username="johndoe",
        )
        self.mock_repo.update.side_effect = IntegrityError(
            statement="UPDATE employees ...",
            params={},
            orig=Exception("unknown errors")
        )

        with self.assertRaises(IntegrityError):
            self.service.update_employee(1, employee_data)

    def test_update_employee_invalid_name(self):
        with self.assertRaises(ValidationError):
            EmployeeUpdate(name="J")  # Too short

    def test_update_employee_invalid_birthdate(self):
        with self.assertRaises(ValidationError):
            EmployeeUpdate(birthdate="invalid-date")

    def test_get_all_employees(self):
        self.mock_repo.get_all.return_value = [Mock(id=1), Mock(id=2)]
        result = self.service.get_all_employees()
        self.assertEqual(len(result), 2)
        self.mock_repo.get_all.assert_called_once()

    def test_get_employee_by_id(self):
        self.mock_repo.get_by_id.return_value = Mock(id=1)
        result = self.service.get_employee_by_id(1)
        self.assertEqual(result.id, 1)
        self.mock_repo.get_by_id.assert_called_once_with(1)

    def test_delete_employee(self):
        self.mock_repo.delete.return_value = True
        result = self.service.delete_employee(1)
        self.assertTrue(result)
        self.mock_repo.delete.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
