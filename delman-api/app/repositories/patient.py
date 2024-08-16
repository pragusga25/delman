from app.models.patient import Patient

class PatientRepository:
    def __init__(self, db):
        self.db = db

    def create(self, patient_data):
        patient = Patient(**patient_data)
        self.db.session.add(patient)
        self.db.session.commit()
        return patient

    def get_all(self):
        return Patient.query.all()

    def get_by_id(self, id):
        return Patient.query.get(id)

    def update(self, id, patient_data):
        patient = self.get_by_id(id)
        if patient:
            for key, value in patient_data.items():
                setattr(patient, key, value)
            self.db.session.commit()
        return patient

    def delete(self, id):
        patient = self.get_by_id(id)
        if patient:
            self.db.session.delete(patient)
            self.db.session.commit()
            return True
        return False
