import uvicorn
from fastapi import FastAPI, APIRouter

from src.queries.workers_orm import WorkersQueries
from src.queries.resumes_orm import ResumesQueries
from src.queries.vacancies_orm import VacanciesQueries

from src.schemas.resumes_schemas import ResumesRelListDTO
from src.schemas.workers_schemas import WorkersRelListDTO, WorkersListDTO

app = FastAPI()


workers_router = APIRouter(prefix="/workers", tags=["Workers"])

resumes_router = APIRouter(prefix="/resumes", tags=["Resumes"])

vacancies_router = APIRouter(prefix="/vacancies", tags=["Vacancies"])


@workers_router.get("/", response_model=WorkersListDTO)
async def get_workers():
    workers = WorkersQueries.select_workers()
    return {"result": workers}


@workers_router.get("/with_resumes", response_model=WorkersRelListDTO)
async def get_workers_and_resumes():
    workers = WorkersQueries.convert_workers_to_dto()
    return {"result": workers}


@resumes_router.get("/", response_model=ResumesRelListDTO)
async def get_resumes():
    resumes = ResumesQueries.select_resumes()
    return {"result": resumes}


@resumes_router.get("/resumes_with_relationships")
async def get_resumes_relationships():
    resumes = ResumesQueries.select_resumes_with_all_relationships()
    return resumes


@vacancies_router.get("/")
async def get_vacancies():
    vacancies = VacanciesQueries.select_vacancies()
    return vacancies


@vacancies_router.get("/vacancies_replied")
async def get_vacancies_replied():
    vacancies = VacanciesQueries.select_vacancies_replies()
    return vacancies


app.include_router(vacancies_router)
app.include_router(resumes_router)
app.include_router(workers_router)


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, host="localhost", port=8000)
    # SyncORM.create_tables()
    # SyncORM.add_vacancies_and_replies()
