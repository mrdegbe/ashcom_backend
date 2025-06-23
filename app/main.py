# FastAPI entry point

from fastapi import FastAPI
from .api import router
from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ASHCOM Job Tracking API", version="1.0.0")

app.include_router(router)
