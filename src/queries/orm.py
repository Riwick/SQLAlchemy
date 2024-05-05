from src.database import session_factory, sync_engine, async_session_factory
from src.models import WorkersORM, metadata_obj


def create_tables():
    sync_engine.echo = False
    metadata_obj.drop_all(sync_engine)
    metadata_obj.create_all(sync_engine)
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


