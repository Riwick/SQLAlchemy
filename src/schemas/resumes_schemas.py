import datetime
from typing import Optional

from pydantic import BaseModel

from src.models import WorkLoad


class ResumesAddDTO(BaseModel):
    title: str
    compensation: Optional[int]
    workload: WorkLoad
    worker_id: int


class ResumesDTO(ResumesAddDTO):
    resume_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ResumesRelDTO(ResumesDTO):
    worker: "WorkersDTO"


class ResumesRelListDTO(BaseModel):
    result: list["ResumesRelDTO"]
