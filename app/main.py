from datetime import datetime
from logging import getLogger

from fastapi import FastAPI, Response
from pydantic import BaseModel

from app.database import Base, engine
from app.utils import check_env_variables

logger = getLogger(__name__)

try:
    check_env_variables()
except ValueError:
    logger.exception("Environment variables validation failed")
    raise

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root() -> Response:
    return Response(content="Hello, World!")


class HealthCheckResponse(BaseModel):
    status: str
    time: datetime


@app.get("/health", response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(status="ok", time=datetime.utcnow())
