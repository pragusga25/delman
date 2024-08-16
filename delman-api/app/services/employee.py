from app.repositories.employee import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from werkzeug.security import generate_password_hash
from app.exceptions import UsernameAlreadyExistsError
from sqlalchemy.exc import IntegrityError

class EmployeeService:
    def __init__(self, repo: EmployeeRepository):
        self.repo = repo

    def create_employee(self, employee_data: EmployeeCreate):
        try:
            employee_dict = employee_data.model_dump()
            employee_dict['password'] = generate_password_hash(employee_dict['password'])
            return self.repo.create(employee_dict)
        except IntegrityError as e:
            if 'unique constraint' in str(e.orig).lower() and 'username' in str(e.orig).lower():
                raise UsernameAlreadyExistsError("employee", employee_data.username)
            raise e

    def get_all_employees(self):
        return self.repo.get_all()

    def get_employee_by_id(self, id: int):
        return self.repo.get_by_id(id)

    def update_employee(self, id: int, employee_data: EmployeeUpdate):
        try:
            employee_dict = employee_data.model_dump(exclude_unset=True)
            if 'password' in employee_dict:
                employee_dict['password'] = generate_password_hash(employee_dict['password'])
            return self.repo.update(id, employee_dict)
        except IntegrityError as e:
            if 'unique constraint' in str(e.orig).lower() and 'username' in str(e.orig).lower():
                raise UsernameAlreadyExistsError("employee", employee_data.username)
            raise e

    def delete_employee(self, id: int):
        return self.repo.delete(id)
