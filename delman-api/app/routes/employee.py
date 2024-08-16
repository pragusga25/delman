from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.services.employee import EmployeeService
from pydantic import ValidationError
from app.utils import success_response, error_response
from app.exceptions import UsernameAlreadyExistsError

def create_employee_blueprint(employee_service: EmployeeService):
    bp = Blueprint('employees', __name__, url_prefix='/employees')

    @bp.route('', methods=['POST'])
    @jwt_required()
    def create_employee():
        try:
            data = EmployeeCreate(**request.json)
            employee = employee_service.create_employee(data)
            return success_response(EmployeeResponse.model_validate(employee).model_dump(), 201)
        except ValidationError as e:
            return error_response(str(e.errors()[0]["msg"]), "employee/validation-error", 400)
        except UsernameAlreadyExistsError as e:
            return error_response(str(e), "employee/username-exists", 409)  # 409 Conflict
        except Exception as e:
            return error_response("Internal server error", "employee/creation-failed", 500)

    @bp.route('', methods=['GET'])
    @jwt_required()
    def get_all_employees():
        employees = employee_service.get_all_employees()
        return success_response([EmployeeResponse.model_validate(employee).model_dump() for employee in employees])

    @bp.route('/<int:id>', methods=['GET'])
    @jwt_required()
    def get_employee(id):
        employee = employee_service.get_employee_by_id(id)
        if employee:
            return success_response(EmployeeResponse.model_validate(employee).model_dump())
        return error_response(f"Employee with id {id} not found", "employee/not-found", 404)

    @bp.route('/<int:id>', methods=['PUT'])
    @jwt_required()
    def update_employee(id):
        try:
            data = EmployeeUpdate(**request.json)
            updated_employee = employee_service.update_employee(id, data)
            if updated_employee:
                return success_response(EmployeeResponse.model_validate(updated_employee).model_dump())
            return error_response(f"Employee with id {id} not found", "employee/not-found", 404)
        except ValidationError as e:
            return error_response(str(e.errors()[0]["msg"]), "employee/validation-error", 400)
        except UsernameAlreadyExistsError as e:
            return error_response(str(e), "employee/username-exists", 409)  # 409 Conflict
        except Exception as e:
            return error_response("Internal server error", "employee/update-failed", 500)

    @bp.route('/<int:id>', methods=['DELETE'])
    @jwt_required()
    def delete_employee(id):
        if employee_service.delete_employee(id):
            return success_response()
        return error_response(f"Employee with id {id} not found", "employee/not-found", 404)

    return bp
