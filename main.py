from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core.models import Base, db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Async context manager for managing lifecycle Fastapi app.

    Function init the database when the app is launched.
    It creates all the tables in the database before the app starts working.

    Arguments:
        app (FastAPI): An instance of the Fastapi app.

    Behaviour:
        - Establishes a connection to the database.
        - Performs sync creation of all tables using 'Base.metadata.create_all'.
        - Transfers control to the app ('yield').

    """
    async with db_helper.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
