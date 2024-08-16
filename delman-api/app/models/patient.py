from app.exts import db
from sqlalchemy.sql import func
from app.models.gender import Gender

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    no_ktp = db.Column(db.String(16), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    vaccine_type = db.Column(db.String(50), nullable=True)
    vaccine_count = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
