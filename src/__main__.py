from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.infra.persistence.adapters.db_connection import init_db
from src.app.controllers import user_controller

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(user_controller.router)
