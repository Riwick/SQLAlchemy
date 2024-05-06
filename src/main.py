import asyncio

from src.queries.core import SyncCore
from src.queries.orm import SyncORM, AsyncORM

# SyncCore.create_tables()

SyncCore.select_workers()
# SyncCore.insert_workers()
SyncORM.select_workers()
#
# SyncORM.update_worker()
# SyncORM.select_resumes_avg_compensation()
asyncio.run(AsyncORM.join_cte_subquery_window_func())
