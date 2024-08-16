from flask import Blueprint, request
from app.schemas.auth import LoginRequest
from app.services.auth import AuthService
from pydantic import ValidationError
from app.utils import success_response, error_response

def create_auth_blueprint(auth_service: AuthService):
    bp = Blueprint('auth', __name__, url_prefix='/auth')

    @bp.route('/login', methods=['POST'])
    def login():
        try:
            login_data = LoginRequest(**request.json)
            tokens = auth_service.login(login_data.username, login_data.password)
            if tokens:
                return success_response(tokens)
            return error_response("Invalid username or password", "auth/invalid-credentials", 401)
        except ValidationError as e:
            return error_response(str(e.errors()[0]["msg"]), "auth/validation-error", 400)
        except Exception as e:
            return error_response("Internal server error", "auth/login-failed", 500)

    return bp
