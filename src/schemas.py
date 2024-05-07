import datetime

from pydantic import BaseModel
from typing import Optional

from src.models import WorkLoad


class WorkersAddDTO(BaseModel):
    username: str


class WorkersDTO(WorkersAddDTO):
    worker_id: int


class WorkersRelDTO(WorkersDTO):
    resumes: list["ResumesDTO"]


class WorkersRelListDTO(BaseModel):
    result: list["WorkersRelDTO"]


class WorkersListDTO(BaseModel):
    result: list["WorkersDTO"]

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


