from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI

from api_v1.auth.router import router as auth_router
from database.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """After application shutdown, database engine shutdown."""
    yield
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
