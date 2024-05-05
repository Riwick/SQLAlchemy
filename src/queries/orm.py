from src.database import session_factory, sync_engine, async_session_factory, Base
from src.models import WorkersORM


def create_tables():
    Base.metadata.drop_all(sync_engine)
    sync_engine.echo = True
    Base.metadata.create_all(sync_engine)
    sync_engine.echo = True


def insert_data():
    with session_factory() as session:
        worker_bobr = WorkersORM(username="Bobr")
        worker_wolf = WorkersORM(username="Wolf")
        session.add_all([worker_bobr, worker_wolf])
        session.commit()


async def async_insert_data():
    async with async_session_factory() as session:
        worker_bobr = WorkersORM(username="Bobr")
        worker_wolf = WorkersORM(username="Wolf")
        session.add_all([worker_bobr, worker_wolf])
        await session.commit()


