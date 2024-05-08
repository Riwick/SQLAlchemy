from pydantic import BaseModel

from src.schemas.resumes_schemas import ResumesDTO


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
