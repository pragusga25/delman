from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.schemas.patient import PatientCreate, PatientUpdate, PatientResponse
from app.services.patient import PatientService
from app.exceptions import  DuplicateResourceError
from app.utils import success_response, error_response
from pydantic import ValidationError
from app.utils import construct_error_msg

def create_patient_blueprint(patient_service: PatientService):
    bp = Blueprint('patients', __name__, url_prefix='/patients')

    @bp.route('', methods=['POST'])
    @jwt_required()
    def create_patient():
        try:
            data = PatientCreate(**request.json)
            patient = patient_service.create_patient(data)
            return success_response(PatientResponse.model_validate(patient).model_dump(), 201)
        except DuplicateResourceError as e:
            return error_response(str(e), "patient/duplicate", 409)
        except ValidationError as e:
            return error_response(construct_error_msg(e), "patient/validation-error", 400)
        except Exception as e:
            return error_response(str(e), "patient/creation-failed", 500)

    @bp.route('', methods=['GET'])
    @jwt_required()
    def get_all_patients():
        patients = patient_service.get_all_patients()
        return success_response([PatientResponse.model_validate(patient).model_dump() for patient in patients])

    @bp.route('/<int:id>', methods=['GET'])
    @jwt_required()
    def get_patient(id):
        patient = patient_service.get_patient_by_id(id)
        if patient:
            return success_response(PatientResponse.model_validate(patient).model_dump())
        return error_response(f"Patient with id {id} not found", "patient/not-found", 404)

    @bp.route('/<int:id>', methods=['PUT'])
    @jwt_required()
    def update_patient(id):
        try:
            data = PatientUpdate(**request.json)
            updated_patient = patient_service.update_patient(id, data)
            if updated_patient:
                return success_response(PatientResponse.model_validate(updated_patient).model_dump())
            return error_response(f"Patient with id {id} not found", "patient/not-found", 404)
        except ValidationError as e:
            return error_response(construct_error_msg(e), "patient/validation-error", 400)
        except DuplicateResourceError as e:
            return error_response(str(e), "patient/duplicate-error", 409)
        except Exception as e:
            print(f"EEE: {e}")
            return error_response("Internal server error", "patient/update-failed", 500)

    @bp.route('/<int:id>', methods=['DELETE'])
    @jwt_required()
    def delete_patient(id):
        if patient_service.delete_patient(id):
            return success_response()
        return error_response(f"Patient with id {id} not found", "patient/not-found", 404)

    return bp
