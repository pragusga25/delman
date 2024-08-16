from app.repositories.doctor import DoctorRepository
from app.exceptions import UsernameAlreadyExistsError
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from app.schemas.doctor import DoctorCreate, DoctorUpdate

class DoctorService:
    def __init__(self, repo: DoctorRepository):
        self.repo = repo

    def create_doctor(self, doctor_data: DoctorCreate):
        try:
            doctor_data_dict = doctor_data.model_dump()
            doctor_data_dict['password'] = generate_password_hash(doctor_data_dict['password'])
            return self.repo.create(doctor_data_dict)
        except IntegrityError as e:
            if 'unique constraint' in str(e.orig).lower() and 'username' in str(e.orig).lower():
                raise UsernameAlreadyExistsError('doctor', doctor_data.username)
            raise e

    def get_all_doctors(self):
        return self.repo.get_all()

    def get_doctor_by_id(self, id):
        return self.repo.get_by_id(id)

    def update_doctor(self, id: int, doctor_data: DoctorUpdate):
        try:
            doctor_data_dict = doctor_data.model_dump(exclude_unset=True)
            return self.repo.update(id, doctor_data_dict)
        except IntegrityError as e:
            if 'unique constraint' in str(e.orig).lower() and 'username' in str(e.orig).lower():
                raise UsernameAlreadyExistsError('doctor', doctor_data.username)
            raise e

    def delete_doctor(self, id: int):
        return self.repo.delete(id)
