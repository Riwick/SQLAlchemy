from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.database import session_factory
from src.models import VacanciesORM, VacanciesRepliesORM


class VacanciesQueries:

    @staticmethod
    def select_vacancies():
        with session_factory() as session:
            query = (
                select(VacanciesORM)
                .options(joinedload(VacanciesORM.resumes_replied))
            )
            result = session.execute(query).unique().scalars().all()
            return result

    @staticmethod
    def select_vacancies_replies():
        with session_factory() as session:
            query = (
                select(VacanciesRepliesORM)
            )
            result = session.execute(query).scalars().all()
            return result
