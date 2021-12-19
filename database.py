from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

import asyncio

from variables import DATABASE_URL
from models import Base

async def setup_databse():
    engine = create_async_engine(DATABASE_URL, echo=False, future=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return engine

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
task = loop.create_task(setup_databse())
engine = loop.run_until_complete(task)
