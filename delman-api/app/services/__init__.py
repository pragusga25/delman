from app.repositories.employee import EmployeeRepository
from app.repositories.doctor import DoctorRepository
from app.services.employee import EmployeeService
from app.services.auth import AuthService
from app.services.doctor import DoctorService
from app.services.patient import PatientService
from app.repositories.patient import PatientRepository
from app.repositories.appointment import AppointmentRepository
from app.services.appointment import AppointmentService

def create_services(db):
    employee_repo = EmployeeRepository(db)
    doctor_repo = DoctorRepository(db)
    patient_repo = PatientRepository(db)
    appointment_repo = AppointmentRepository(db)
    return {
        'employee_service': EmployeeService(employee_repo),
        'auth_service': AuthService(employee_repo),
        'doctor_service': DoctorService(doctor_repo),
        'patient_service': PatientService(patient_repo),
        'appointment_service': AppointmentService(appointment_repo, doctor_repo, patient_repo)
    }
