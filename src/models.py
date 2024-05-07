import datetime
import enum
from typing import Optional, Annotated

from sqlalchemy import Table, Column, String, Integer, MetaData, ForeignKey, text, CheckConstraint, Index, PrimaryKeyConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database import Base, str_256

integer_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                        onupdate=datetime.datetime.utcnow)]


class WorkersORM(Base):
    __tablename__ = "workers"

    worker_id: Mapped[integer_pk]
    username: Mapped[str]

    resumes: Mapped[list["ResumesORM"] | None] = relationship(
        back_populates="worker_id",
    )

    resumes_part_time: Mapped[list["ResumesORM"] | None] = relationship(
        back_populates="worker_id",
        primaryjoin="and_(WorkersORM.worker_id == ResumesORM.worker, ResumesORM.workload == 'part_time')",
        order_by="ResumesORM.resume_id.desc()",
        # lazy="selectin"  # неявная подгрузка
    )

    repr_cols_num = 2


class WorkLoad(enum.Enum):
    part_time = "part_time"
    full_time = "full_time"


class ResumesORM(Base):
    __tablename__ = "resumes"

    resume_id: Mapped[integer_pk]
    title: Mapped[str_256]
    compensation: Mapped[Optional[int]]
    workload: Mapped[WorkLoad]
    worker: Mapped[int] = mapped_column(ForeignKey("workers.worker_id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    worker_id: Mapped["WorkersORM"] = relationship(
        back_populates="resumes"
    )

    repr_cols_num = 3
    repr_cols = ("worker", "created_at")

    __table_args__ = (
        PrimaryKeyConstraint("resume_id", "resume_pk"),  # Первичный ключ
        Index("title_index", "title"),  # B-Tree индекс
        CheckConstraint("compensation > 0", "check_compensation_positive")  # Какие-то правила для полей
    )


metadata_obj = MetaData()

workers_table = Table(
    "workers",
    metadata_obj,
    Column("worker_id", Integer, primary_key=True),
    Column("username", String),
)
