from pydantic import BaseModel, ConfigDict
from datetime import datetime as dt
from typing import Optional
from app.models.appointment import AppointmentStatus
from app.schemas.base import BasicInfoResponse

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    datetime: dt
    diagnose: Optional[str] = None
    notes: Optional[str] = None
    status: AppointmentStatus = AppointmentStatus.IN_QUEUE

class AppointmentUpdate(BaseModel):
    status: Optional[AppointmentStatus] = None
    diagnose: Optional[str] = None
    notes: Optional[str] = None
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    datetime: Optional[dt] = None 

class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    datetime: dt
    status: str
    diagnose: Optional[str] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class AppointmentDetailResponse(BaseModel):
    id: int
    datetime: dt
    status: str
    diagnose: Optional[str] = None
    notes: Optional[str] = None
    patient: BasicInfoResponse
    doctor: BasicInfoResponse

    model_config = ConfigDict(from_attributes=True)

class AppointmentFilter(BaseModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    status: Optional[AppointmentStatus] = None
    start_date: Optional[dt] = None
    end_date: Optional[dt] = None
