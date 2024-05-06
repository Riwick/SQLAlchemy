from sqlalchemy import select, update, func, cast, Integer, and_

from src.database import session_factory, sync_engine, async_session_factory, Base
from src.models import WorkersORM, ResumesORM


class SyncORM:

    @staticmethod
    def create_tables():
        Base.metadata.drop_all(sync_engine)
        sync_engine.echo = True
        Base.metadata.create_all(sync_engine)

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
            query = select(WorkersORM)
            res = session.execute(query)
            workers = res.scalars().all()
            print(f"{workers=}")

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
    def select_resumes_avg_compensation():
        """select workload, avg(compensation)::int as avg_compensation
        from resumes
        where title like '%Python%' and compensation > 40000
        group by workload"""
        with session_factory() as session:
            query = (
                select(
                    ResumesORM.workload,
                    cast(func.avg(ResumesORM.compensation), Integer).label("avg_compensation"),
                ).
                where(and_(
                    ResumesORM.title.like("%Python%"),
                    ResumesORM.compensation > 40000,
                )).
                group_by(ResumesORM.workload).
                having(cast(func.avg(ResumesORM.compensation), Integer) > 70000)
            )
            # print(query.compile(compile_kwargs={"literal_binds": True}))
            result = session.execute(query).all()
            print(result[0].avg_compensation)
            print(result)


class AsyncORM:

    @staticmethod
    async def async_insert_data():
        async with async_session_factory() as session:
            worker_bobr = WorkersORM(username="Bobr")
            worker_wolf = WorkersORM(username="Wolf")
            session.add_all([worker_bobr, worker_wolf])
            await session.commit()
