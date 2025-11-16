from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api.routes import router as api_router
from .db.init_db import init_db
from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    if settings.load_fake_data:
        print("loading fake data")
        from .db.session import engine
        from .db.fake.load_tables import load_tables

        load_tables(engine)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
