from fastapi import FastAPI
from contextlib import asynccontextmanager
from infra.persistence.adapters.db_connection import init_db
from app.controllers import user_controller, authentication_controller

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(prefix="/users", tags=["User"], router=user_controller.router)
app.include_router(
    prefix="/authentication",
    tags=["Authentication"],
    router=authentication_controller.router,
)
