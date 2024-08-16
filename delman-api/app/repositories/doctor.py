from app.models.doctor import Doctor
from typing import Optional, List

class DoctorRepository:
    def __init__(self, db):
        self.db = db

    def create(self, doctor_data) -> Doctor:
        doctor = Doctor(**doctor_data)
        self.db.session.add(doctor)
        self.db.session.commit()
        return doctor

    def get_all(self) -> List[Doctor]:
        return Doctor.query.all()

    def get_by_id(self, id) -> Optional[Doctor]:
        return Doctor.query.get(id)

    def update(self, id, doctor_data) -> Optional[Doctor]:
        doctor = self.get_by_id(id)
        if doctor:
            for key, value in doctor_data.items():
                setattr(doctor, key, value)
            self.db.session.commit()
        return doctor

    def delete(self, id) -> bool:
        doctor = self.get_by_id(id)
        if doctor:
            self.db.session.delete(doctor)
            self.db.session.commit()
            return True
        return False
