import datetime
import enum
from typing import Optional, Annotated

from sqlalchemy import Table, Column, String, Integer, MetaData, ForeignKey, func, text
from sqlalchemy.orm import mapped_column, Mapped
from src.database import Base, str_256

integer_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                        onupdate=datetime.datetime.utcnow)]


class WorkersORM(Base):
    __tablename__ = "workers"

    worker_id: Mapped[integer_pk]
    username: Mapped[str]


class WorkLoad(enum.Enum):
    part_time = "part_time"
    full_time = "full_time"


class ResumesORM(Base):
    __tablename__ = "resumes"

    resume_id: Mapped[integer_pk]
    title: Mapped[str_256]
    compensation: Mapped[Optional[int]]
    workload: Mapped[WorkLoad]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.worker_id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


metadata_obj = MetaData()

workers_table = Table(
    "workers",
    metadata_obj,
    Column("worker_id", Integer, primary_key=True),
    Column("username", String),
)
