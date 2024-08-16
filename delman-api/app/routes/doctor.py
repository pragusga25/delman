from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.schemas.doctor import DoctorCreate, DoctorUpdate, DoctorResponse
from app.services.doctor import DoctorService
from app.exceptions import UsernameAlreadyExistsError
from pydantic import ValidationError
from app.utils import success_response, error_response

def create_doctor_blueprint(doctor_service: DoctorService):
    bp = Blueprint('doctors', __name__, url_prefix='/doctors')

    @bp.route('', methods=['POST'])
    @jwt_required()
    def create_doctor():
        try:
            data = DoctorCreate(**request.json)
            doctor = doctor_service.create_doctor(data)
            return success_response(DoctorResponse.model_validate(doctor).model_dump(), 201)
        except ValidationError as e:
            return error_response(str(e.errors()[0]["msg"]), "doctor/validation-error", 400)
        except UsernameAlreadyExistsError as e:
            return error_response(str(e), "doctor/username-exists", 409)
        except Exception as e:
            return error_response(str(e), "doctor/creation-failed", 500)

    @bp.route('', methods=['GET'])
    @jwt_required()
    def get_all_doctors():
        doctors = doctor_service.get_all_doctors()
        return success_response([DoctorResponse.model_validate(doctor).model_dump() for doctor in doctors])

    @bp.route('/<int:id>', methods=['GET'])
    @jwt_required()
    def get_doctor(id):
        doctor = doctor_service.get_doctor_by_id(id)
        if doctor:
            return success_response(DoctorResponse.model_validate(doctor).model_dump())
        return error_response(f"Doctor with id {id} not found", "doctor/not-found", 404)

    @bp.route('/<int:id>', methods=['PUT'])
    @jwt_required()
    def update_doctor(id):
        try:
            data = DoctorUpdate(**request.json)
            updated_doctor = doctor_service.update_doctor(id, data)
            if updated_doctor:
                return success_response(DoctorResponse.model_validate(updated_doctor).model_dump())
            return error_response(f"Doctor with id {id} not found", "doctor/not-found", 404)
        except ValidationError as e:
            return error_response(str(e.errors()[0]["msg"]), "doctor/validation-error", 400)
        except UsernameAlreadyExistsError as e:
            return error_response(str(e), "doctor/username-exists", 409)  # 409 Conflict
        except Exception as e:
            return error_response("Internal server error", "doctor/update-failed", 500)

    @bp.route('/<int:id>', methods=['DELETE'])
    @jwt_required()
    def delete_doctor(id):
        if doctor_service.delete_doctor(id):
            return success_response()
        return error_response(f"Doctor with id {id} not found", "doctor/not-found", 404)

    return bp
