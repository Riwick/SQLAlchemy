import asyncio
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], ".."))

from src.queries.orm import insert_data, create_tables, async_insert_data


create_tables()

asyncio.run(async_insert_data())
