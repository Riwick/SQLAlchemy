import asyncio

from src.queries.core import SyncCore
from src.queries.orm import SyncORM, AsyncORM


# SyncORM.create_tables()
# asyncio.run(AsyncORM.insert_additional_resumes())

# SyncORM.select_workers_with_joined_relationship()
# SyncORM.select_workers_with_lazy_relationship()
SyncORM.select_workers_with_selectin_relationship()

# asyncio.run(AsyncORM.join_cte_subquery_window_func())
