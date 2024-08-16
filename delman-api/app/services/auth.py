from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from app.repositories.employee import EmployeeRepository

class AuthService:
    def __init__(self, repo: EmployeeRepository):
        self.repo = repo

    def login(self, username: str, password: str):
        employee = self.repo.get_by_username(username)
        if employee and check_password_hash(employee.password, password):
            access_token = create_access_token(identity=employee.id)
            refresh_token = create_refresh_token(identity=employee.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        return None
