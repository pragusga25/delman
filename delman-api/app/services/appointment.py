from app.repositories.appointment import AppointmentRepository
from app.repositories.doctor import DoctorRepository
from app.repositories.patient import PatientRepository
from app.exceptions import ResourceNotFoundError, ValidationError
from datetime import timedelta, datetime
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentFilter

class AppointmentService:
    def __init__(self, appointment_repo: AppointmentRepository, doctor_repo: DoctorRepository, patient_repo: PatientRepository):
        self.appointment_repo = appointment_repo
        self.doctor_repo = doctor_repo
        self.patient_repo = patient_repo

    def create_appointment(self, appointment_data: AppointmentCreate):
        appointment_data_dict = appointment_data.model_dump()
        self._validate_appointment(appointment_data_dict)
        return self.appointment_repo.create(appointment_data_dict)

    def get_all_appointments(self):
        return self.appointment_repo.get_all()

    def get_appointment_by_id(self, id: int):
        return self.appointment_repo.get_by_id(id)

    def update_appointment(self, id: int, appointment_data: AppointmentUpdate):
        existing_appointment = self.get_appointment_by_id(id)
        if not existing_appointment:
            raise ResourceNotFoundError(f"Appointment with id {id} not found", "appointment/not-found")
        
        appointment_data_dict = appointment_data.model_dump(exclude_unset=True)
        
        # If doctor_id, patient_id, or datetime is being updated, we need to validate
        if 'doctor_id' in appointment_data_dict or 'patient_id' in appointment_data_dict or 'datetime' in appointment_data_dict:
            updated_appointment_data: dict = existing_appointment.__dict__
            updated_appointment_data.update(appointment_data_dict)
            self._validate_appointment(updated_appointment_data)
        
        updated_appointment = self.appointment_repo.update(id, appointment_data_dict)
        return updated_appointment

    def delete_appointment(self, id: int) -> bool:
        return self.appointment_repo.delete(id)

    def filter_appointments(self, filters: AppointmentFilter):
        return self.appointment_repo.filter_appointments(filters)

    def _validate_appointment(self, appointment_data: dict):
        doctor = self.doctor_repo.get_by_id(appointment_data['doctor_id'])
        if not doctor:
            raise ResourceNotFoundError(f"Doctor with id {appointment_data['doctor_id']} not found", "appointment/doctor-not-found")

        patient = self.patient_repo.get_by_id(appointment_data['patient_id'])
        if not patient:
            raise ResourceNotFoundError(f"Patient with id {appointment_data['patient_id']} not found", "appointment/patient-not-found")

        # Check if the appointment time is within doctor's working hours
        appointment_time = appointment_data['datetime'].time()
        if appointment_time < doctor.work_start_time or appointment_time >= doctor.work_end_time:
            raise ValidationError("Appointment time is outside of doctor's working hours")

        # Check if the doctor is already booked at this time
        appointment_date = appointment_data['datetime'].date()
        start_datetime = datetime.combine(appointment_date, doctor.work_start_time)
        end_datetime = datetime.combine(appointment_date, doctor.work_end_time)
        existing_appointments = self.appointment_repo.get_doctor_appointments(doctor.id, start_datetime, end_datetime)
        
        for existing_appointment in existing_appointments:
            if existing_appointment.id != appointment_data.get('id') and \
                abs(existing_appointment.datetime - appointment_data['datetime']) < timedelta(minutes=30):
                raise ValidationError("Doctor is already booked at this time")
