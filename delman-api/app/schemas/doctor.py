from app.schemas.base import DoctorEmployeeCreate, DoctorEmployeeResponse, DoctorEmployeeUpdate
from datetime import time
from typing import Optional

class DoctorCreate(DoctorEmployeeCreate):
    work_start_time: time
    work_end_time: time

class DoctorUpdate(DoctorEmployeeUpdate):
    work_start_time: Optional[time] = None
    work_end_time: Optional[time] = None


class DoctorResponse(DoctorEmployeeResponse):
    work_start_time: time
    work_end_time: time
