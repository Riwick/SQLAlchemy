from sqlalchemy import select, insert, update, text
from src.database import async_engine, sync_engine, session_factory
from src.models import metadata_obj, workers_table, WorkersORM


class SyncCore:

    @staticmethod
    def create_tables():
        sync_engine.echo = False
        metadata_obj.drop_all(sync_engine)
        metadata_obj.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_workers():
        with sync_engine.connect() as conn:
            # stmt = """INSERT INTO workers (username) VALUES
            # ('Jack'),
            # ('Michael')"""
            stmt = insert(workers_table).values([
                {"username": "John"},
                {"username": "Michael"}
            ])
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def select_workers():
        with sync_engine.connect() as coon:
            query = select(workers_table)
            res = coon.execute(query)
            workers = res.all()
            print(f"{workers=}")

    @staticmethod
    def update_worker(worker_id: int = 1, new_username: str = "Micha"):
        with sync_engine.connect() as conn:
            # stmt = text("UPDATE workers SET username=:username WHERE worker_id=:worker_id")
            # stmt = stmt.bindparams(username=new_username, worker_id=worker_id)'
            stmt = (
                update(workers_table).
                # where(workers_table.c.worker_id == worker_id).
                filter(workers_table.c.worker_id == worker_id).
                values(username=new_username)
            )
            conn.execute(stmt)
            conn.commit()


class AsyncCore:

    @staticmethod
    async def create_tables():
        async with async_engine.connect() as conn:
            await conn.run_sync(metadata_obj.drop_all)
            await conn.run_sync(metadata_obj.create_all)
