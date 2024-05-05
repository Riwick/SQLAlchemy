from sqlalchemy import Table, Column, String, Integer, MetaData
from sqlalchemy.orm import mapped_column, Mapped
from src.database import Base


class WorkersORM(Base):
    __tablename__ = "workers"
    worker_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]

























metadata_obj = MetaData()


workers_table = Table(
    "workers",
    metadata_obj,
    Column("worker_id", Integer, primary_key=True),
    Column("username", String),
)
