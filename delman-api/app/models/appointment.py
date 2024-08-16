from app.exts import db
from sqlalchemy.sql import func
from enum import Enum

class AppointmentStatus(Enum):
    IN_QUEUE = "IN_QUEUE"
    DONE = "DONE"
    CANCELLED = "CANCELLED"

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id', ondelete='CASCADE'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id', ondelete='CASCADE'), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(AppointmentStatus), nullable=False, default=AppointmentStatus.IN_QUEUE)
    diagnose = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    patient = db.relationship('Patient', backref=db.backref('appointments', cascade='all, delete-orphan'))
    doctor = db.relationship('Doctor', backref=db.backref('appointments', cascade='all, delete-orphan'))
