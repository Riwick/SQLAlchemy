from sqlalchemy import select, cast, func, Integer, and_
from sqlalchemy.orm import selectinload, joinedload

from src.database import session_factory
from src.models import ResumesORM, VacanciesORM
from src.schemas.vacancies_schemas import ResumesRelVacanciesRepliedDTO


class ResumesQueries:

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
    def select_resumes():
        with session_factory() as session:
            query = (
                select(ResumesORM).options(selectinload(ResumesORM.worker))
                .limit(2)
            )
            res = session.execute(query).scalars().all()

            return res

    @staticmethod
    def add_vacancies_and_replies():
        with session_factory() as session:
            new_vacancy = VacanciesORM(title="Python Разработчик", compensation=100000)
            resume_1 = session.get(ResumesORM, 1)
            resume_2 = session.get(ResumesORM, 2)
            resume_1.vacancies_replied.append(new_vacancy)
            resume_2.vacancies_replied.append(new_vacancy)
            session.commit()

    @staticmethod
    def select_resumes_with_all_relationships():
        with session_factory() as session:
            query = (
                select(ResumesORM)
                .options(selectinload(ResumesORM.worker))
                .options(joinedload(ResumesORM.vacancies_replied))
            )
            result = session.execute(query).unique().scalars().all()
            result = [ResumesRelVacanciesRepliedDTO.model_validate(row, from_attributes=True) for row in result]
            return result
