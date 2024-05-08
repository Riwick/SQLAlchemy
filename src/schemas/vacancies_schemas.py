from pydantic import BaseModel
from typing import Optional

from src.schemas.resumes_schemas import ResumesDTO


class VacanciesAddDTO(BaseModel):
    title: str
    compensation: Optional[int]


class VacanciesDTO(VacanciesAddDTO):
    vacancy_id: int


class ResumesRelVacanciesRepliedDTO(ResumesDTO):
    worker: "WorkersDTO"
    vacancies_replied: list["VacanciesDTO"]
