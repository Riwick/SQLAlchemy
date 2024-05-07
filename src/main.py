import uvicorn
from fastapi import FastAPI, APIRouter

from src.queries.orm import SyncORM
from src.schemas import WorkersRelListDTO, WorkersListDTO, ResumesRelListDTO

app = FastAPI()


workers_router = APIRouter(prefix="/workers", tags=["Workers"])

resumes_router = APIRouter(prefix="/resumes", tags=["Resumes"])


@workers_router.get("/", response_model=WorkersListDTO)
async def get_workers():
    workers = SyncORM.select_workers()
    return {"result": workers}


@workers_router.get("/with_resumes", response_model=WorkersRelListDTO)
async def get_workers_and_resumes():
    workers = SyncORM.convert_workers_to_dto()
    return {"result": workers}


@resumes_router.get("/", response_model=ResumesRelListDTO)
async def get_resumes():
    resumes = SyncORM.select_resumes()
    return {"result": resumes}


app.include_router(resumes_router)
app.include_router(workers_router)


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, host="localhost", port=8000)
