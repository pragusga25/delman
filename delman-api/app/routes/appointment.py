from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentResponse, AppointmentFilter, AppointmentDetailResponse
from app.services.appointment import AppointmentService
from app.exceptions import ResourceNotFoundError, ValidationError
from pydantic import ValidationError as PydanticValidationError
from app.utils import success_response, error_response

def create_appointment_blueprint(appointment_service: AppointmentService):
    bp = Blueprint('appointments', __name__, url_prefix='/appointments')

    @bp.route('', methods=['POST'])
    @jwt_required()
    def create_appointment():
        try:
            data = AppointmentCreate(**request.json)
            appointment = appointment_service.create_appointment(data)
            return success_response(AppointmentResponse.model_validate(appointment).model_dump(), 201)
        except PydanticValidationError as e:
            return error_response(str(e.errors()[0]["msg"]), "appointment/validation-error", 400)
        except ValidationError as e:
            return error_response(str(e), "appointment/validation-error", 400)
        except ResourceNotFoundError as e:
            return error_response(str(e), e.err_code, 404)
        except Exception as e:
            return error_response("Internal server error", "appointment/creation-failed", 500)

    @bp.route('', methods=['GET'])
    @jwt_required()
    def get_all_appointments():
        filter_data = AppointmentFilter(**request.args)
        appointments = appointment_service.filter_appointments(filter_data)
        return success_response([AppointmentResponse.model_validate(appointment).model_dump() for appointment in appointments])

    @bp.route('/<int:id>', methods=['GET'])
    @jwt_required()
    def get_appointment(id):
        appointment = appointment_service.get_appointment_by_id(id)
        if appointment:
            return success_response(AppointmentDetailResponse.model_validate(appointment).model_dump())
        return error_response(f"Appointment with id {id} not found", "appointment/not-found", 404)

    @bp.route('/<int:id>', methods=['PUT'])
    @jwt_required()
    def update_appointment(id):
        try:
            data = AppointmentUpdate(**request.json)
            updated_appointment = appointment_service.update_appointment(id, data)
            if updated_appointment:
                return success_response(AppointmentResponse.model_validate(updated_appointment).model_dump())
            return error_response(f"Appointment with id {id} not found", "appointment/not-found", 404)
        except PydanticValidationError as e:
            return error_response(str(e.errors()[0]["msg"]), "appointment/validation-error", 400)
        except ValidationError as e:
            return error_response(str(e), "appointment/validation-error", 400)
        except ResourceNotFoundError as e:
            return error_response(str(e), e.err_code, 404)
        except Exception as e:
            return error_response("Internal server error", "appointment/update-failed", 500)

    @bp.route('/<int:id>', methods=['DELETE'])
    @jwt_required()
    def delete_appointment(id):
        if appointment_service.delete_appointment(id):
            return success_response()
        return error_response(f"Appointment with id {id} not found", "appointment/not-found", 404)

    return bp
