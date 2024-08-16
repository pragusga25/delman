from app.repositories.patient import PatientRepository
from app.exceptions import DuplicateResourceError
from sqlalchemy.exc import IntegrityError
from app.schemas.patient import PatientCreate, PatientUpdate

class PatientService:
    def __init__(self, repo: PatientRepository):
        self.repo = repo

    def create_patient(self, patient_data: PatientCreate):
        try:
            patient_dict = patient_data.model_dump()
            return self.repo.create(patient_dict)
        except IntegrityError as e:
            if 'unique constraint' in str(e.orig).lower() and 'ktp' in str(e.orig).lower():
                raise DuplicateResourceError(f"A patient with KTP number {patient_data.no_ktp} already exists.")
            raise e

    def get_all_patients(self):
        return self.repo.get_all()

    def get_patient_by_id(self, id: int):
        return self.repo.get_by_id(id)

    def update_patient(self, id: int, patient_data: PatientUpdate):
        try:
            patient_dict = patient_data.model_dump(exclude_unset=True)
            return self.repo.update(id, patient_dict)
        except IntegrityError as e:
            if 'unique constraint' in str(e.orig).lower() and 'ktp' in str(e.orig).lower():
                raise DuplicateResourceError(f"A patient with KTP number {patient_data.no_ktp} already exists.")
            raise e

    def delete_patient(self, id):
        return self.repo.delete(id)
