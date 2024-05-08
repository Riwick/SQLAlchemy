from sqlalchemy import select, func, cast, Integer, insert
from sqlalchemy.orm import aliased

from src.database import sync_engine, async_session_factory, Base
from src.models import WorkersORM, ResumesORM


class SyncORM:

    @staticmethod
    def create_tables():
        # Base.metadata.drop_all(sync_engine)
        sync_engine.echo = True
        Base.metadata.create_all(sync_engine)


class AsyncORM:

    @staticmethod
    async def async_insert_data():
        async with async_session_factory() as session:
            worker_bobr = WorkersORM(username="Bobr")
            worker_wolf = WorkersORM(username="Wolf")
            session.add_all([worker_bobr, worker_wolf])
            await session.commit()

    @staticmethod
    async def insert_additional_resumes():
        async with async_session_factory() as session:
            workers = [
                {"username": "Michail"},
                {"username": "Riwi"},
                {"username": "Bobr"},
                {"username": "Oleg"},
                {"username": "Pasha"},
            ]

            resumes = [
                {"title": "Python программист", "compensation": 60000, "workload": "full_time", "worker_id": 3},
                {"title": "Machine Learning Engineer", "compensation": 70000, "workload": "part_time", "worker_id": 1},
                {"title": "Python Data Scientist", "compensation": 80000, "workload": "part_time", "worker_id": 4},
                {"title": "Python Analyst", "compensation": 90000, "workload": "full_time", "worker_id": 2},
                {"title": "Python Junior Developer", "compensation": 100000, "workload": "full_time", "worker_id": 5},
            ]
            insert_workers = insert(WorkersORM).values(workers)
            insert_resumes = insert(ResumesORM).values(resumes)
            await session.execute(insert_workers)
            await session.commit()

            await session.execute(insert_resumes)
            await session.commit()

    @staticmethod
    async def join_cte_subquery_window_func(like_language: str = "Python"):
        """with helper2 as (
        select *, compensation - avg_workload_compensation as compensation_diff
        from
        (select
        w.worker_id,
        w.username,
        r.compensation,
        r.workload,
        avg(r.compensation) over (partition by workload)::int as avg_workload_compensation
        from resumes r
        join workers w on w.worker_id == r.worker_id helper1)

        select * from helper2
        order by compensation_diff desc"""

        r = aliased(ResumesORM)
        w = aliased(WorkersORM)

        subquery = (
            select(
                r,
                w,
                cast(func.avg(r.compensation).over(partition_by=r.workload), Integer).label("avg_workload_compensation")
            ).
            join(r, r.worker_id == w.worker_id).subquery("helper1")
        )
        cte = (
            select(
                subquery.c.worker_id,
                subquery.c.title,
                subquery.c.username,
                subquery.c.compensation,
                subquery.c.workload,
                subquery.c.avg_workload_compensation,
                (subquery.c.compensation - subquery.c.avg_workload_compensation).label("compensation_diff")
            ).
            cte("helper2")
        )
        query = (
            select(cte).where(cte.c.title.contains(like_language)).order_by(cte.c.compensation_diff.desc())
        )

        print(query.compile(compile_kwargs={"literal_binds": True}))

        async with async_session_factory() as session:
            result = await session.execute(query)
            print(result.all())
