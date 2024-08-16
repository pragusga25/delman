from app.models.appointment import Appointment
from sqlalchemy import and_
from typing import List, Optional
from sqlalchemy.orm import joinedload

class AppointmentRepository:
    def __init__(self, db):
        self.db = db

    def create(self, appointment_data) -> Appointment:
        appointment = Appointment(**appointment_data)
        self.db.session.add(appointment)
        self.db.session.commit()
        return appointment

    def get_all(self) -> List[Appointment]:
        return Appointment.query.all()

    def get_by_id(self, id) -> Optional[Appointment]:
        # return Appointment.query.get(id)
        return Appointment.query.options(
            joinedload(Appointment.patient),
            joinedload(Appointment.doctor)
        ).get(id)

    def update(self, id, appointment_data) -> Optional[Appointment]:
        appointment = self.get_by_id(id)
        if appointment:
            for key, value in appointment_data.items():
                setattr(appointment, key, value)
            self.db.session.commit()
        return appointment

    def delete(self, id) -> bool:
        appointment = self.get_by_id(id)
        if appointment:
            self.db.session.delete(appointment)
            self.db.session.commit()
            return True
        return False

    def get_doctor_appointments(self, doctor_id, start_datetime, end_datetime):
        return Appointment.query.filter(
            and_(
                Appointment.doctor_id == doctor_id,
                Appointment.datetime >= start_datetime,
                Appointment.datetime < end_datetime
            )
        ).all()

    def filter_appointments(self, filters):
        query = Appointment.query
        if filters.patient_id:
            query = query.filter(Appointment.patient_id == filters.patient_id)
        if filters.doctor_id:
            query = query.filter(Appointment.doctor_id == filters.doctor_id)
        if filters.status:
            query = query.filter(Appointment.status == filters.status)
        if filters.start_date:
            query = query.filter(Appointment.datetime >= filters.start_date)
        if filters.end_date:
            query = query.filter(Appointment.datetime < filters.end_date)
        return query.all()
