from sqlalchemy import select, func, cast, Integer, and_, insert
from sqlalchemy.orm import aliased, joinedload, selectinload, contains_eager

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

    @staticmethod
    def select_workers_with_selectin_relationship():
        """Для связи o2m и m2m (один-ко-многим и многие-ко-многим)"""
        with session_factory() as session:
            query = (
                select(WorkersORM).options(selectinload(WorkersORM.resumes))
            )
            res = session.execute(query)
            result = res.unique().scalars().all()

            worker_1_resumes = result[3].resumes
            worker_2_resumes = result[2].resumes

            print(worker_1_resumes)
            print(worker_2_resumes)

    @staticmethod
    def select_workers_with_condition_relationships():
        with session_factory() as session:
            query = (
                select(WorkersORM).options(selectinload(WorkersORM.resumes_part_time))
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
                {"title": "Python программист", "compensation": 60000, "workload": "full_time", "worker": 3},
                {"title": "Machine Learning Engineer", "compensation": 70000, "workload": "part_time", "worker": 3},
                {"title": "Python Data Scientist", "compensation": 80000, "workload": "part_time", "worker": 4},
                {"title": "Python Analyst", "compensation": 90000, "workload": "full_time", "worker": 4},
                {"title": "Python Junior Developer", "compensation": 100000, "workload": "full_time", "worker": 5},
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
