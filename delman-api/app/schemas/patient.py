from pydantic import Field
from typing import Optional
from app.schemas.base import BasicInfoCreate, BasicInfoResponse, BasicInfoUpdate

class PatientCreate(BasicInfoCreate):
    no_ktp: str = Field(min_length=16, max_length=16, pattern=r'^\d+$', title='Nomor KTP')
    address: str = Field(min_length=5, max_length=200)

class PatientUpdate(BasicInfoUpdate):
    no_ktp: Optional[str] = Field(None, min_length=16, max_length=16, pattern=r'^\d+$')
    address: Optional[str] = Field(None, min_length=5, max_length=200)

class PatientResponse(BasicInfoResponse):
    no_ktp: str
    address: str
    vaccine_type: Optional[str] = None
    vaccine_count: Optional[int] = None
