from sqlalchemy import select
from sqlalchemy.orm import selectinload, contains_eager, joinedload

from src.database import session_factory
from src.models import WorkersORM, ResumesORM
from src.schemas.workers_schemas import WorkersDTO, WorkersRelDTO


class WorkersQueries:

    @staticmethod
    def insert_workers():
        with session_factory() as session:
            worker_bobr = WorkersORM(username="Bobr")
            worker_wolf = WorkersORM(username="Wolf")
            session.add_all([worker_bobr, worker_wolf])
            # session.flush()
            session.commit()

    @staticmethod
    def select_workers():
        with session_factory() as session:
            query = (
                select(WorkersORM)
            )
            res = session.execute(query).scalars().all()
            workers = [WorkersDTO.model_validate(row, from_attributes=True) for row in res]
            return workers

    @staticmethod
    def update_worker(worker_id: int = 2, new_username: str = "Michael"):
        with session_factory() as session:
            worker = session.get(WorkersORM, {"worker_id": worker_id})
            worker.username = new_username
            session.refresh(worker)
            # stmt = (
            #     update(WorkersORM).
            #     values(username=new_username).
            #     filter(WorkersORM.worker_id == worker_id)
            # )
            # session.execute(stmt)
            session.commit()

    @staticmethod
    def select_workers_with_selectin_relationship():
        """Для связи o2m и m2m (один-ко-многим и многие-ко-многим)"""
        with session_factory() as session:
            query = (
                select(WorkersORM).options(selectinload(WorkersORM.resumes))
            )
            res = session.execute(query)
            result = res.unique().scalars().all()

            return result

    @staticmethod
    def convert_workers_to_dto():
        with session_factory() as session:
            query = (
                select(WorkersORM).options(selectinload(WorkersORM.resumes))
                .limit(2)
            )
            res = session.execute(query).scalars().all()

            result_dto = [WorkersRelDTO.model_validate(row, from_attributes=True) for row in res]
            return result_dto

    @staticmethod
    def select_workers_with_condition_relationships():
        with session_factory() as session:
            query = (
                select(WorkersORM).options(selectinload(WorkersORM.resumes))
            )
            res = session.execute(query)
            result = res.scalars().all()

            print(result)

    @staticmethod
    def select_workers_with_condition_relationships_contains_eager():
        with session_factory() as session:
            query = (
                select(WorkersORM).
                join(WorkersORM.resumes).
                options(contains_eager(WorkersORM.resumes)).
                filter(ResumesORM.workload == "part_time")
            )
            res = session.execute(query)
            result = res.unique().scalars().all()

            print(result)

    @staticmethod
    def select_workers_with_lazy_relationship():
        with session_factory() as session:
            query = (
                select(WorkersORM)
            )
            res = session.execute(query)
            result = res.scalars().all()

            worker_1_resumes = result[3].resumes
            worker_2_resumes = result[2].resumes

            print(worker_1_resumes)
            print(worker_2_resumes)

    @staticmethod
    def select_workers_with_joined_relationship():
        """Для связи m2o и o2o (многие-к-одному и один-к-одному)"""
        with session_factory() as session:
            query = (
                select(WorkersORM).options(joinedload(WorkersORM.resumes))
            )
            res = session.execute(query)
            result = res.unique().scalars().all()

            worker_1_resumes = result[3].resumes
            worker_2_resumes = result[2].resumes

            print(worker_1_resumes)
            print(worker_2_resumes)