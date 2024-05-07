import datetime
import enum
from typing import Optional, Annotated

from sqlalchemy import ForeignKey, text
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

    resumes: Mapped[list["ResumesORM"]] = relationship(
        back_populates="worker",
    )

    repr_cols_num = 2

    __table_args__ = {'extend_existing': True}


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

    worker: Mapped["WorkersORM"] = relationship(
        back_populates="resumes",
    )

    repr_cols_num = 3
    repr_cols = ("created_at",)

    __table_args__ = {'extend_existing': True}
