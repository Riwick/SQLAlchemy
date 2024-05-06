from sqlalchemy import select, update

from src.database import session_factory, sync_engine, async_session_factory, Base
from src.models import WorkersORM


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


class AsyncORM:

    @staticmethod
    async def async_insert_data():
        async with async_session_factory() as session:
            worker_bobr = WorkersORM(username="Bobr")
            worker_wolf = WorkersORM(username="Wolf")
            session.add_all([worker_bobr, worker_wolf])
            await session.commit()
